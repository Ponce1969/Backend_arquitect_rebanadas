#!/usr/bin/env python3
"""
Script para probar el sistema de auditoría.

Este script realiza operaciones de prueba en las tablas auditadas
y verifica que los cambios se registren correctamente en las tablas de auditoría.
"""
import sys
import random
import string
import logging
from faker import Faker

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('audit_test.log')
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
DB_CONFIG = {
    'dbname': os.getenv('POSTGRES_DB', 'seguros_db'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'host': os.getenv('POSTGRES_SERVER', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

class AuditTester:
    """Clase para probar el sistema de auditoría."""
    
    def __init__(self, db_config):
        """Inicializa el probador de auditoría."""
        self.db_config = db_config
        self.conn = None
        self.fake = Faker('es_ES')  # Usamos datos en español
        
        # Contadores para estadísticas
        self.stats = {
            'users_created': 0,
            'users_updated': 0,
            'users_deleted': 0,
            'roles_created': 0,
            'roles_updated': 0,
            'roles_deleted': 0,
            'audit_entries': 0
        }
    
    def connect(self):
        """Establece conexión a la base de datos."""
        try:
            import psycopg2
            from psycopg2.extras import DictCursor
            
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
            logger.info("Conexión establecida con la base de datos")
            return True
        except ImportError:
            logger.error("Se requiere el paquete 'psycopg2-binary' para conectarse a PostgreSQL")
            return False
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            return False
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logger.info("Conexión cerrada")
    
    def execute_query(self, query, params=None, fetchone=False):
        """Ejecuta una consulta y devuelve el resultado."""
        try:
            self.cursor.execute(query, params or ())
            if fetchone:
                return self.cursor.fetchone()
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error al ejecutar consulta: {e}")
            logger.debug(f"Consulta fallida: {query}")
            raise
    
    def generate_random_password(self, length=12):
        """Genera una contraseña aleatoria."""
        chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        return ''.join(random.choice(chars) for _ in range(length))
    
    def create_test_user(self):
        """Crea un usuario de prueba."""
        username = self.fake.user_name()
        email = self.fake.email()
        password = self.generate_random_password()
        nombre = self.fake.first_name()
        apellido = self.fake.last_name()
        activo = random.choice([True, False])
        
        query = """
        INSERT INTO usuarios (username, email, password_hash, nombre, apellido, activo, email_verificado)
        VALUES (%s, %s, crypt(%s, gen_salt('bf')), %s, %s, %s, %s)
        RETURNING id
        """
        
        try:
            self.cursor.execute(query, (username, email, password, nombre, apellido, activo, activo))
            user_id = self.cursor.fetchone()['id']
            logger.info(f"Usuario de prueba creado: {username} (ID: {user_id})")
            self.stats['users_created'] += 1
            return user_id
        except Exception as e:
            logger.error(f"Error al crear usuario de prueba: {e}")
            return None
    
    def update_test_user(self, user_id):
        """Actualiza un usuario de prueba."""
        # Obtener el usuario actual
        query = "SELECT id, username FROM usuarios WHERE id = %s"
        user = self.execute_query(query, (user_id,), fetchone=True)
        
        if not user:
            logger.warning(f"Usuario con ID {user_id} no encontrado")
            return False
        
        # Actualizar algunos campos
        new_email = self.fake.email()
        new_nombre = self.fake.first_name()
        new_apellido = self.fake.last_name()
        new_activo = not bool(random.getrandbits(1))  # 50% de probabilidad de cambiar el estado
        
        update_query = """
        UPDATE usuarios
        SET email = %s, nombre = %s, apellido = %s, activo = %s, updated_at = NOW()
        WHERE id = %s
        RETURNING id, username
        """
        
        try:
            self.cursor.execute(update_query, (new_email, new_nombre, new_apellido, new_activo, user_id))
            updated_user = self.cursor.fetchone()
            if updated_user:
                logger.info(f"Usuario actualizado: {updated_user['username']} (ID: {updated_user['id']})")
                self.stats['users_updated'] += 1
                return True
            return False
        except Exception as e:
            logger.error(f"Error al actualizar usuario: {e}")
            return False
    
    def delete_test_user(self, user_id):
        """Elimina un usuario de prueba."""
        # Obtener el usuario antes de eliminarlo para registrarlo
        query = "SELECT id, username FROM usuarios WHERE id = %s"
        user = self.execute_query(query, (user_id,), fetchone=True)
        
        if not user:
            logger.warning(f"Usuario con ID {user_id} no encontrado")
            return False
        
        delete_query = "DELETE FROM usuarios WHERE id = %s"
        
        try:
            self.cursor.execute(delete_query, (user_id,))
            if self.cursor.rowcount > 0:
                logger.info(f"Usuario eliminado: {user['username']} (ID: {user_id})")
                self.stats['users_deleted'] += 1
                return True
            return False
        except Exception as e:
            logger.error(f"Error al eliminar usuario: {e}")
            return False
    
    def create_test_role(self):
        """Crea un rol de prueba."""
        role_name = f"rol_{self.fake.word().lower()}"
        descripcion = self.fake.sentence()
        
        query = """
        INSERT INTO roles (nombre, descripcion, activo)
        VALUES (%s, %s, %s)
        RETURNING id
        """
        
        try:
            self.cursor.execute(query, (role_name, descripcion, True))
            role_id = self.cursor.fetchone()['id']
            logger.info(f"Rol de prueba creado: {role_name} (ID: {role_id})")
            self.stats['roles_created'] += 1
            return role_id
        except Exception as e:
            logger.error(f"Error al crear rol de prueba: {e}")
            return None
    
    def update_test_role(self, role_id):
        """Actualiza un rol de prueba."""
        # Obtener el rol actual
        query = "SELECT id, nombre FROM roles WHERE id = %s"
        role = self.execute_query(query, (role_id,), fetchone=True)
        
        if not role:
            logger.warning(f"Rol con ID {role_id} no encontrado")
            return False
        
        # Actualizar algunos campos
        new_descripcion = self.fake.sentence()
        new_activo = not bool(random.getrandbits(1))  # 50% de probabilidad de cambiar el estado
        
        update_query = """
        UPDATE roles
        SET descripcion = %s, activo = %s, updated_at = NOW()
        WHERE id = %s
        RETURNING id, nombre
        """
        
        try:
            self.cursor.execute(update_query, (new_descripcion, new_activo, role_id))
            updated_role = self.cursor.fetchone()
            if updated_role:
                logger.info(f"Rol actualizado: {updated_role['nombre']} (ID: {updated_role['id']})")
                self.stats['roles_updated'] += 1
                return True
            return False
        except Exception as e:
            logger.error(f"Error al actualizar rol: {e}")
            return False
    
    def delete_test_role(self, role_id):
        """Elimina un rol de prueba."""
        # Obtener el rol antes de eliminarlo para registrarlo
        query = "SELECT id, nombre FROM roles WHERE id = %s"
        role = self.execute_query(query, (role_id,), fetchone=True)
        
        if not role:
            logger.warning(f"Rol con ID {role_id} no encontrado")
            return False
        
        delete_query = "DELETE FROM roles WHERE id = %s"
        
        try:
            self.cursor.execute(delete_query, (role_id,))
            if self.cursor.rowcount > 0:
                logger.info(f"Rol eliminado: {role['nombre']} (ID: {role_id})")
                self.stats['roles_deleted'] += 1
                return True
            return False
        except Exception as e:
            logger.error(f"Error al eliminar rol: {e}")
            return False
    
    def check_audit_entries(self):
        """Verifica las entradas de auditoría generadas."""
        query = """
        SELECT 
            COUNT(*) as total,
            action,
            table_name
        FROM audit.logged_actions
        WHERE action_tstamp > NOW() - INTERVAL '1 hour'
        GROUP BY action, table_name
        ORDER BY table_name, action
        """
        
        try:
            results = self.execute_query(query)
            if not results:
                logger.warning("No se encontraron entradas de auditoría recientes")
                return False
            
            logger.info("\nResumen de entradas de auditoría:")
            logger.info("-" * 60)
            logger.info(f"{'Tabla':<20} {'Acción':<10} {'Total':<10}")
            logger.info("-" * 60)
            
            total = 0
            for row in results:
                logger.info(f"{row['table_name']:<20} {row['action']:<10} {row['total']:<10}")
                total += row['total']
            
            logger.info("-" * 60)
            logger.info(f"{'TOTAL':<20} {'':<10} {total:<10}")
            logger.info("-" * 60)
            
            self.stats['audit_entries'] = total
            return total > 0
            
        except Exception as e:
            logger.error(f"Error al verificar entradas de auditoría: {e}")
            return False
    
    def run_tests(self, num_operations=10):
        """Ejecuta una serie de pruebas de auditoría."""
        logger.info(f"Iniciando pruebas de auditoría ({num_operations} operaciones)")
        
        # Crear algunos usuarios y roles iniciales
        user_ids = []
        role_ids = []
        
        # Crear 5 usuarios iniciales
        for _ in range(5):
            user_id = self.create_test_user()
            if user_id:
                user_ids.append(user_id)
        
        # Crear 3 roles iniciales
        for _ in range(3):
            role_id = self.create_test_role()
            if role_id:
                role_ids.append(role_id)
        
        # Realizar operaciones aleatorias
        operations = [
            (self.create_test_user, 0.2),         # 20% de probabilidad
            (self.update_test_user, 0.3),         # 30% de probabilidad
            (self.delete_test_user, 0.1),         # 10% de probabilidad
            (self.create_test_role, 0.1),         # 10% de probabilidad
            (self.update_test_role, 0.2),         # 20% de probabilidad
            (self.delete_test_role, 0.1)          # 10% de probabilidad
        ]
        
        for _ in range(num_operations):
            # Seleccionar una operación aleatoria según las probabilidades
            op_weights = [op[1] for op in operations]
            selected_op = random.choices(operations, weights=op_weights, k=1)[0][0]
            
            # Ejecutar la operación seleccionada con un ID aleatorio si es necesario
            if selected_op == self.create_test_user:
                user_id = selected_op()
                if user_id:
                    user_ids.append(user_id)
            
            elif selected_op == self.update_test_user and user_ids:
                user_id = random.choice(user_ids)
                selected_op(user_id)
            
            elif selected_op == self.delete_test_user and user_ids:
                user_id = random.choice(user_ids)
                if selected_op(user_id):
                    user_ids.remove(user_id)
            
            elif selected_op == self.create_test_role:
                role_id = selected_op()
                if role_id:
                    role_ids.append(role_id)
            
            elif selected_op == self.update_test_role and role_ids:
                role_id = random.choice(role_ids)
                selected_op(role_id)
            
            elif selected_op == self.delete_test_role and role_ids:
                role_id = random.choice(role_ids)
                if selected_op(role_id):
                    role_ids.remove(role_id)
            
            # Pequeña pausa entre operaciones
            import time
            time.sleep(0.1)
        
        # Verificar las entradas de auditoría
        logger.info("\nVerificando entradas de auditoría...")
        audit_ok = self.check_audit_entries()
        
        # Mostrar resumen
        logger.info("\n" + "="*60)
        logger.info("RESUMEN DE PRUEBAS DE AUDITORÍA")
        logger.info("="*60)
        
        logger.info("\nUsuarios:")
        logger.info(f"  - Creados: {self.stats['users_created']}")
        logger.info(f"  - Actualizados: {self.stats['users_updated']}")
        logger.info(f"  - Eliminados: {self.stats['users_deleted']}")
        
        logger.info("\nRoles:")
        logger.info(f"  - Creados: {self.stats['roles_created']}")
        logger.info(f"  - Actualizados: {self.stats['roles_updated']}")
        logger.info(f"  - Eliminados: {self.stats['roles_deleted']}")
        
        logger.info("\nAuditoría:")
        logger.info(f"  - Entradas de auditoría generadas: {self.stats['audit_entries']}")
        
        logger.info("\nResultado: " + ("ÉXITO" if audit_ok else "FALLO"))
        logger.info("="*60 + "\n")
        
        return audit_ok

def parse_args():
    """Parsea los argumentos de línea de comandos."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Pruebas del sistema de auditoría')
    
    # Argumentos de conexión a la base de datos
    parser.add_argument('--dbname', default=DB_CONFIG['dbname'],
                       help='Nombre de la base de datos')
    parser.add_argument('--user', default=DB_CONFIG['user'],
                       help='Usuario de la base de datos')
    parser.add_argument('--password', default=DB_CONFIG['password'],
                       help='Contraseña de la base de datos')
    parser.add_argument('--host', default=DB_CONFIG['host'],
                       help='Servidor de la base de datos')
    parser.add_argument('--port', default=DB_CONFIG['port'],
                       help='Puerto de la base de datos')
    
    # Número de operaciones a realizar
    parser.add_argument('-n', '--num-operations', type=int, default=20,
                       help='Número de operaciones a realizar (por defecto: 20)')
    
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
    
    # Crear y ejecutar el probador de auditoría
    tester = AuditTester(db_config)
    
    try:
        # Conectar a la base de datos
        if not tester.connect():
            logger.error("No se pudo conectar a la base de datos")
            return 1
        
        # Ejecutar pruebas
        success = tester.run_tests(args.num_operations)
        return 0 if success else 1
        
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return 1
    finally:
        # Cerrar la conexión a la base de datos
        tester.close()

if __name__ == "__main__":
    sys.exit(main())
