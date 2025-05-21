#!/usr/bin/env python3
"""
Script para configurar tablas de auditoría en la base de datos.

Este script crea las tablas y funciones necesarias para auditar cambios
en las tablas de la base de datos, incluyendo:
- Creación de tablas de auditoría
- Funciones para registrar cambios
- Triggers para capturar cambios automáticamente
"""
import argparse
import logging
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('audit_setup.log')
    ]
)
logger = logging.getLogger(__name__)

import os
from pathlib import Path
import sys

# Añadir el directorio raíz al path para importaciones absolutas
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(PROJECT_ROOT))

# Configuración de la base de datos desde variables de entorno
DEFAULT_DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'seguros_db'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

class AuditTableSetup:
    """Clase para configurar tablas y funciones de auditoría."""
    
    def __init__(self, db_config):
        """Inicializa la configuración de auditoría."""
        self.db_config = db_config
        self.conn = None
    
    def connect(self):
        """Establece conexión a la base de datos."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            logger.info("Conexión establecida con la base de datos")
            return True
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            return False
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            logger.info("Conexión cerrada")
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL y devuelve el resultado."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params or ())
                if cur.description:
                    return cur.fetchall()
                return None
        except Exception as e:
            logger.error(f"Error al ejecutar consulta: {e}")
            logger.debug(f"Consulta fallida: {query}")
            raise
    
    def check_audit_schema(self):
        """Verifica si existe el esquema de auditoría y lo crea si es necesario."""
        query = """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'audit') THEN
                CREATE SCHEMA audit;
                COMMENT ON SCHEMA audit IS 'Esquema para tablas y funciones de auditoría';
                RAISE NOTICE 'Esquema de auditoría creado';
            ELSE
                RAISE NOTICE 'El esquema de auditoría ya existe';
            END IF;
        END $$;
        """
        self.execute_query(query)
        logger.info("Verificando esquema de auditoría")
    
    def create_audit_log_table(self):
        """Crea la tabla principal de logs de auditoría."""
        query = """
        CREATE TABLE IF NOT EXISTS audit.logged_actions (
            event_id bigserial PRIMARY KEY,
            schema_name text NOT NULL,
            table_name text NOT NULL,
            user_name text,
            action_tstamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            action TEXT NOT NULL CHECK (action IN ('I','D','U')),
            original_data jsonb,
            new_data jsonb,
            query text,
            transaction_id bigint,
            application_name text,
            client_addr inet,
            client_port integer,
            client_query text,
            client_username text,
            client_application_name text,
            client_command_tag text,
            client_session_id text,
            client_backend_start timestamptz,
            client_xid bigint,
            client_xid_epoch bigint,
            client_in_abort boolean,
            client_in_error boolean
        );
        
        COMMENT ON TABLE audit.logged_actions IS 'Registro de cambios realizados en tablas auditadas';
        COMMENT ON COLUMN audit.logged_actions.event_id IS 'Identificador único del evento de auditoría';
        COMMENT ON COLUMN audit.logged_actions.schema_name IS 'Esquema de la base de datos de la tabla auditada';
        COMMENT ON COLUMN audit.logged_actions.table_name IS 'Tabla que se está auditando';
        COMMENT ON COLUMN audit.logged_actions.user_name IS 'Usuario de la base de datos que realizó el cambio';
        COMMENT ON COLUMN audit.logged_actions.action_tstamp IS 'Marca de tiempo del cambio';
        COMMENT ON COLUMN audit.logged_actions.action IS 'Tipo de acción: I=Insert, U=Update, D=Delete';
        COMMENT ON COLUMN audit.logged_actions.original_data IS 'Valores anteriores a la modificación (solo UPDATE/DELETE)';
        COMMENT ON COLUMN audit.logged_actions.new_data IS 'Nuevos valores (solo INSERT/UPDATE)';
        COMMENT ON COLUMN audit.logged_actions.query IS 'Consulta SQL que originó el cambio';
        
        -- Índices para mejorar el rendimiento de las consultas
        CREATE INDEX IF NOT EXISTS logged_actions_schema_table_idx 
        ON audit.logged_actions(schema_name, table_name);
        
        CREATE INDEX IF NOT EXISTS logged_actions_action_tstamp_idx 
        ON audit.logged_actions(action_tstamp);
        
        CREATE INDEX IF NOT EXISTS logged_actions_action_idx 
        ON audit.logged_actions(action);
        
        -- Particionamiento por mes para manejar grandes volúmenes de datos
        CREATE TABLE IF NOT EXISTS audit.logged_actions_default PARTITION OF audit.logged_actions 
        DEFAULT;
        
        COMMENT ON TABLE audit.logged_actions_default IS 'Partición por defecto para la tabla de logs de auditoría';
        
        -- Función para crear particiones mensuales automáticamente
        CREATE OR REPLACE FUNCTION audit.create_monthly_partition()
        RETURNS trigger AS $$
        DECLARE
            partition_start DATE;
            partition_end DATE;
            partition_name TEXT;
            partition_exists BOOLEAN;
        BEGIN
            -- Calcular el primer día del mes actual
            partition_start := DATE_TRUNC('month', CURRENT_DATE);
            -- Calcular el primer día del mes siguiente
            partition_end := partition_start + INTERVAL '1 month';
            -- Nombre de la partición: logged_actions_YYYY_MM
            partition_name := 'logged_actions_' || 
                             TO_CHAR(partition_start, 'YYYY_MM');
            
            -- Verificar si la partición ya existe
            SELECT EXISTS (
                SELECT 1 
                FROM pg_catalog.pg_class c
                JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                WHERE n.nspname = 'audit' 
                AND c.relname = partition_name
                AND c.relkind = 'r'
            ) INTO partition_exists;
            
            -- Crear la partición si no existe
            IF NOT partition_exists THEN
                EXECUTE format(
                    'CREATE TABLE audit.%I PARTITION OF audit.logged_actions ' ||
                    'FOR VALUES FROM (%L) TO (%L)',
                    partition_name,
                    partition_start,
                    partition_end
                );
                
                -- Crear índices en la nueva partición
                EXECUTE format(
                    'CREATE INDEX %I ON audit.%I (action_tstamp)',
                    partition_name || '_action_tstamp_idx',
                    partition_name
                );
                
                EXECUTE format(
                    'CREATE INDEX %I ON audit.%I (action)',
                    partition_name || '_action_idx',
                    partition_name
                );
                
                RAISE NOTICE 'Creada nueva partición de auditoría: %', partition_name;
            END IF;
            
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Programar la creación de particiones mensuales
        DO $$
        BEGIN
            -- Verificar si el trigger ya existe para evitar duplicados
            IF NOT EXISTS (
                SELECT 1 
                FROM pg_trigger 
                WHERE tgname = 'trigger_create_monthly_partition'
            ) THEN
                -- Crear un evento que se ejecute el primer día de cada mes
                PERFORM pg_catalog.pg_event_trigger_dropped();
                
                -- Usar pg_cron para programar la creación de particiones
                -- Nota: Requiere la extensión pg_cron instalada
                IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_cron') THEN
                    PERFORM cron.schedule(
                        'create_audit_partition',
                        '0 0 1 * *',  -- El primer día de cada mes a medianoche
                        'SELECT audit.create_monthly_partition()'
                    );
                    RAISE NOTICE 'Tarea programada para crear particiones mensuales';
                ELSE
                    RAISE NOTICE 'La extensión pg_cron no está instalada. No se pudo programar la creación de particiones.';
                END IF;
            END IF;
        END $$;
        
        -- Crear partición para el mes actual si no existe
        SELECT audit.create_monthly_partition();
        """
        
        self.execute_query(query)
        logger.info("Tabla de logs de auditoría configurada")
    
    def create_audit_trigger_function(self):
        """Crea la función que se ejecutará en los triggers de auditoría."""
        query = """
        CREATE OR REPLACE FUNCTION audit.if_modified_func() 
        RETURNS TRIGGER AS $$
        DECLARE
            audit_row audit.logged_actions;
            include_values boolean;
            log_diffs boolean;
            h_old jsonb;
            h_new jsonb;
            excluded_cols text[] = ARRAY[]::text[];
            row_data jsonb;
            changed_fields jsonb;
        BEGIN
            -- Verificar si la auditoría está habilitada para esta tabla
            IF TG_WHEN <> 'AFTER' THEN
                RAISE EXCEPTION 'audit.if_modified_func() solo puede ejecutarse con triggers AFTER';
            END IF;
            
            -- Configuración específica de la tabla
            -- Se pueden excluir columnas sensibles de ser auditadas
            -- Ejemplo: excluded_cols = ARRAY['password', 'token'];
            
            audit_row = ROW(
                nextval('audit.logged_actions_event_id_seq'), -- event_id
                TG_TABLE_SCHEMA::text,                        -- schema_name
                TG_TABLE_NAME::text,                          -- table_name
                session_user::text,                           -- user_name
                current_timestamp,                            -- action_tstamp
                substring(TG_OP, 1, 1),                       -- action
                NULL, NULL,                                   -- original_data, new_data
                current_query(),                              -- query
                txid_current(),                               -- transaction_id
                current_setting('application_name', true),    -- application_name
                inet_client_addr(),                           -- client_addr
                inet_client_port(),                           -- client_port
                NULL,                                         -- client_query
                current_user,                                 -- client_username
                current_setting('application_name', true),    -- client_application_name
                NULL,                                         -- client_command_tag
                NULL,                                         -- client_session_id
                NULL,                                         -- client_backend_start
                NULL,                                         -- client_xid
                NULL,                                         -- client_xid_epoch
                NULL,                                         -- client_in_abort
                NULL                                          -- client_in_error
            );
            
            -- Manejar diferentes tipos de operaciones
            IF TG_ARGV[0]::boolean IS DISTINCT FROM FALSE THEN
                audit_row.client_query = current_query();
            END IF;
            
            IF TG_ARGV[1] IS NOT NULL THEN
                excluded_cols = TG_ARGV[1]::text[];
            END IF;
            
            IF (TG_OP = 'UPDATE' AND TG_LEVEL = 'ROW') THEN
                -- Para actualizaciones, registrar solo los campos que cambiaron
                h_old = to_jsonb(OLD);
                h_new = to_jsonb(NEW);
                
                -- Filtrar columnas excluidas
                IF array_length(excluded_cols, 1) > 0 THEN
                    FOR i IN array_lower(excluded_cols, 1)..array_upper(excluded_cols, 1) LOOP
                        h_old = h_old - excluded_cols[i];
                        h_new = h_new - excluded_cols[i];
                    END LOOP;
                END IF;
                
                -- Encontrar campos que realmente cambiaron
                changed_fields = '{}'::jsonb;
                
                FOR key, value IN SELECT * FROM jsonb_each(h_new) LOOP
                    IF (h_old->key)::text IS DISTINCT FROM (h_new->key)::text THEN
                        changed_fields = jsonb_insert(
                            changed_fields,
                            ARRAY[key],
                            h_new->key
                        );
                    END IF;
                END LOOP;
                
                -- Si no hay cambios, no registrar nada
                IF changed_fields = '{}'::jsonb THEN
                    RETURN NULL;
                END IF;
                
                audit_row.original_data = h_old;
                audit_row.new_data = changed_fields;
                
            ELSIF (TG_OP = 'DELETE' AND TG_LEVEL = 'ROW') THEN
                -- Para eliminaciones, registrar el registro completo
                audit_row.original_data = to_jsonb(OLD);
                
                -- Filtrar columnas excluidas
                IF array_length(excluded_cols, 1) > 0 THEN
                    FOR i IN array_lower(excluded_cols, 1)..array_upper(excluded_cols, 1) LOOP
                        audit_row.original_data = audit_row.original_data - excluded_cols[i];
                    END LOOP;
                END IF;
                
            ELSIF (TG_OP = 'INSERT' AND TG_LEVEL = 'ROW') THEN
                -- Para inserciones, registrar el nuevo registro
                audit_row.new_data = to_jsonb(NEW);
                
                -- Filtrar columnas excluidas
                IF array_length(excluded_cols, 1) > 0 THEN
                    FOR i IN array_lower(excluded_cols, 1)..array_upper(excluded_cols, 1) LOOP
                        audit_row.new_data = audit_row.new_data - excluded_cols[i];
                    END LOOP;
                END IF;
                
            ELSE
                RAISE EXCEPTION '[audit.if_modified_func] - Trigger funcionó como disparador para operación % inesperada', TG_OP;
                RETURN NULL;
            END IF;
            
            INSERT INTO audit.logged_actions VALUES (audit_row.*);
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql SECURITY DEFINER;
        
        -- Comentarios para documentación
        COMMENT ON FUNCTION audit.if_modified_func() IS 'Función para registrar cambios en tablas auditadas';
        """
        
        self.execute_query(query)
        logger.info("Función de trigger de auditoría creada")
    
    def create_audit_trigger(self, schema_name, table_name, audit_query_text=False, excluded_columns=None):
        """Crea un trigger de auditoría para una tabla específica.
        
        Args:
            schema_name: Nombre del esquema de la tabla
            table_name: Nombre de la tabla a auditar
            audit_query_text: Si es True, registra la consulta completa que originó el cambio
            excluded_columns: Lista de columnas a excluir de la auditoría
        """
        if excluded_columns is None:
            excluded_columns = []
        
        # Convertir la lista de columnas excluidas a una cadena para SQL
        excluded_cols_str = "ARRAY['" + "','".join(excluded_columns) + "']" if excluded_columns else 'NULL'
        
        query = sql.SQL("""
        DO $$
        BEGIN
            -- Eliminar el trigger si ya existe
            DROP TRIGGER IF EXISTS {trigger_name} ON {schema_table};
            
            -- Crear el trigger
            CREATE TRIGGER {trigger_name}
            AFTER INSERT OR UPDATE OR DELETE ON {schema_table}
            FOR EACH ROW
            EXECUTE FUNCTION audit.if_modified_func({audit_query_text}, {excluded_columns});
            
            RAISE NOTICE 'Trigger de auditoría creado para %.%', '{schema_name}', '{table_name}';
        END $$;
        """).format(
            trigger_name=sql.Identifier(f'audit_trigger_{table_name}'),
            schema_table=sql.Identifier(schema_name, table_name),
            schema_name=sql.SQL(schema_name),
            table_name=sql.SQL(table_name),
            audit_query_text=sql.SQL('true' if audit_query_text else 'false'),
            excluded_columns=sql.SQL(excluded_cols_str)
        )
        
        try:
            self.execute_query(query)
            logger.info(f"Trigger de auditoría creado para {schema_name}.{table_name}")
            return True
        except Exception as e:
            logger.error(f"Error al crear trigger para {schema_name}.{table_name}: {e}")
            return False
    
    def setup_default_audit_tables(self):
        """Configura la auditoría para las tablas principales del sistema."""
        # Lista de tablas a auditar con sus columnas excluidas (si las hay)
        tables_to_audit = [
            # Formato: (esquema, tabla, [columnas_excluidas])
            ('public', 'usuarios', ['password_hash', 'reset_token', 'verification_token']),
            ('public', 'roles', []),
            ('public', 'permisos', []),
            ('public', 'usuario_roles', []),
            ('public', 'rol_permisos', []),
            ('public', 'sessions', ['data']),
            # Agregar más tablas según sea necesario
        ]
        
        # Crear triggers para cada tabla
        for schema, table, excluded_cols in tables_to_audit:
            self.create_audit_trigger(schema, table, audit_query_text=True, excluded_columns=excluded_cols)
    
    def setup_audit_system(self):
        """Configura todo el sistema de auditoría."""
        try:
            logger.info("Iniciando configuración del sistema de auditoría...")
            
            # Verificar y crear el esquema de auditoría
            self.check_audit_schema()
            
            # Crear la tabla de logs
            self.create_audit_log_table()
            
            # Crear la función del trigger
            self.create_audit_trigger_function()
            
            # Configurar auditoría para tablas por defecto
            self.setup_default_audit_tables()
            
            logger.info("Configuración de auditoría completada con éxito")
            return True
            
        except Exception as e:
            logger.error(f"Error al configurar el sistema de auditoría: {e}")
            return False

def parse_args():
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description='Configuración del sistema de auditoría de base de datos')
    
    # Argumentos de conexión a la base de datos
    parser.add_argument('--dbname', default=DEFAULT_DB_CONFIG['dbname'],
                       help='Nombre de la base de datos')
    parser.add_argument('--user', default=DEFAULT_DB_CONFIG['user'],
                       help='Usuario de la base de datos')
    parser.add_argument('--password', default=DEFAULT_DB_CONFIG['password'],
                       help='Contraseña de la base de datos')
    parser.add_argument('--host', default=DEFAULT_DB_CONFIG['host'],
                       help='Servidor de la base de datos')
    parser.add_argument('--port', default=DEFAULT_DB_CONFIG['port'],
                       help='Puerto de la base de datos')
    
    # Comandos
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando setup: Configura todo el sistema de auditoría
    subparsers.add_parser('setup', help='Configurar todo el sistema de auditoría')
    
    # Comando create-trigger: Crea un trigger de auditoría para una tabla específica
    trigger_parser = subparsers.add_parser('create-trigger', help='Crear un trigger de auditoría para una tabla')
    trigger_parser.add_argument('schema', help='Esquema de la tabla')
    trigger_parser.add_argument('table', help='Nombre de la tabla')
    trigger_parser.add_argument('--exclude', nargs='+', default=[], 
                              help='Columnas a excluir de la auditoría')
    trigger_parser.add_argument('--query-text', action='store_true',
                              help='Incluir la consulta SQL completa en el registro de auditoría')
    
    return parser.parse_args()

def main():
    """Función principal."""
    args = parse_args()
    
    # Configuración de la base de datos
    db_config = {
        'dbname': args.dbname,
        'user': args.user,
        'password': args.password,
        'host': args.host,
        'port': args.port
    }
    
    # Configurar el sistema de auditoría
    audit_setup = AuditTableSetup(db_config)
    
    try:
        # Conectar a la base de datos
        if not audit_setup.connect():
            logger.error("No se pudo conectar a la base de datos")
            return 1
        
        # Ejecutar el comando solicitado
        if args.command == 'setup':
            success = audit_setup.setup_audit_system()
            if not success:
                return 1
                
        elif args.command == 'create-trigger':
            success = audit_setup.create_audit_trigger(
                args.schema,
                args.table,
                audit_query_text=args.query_text,
                excluded_columns=args.exclude
            )
            if not success:
                return 1
                
        else:
            logger.error("Comando no reconocido. Use 'setup' o 'create-trigger'.")
            return 1
            
        return 0
        
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return 1
    finally:
        # Cerrar la conexión a la base de datos
        audit_setup.close()

if __name__ == "__main__":
    import sys
    sys.exit(main())
