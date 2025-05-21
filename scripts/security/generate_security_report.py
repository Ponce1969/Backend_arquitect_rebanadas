#!/usr/bin/env python3
"""
Script para generar informes de seguridad sobre intentos de inicio de sesión y bloqueos de cuentas.

Este script genera informes detallados sobre la actividad de inicio de sesión,
intentos fallidos, cuentas bloqueadas y actividad sospechosa en un rango de fechas.

Uso:
    python generate_security_report.py [--start FECHA_INICIO] [--end FECHA_FIN] [--output FORMATO]

Argumentos:
    --start FECHA_INICIO  Fecha de inicio en formato YYYY-MM-DD (por defecto: hace 7 días)
    --end FECHA_FIN      Fecha de fin en formato YYYY-MM-DD (por defecto: hoy)
    --output FORMATO     Formato de salida: 'text', 'csv' o 'json' (por defecto: 'text')
"""
import argparse
import json
import sys
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import RealDictCursor

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

class SecurityReporter:
    def __init__(self, db_config):
        """Inicializa el generador de informes.
        
        Args:
            db_config: Configuración de la base de datos
        """
        self.db_config = db_config
    
    def get_db_connection(self):
        """Establece una conexión a la base de datos."""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}", file=sys.stderr)
            sys.exit(1)
    
    def get_failed_login_stats(self, start_date, end_date):
        """Obtiene estadísticas de inicios de sesión fallidos por día.
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            Lista de diccionarios con las estadísticas por día
        """
        conn = self.get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT 
                        DATE(created_at) as fecha,
                        COUNT(*) as intentos,
                        COUNT(DISTINCT ip_address) as ips_unicas,
                        COUNT(DISTINCT username) as usuarios_unicos
                    FROM login_attempts
                    WHERE success = false
                    AND created_at BETWEEN %s AND %s
                    GROUP BY DATE(created_at)
                    ORDER BY fecha
                """
                cur.execute(query, (start_date, end_date))
                return cur.fetchall()
        finally:
            conn.close()
    
    def get_locked_accounts(self, start_date, end_date):
        """Obtiene información sobre cuentas bloqueadas.
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            Lista de diccionarios con información de cuentas bloqueadas
        """
        conn = self.get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT 
                        u.id,
                        u.username,
                        u.email,
                        u.bloqueado_hasta,
                        u.intentos_fallidos,
                        u.ultimo_intento_fallido,
                        la.ip_address as ultima_ip
                    FROM usuarios u
                    LEFT JOIN LATERAL (
                        SELECT ip_address 
                        FROM login_attempts 
                        WHERE username = u.username 
                        ORDER BY created_at DESC 
                        LIMIT 1
                    ) la ON true
                    WHERE u.bloqueado_hasta IS NOT NULL
                    AND u.bloqueado_hasta BETWEEN %s AND %s
                    ORDER BY u.bloqueado_hasta DESC
                """
                cur.execute(query, (start_date, end_date))
                return cur.fetchall()
        finally:
            conn.close()
    
    def get_suspicious_ips(self, start_date, end_date, threshold=5):
        """Identifica IPs con actividad sospechosa.
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            threshold: Umbral de intentos para considerar sospechoso
            
        Returns:
            Lista de diccionarios con información de IPs sospechosas
        """
        conn = self.get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    WITH ip_stats AS (
                        SELECT 
                            ip_address,
                            COUNT(*) as intentos,
                            COUNT(DISTINCT username) as usuarios_unicos,
                            MIN(created_at) as primer_intento,
                            MAX(created_at) as ultimo_intento
                        FROM login_attempts
                        WHERE success = false
                        AND created_at BETWEEN %s AND %s
                        GROUP BY ip_address
                        HAVING COUNT(*) >= %s
                    )
                    SELECT 
                        ip_address,
                        intentos,
                        usuarios_unicos,
                        primer_intento,
                        ultimo_intento,
                        EXTRACT(EPOCH FROM (ultimo_intento - primer_intento)) / 60 as minutos_entre_intentos
                    FROM ip_stats
                    ORDER BY intentos DESC
                """
                cur.execute(query, (start_date, end_date, threshold))
                return cur.fetchall()
        finally:
            conn.close()
    
    def get_failed_logins_by_hour(self, start_date, end_date):
        """Obtiene estadísticas de inicios de sesión fallidos por hora del día.
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            Lista de diccionarios con las estadísticas por hora
        """
        conn = self.get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT 
                        EXTRACT(HOUR FROM created_at) as hora,
                        COUNT(*) as intentos
                    FROM login_attempts
                    WHERE success = false
                    AND created_at BETWEEN %s AND %s
                    GROUP BY EXTRACT(HOUR FROM created_at)
                    ORDER BY hora
                """
                cur.execute(query, (start_date, end_date))
                return cur.fetchall()
        finally:
            conn.close()
    
    def generate_report(self, start_date, end_date, output_format='text'):
        """Genera un informe de seguridad.
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            output_format: Formato de salida ('text', 'csv' o 'json')
            
        Returns:
            El informe en el formato solicitado
        """
        print(f"Generando informe de seguridad del {start_date} al {end_date}...", file=sys.stderr)
        
        # Obtener datos
        failed_stats = self.get_failed_login_stats(start_date, end_date)
        locked_accounts = self.get_locked_accounts(start_date, end_date)
        suspicious_ips = self.get_suspicious_ips(start_date, end_date)
        hourly_stats = self.get_failed_logins_by_hour(start_date, end_date)
        
        # Calcular totales
        total_attempts = sum(day['intentos'] for day in failed_stats)
        total_locked = len(locked_accounts)
        total_suspicious = len(suspicious_ips)
        
        # Preparar datos para el informe
        report_data = {
            'rango_fechas': {
                'inicio': start_date.isoformat(),
                'fin': end_date.isoformat(),
                'dias': (end_date - start_date).days + 1
            },
            'resumen': {
                'intentos_fallidos_totales': total_attempts,
                'cuentas_bloqueadas': total_locked,
                'ips_sospechosas': total_suspicious,
                'promedio_diario': total_attempts / ((end_date - start_date).days + 1) if (end_date - start_date).days > 0 else total_attempts
            },
            'intentos_por_dia': [
                {
                    'fecha': str(day['fecha']),
                    'intentos': day['intentos'],
                    'ips_unicas': day['ips_unicas'],
                    'usuarios_unicos': day['usuarios_unicos']
                } for day in failed_stats
            ],
            'cuentas_bloqueadas': [
                {
                    'usuario': acc['username'],
                    'email': acc['email'],
                    'bloqueado_hasta': acc['bloqueado_hasta'].isoformat() if acc['bloqueado_hasta'] else None,
                    'intentos_fallidos': acc['intentos_fallidos'],
                    'ultimo_intento': acc['ultimo_intento_fallido'].isoformat() if acc['ultimo_intento_fallido'] else None,
                    'ultima_ip': acc['ultima_ip']
                } for acc in locked_accounts
            ],
            'ips_sospechosas': [
                {
                    'ip': ip['ip_address'],
                    'intentos': ip['intentos'],
                    'usuarios_unicos': ip['usuarios_unicos'],
                    'primer_intento': ip['primer_intento'].isoformat(),
                    'ultimo_intento': ip['ultimo_intento'].isoformat(),
                    'minutos_entre_intentos': float(ip['minutos_entre_intentos']) if ip['minutos_entre_intentos'] else 0
                } for ip in suspicious_ips
            ],
            'intentos_por_hora': [
                {
                    'hora': int(hour['hora']),
                    'intentos': hour['intentos']
                } for hour in hourly_stats
            ]
        }
        
        # Generar el informe en el formato solicitado
        if output_format == 'json':
            return json.dumps(report_data, indent=2, ensure_ascii=False)
        
        elif output_format == 'csv':
            # Para CSV, creamos un resumen y luego secciones separadas
            import io
            import csv
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Resumen
            writer.writerow(['Informe de Seguridad', f"{start_date} al {end_date}"])
            writer.writerow([])
            writer.writerow(['RESUMEN'])
            writer.writerow(['Total de intentos fallidos', total_attempts])
            writer.writerow(['Cuentas bloqueadas', total_locked])
            writer.writerow(['IPs sospechosas', total_suspicious])
            writer.writerow(['Promedio diario', f"{report_data['resumen']['promedio_diario']:.1f}"])
            
            # Intentos por día
            writer.writerow([])
            writer.writerow(['INTENTOS POR DÍA'])
            writer.writerow(['Fecha', 'Intentos', 'IPs únicas', 'Usuarios únicos'])
            for day in report_data['intentos_por_dia']:
                writer.writerow([day['fecha'], day['intentos'], day['ips_unicas'], day['usuarios_unicos']])
            
            # Cuentas bloqueadas
            if report_data['cuentas_bloqueadas']:
                writer.writerow([])
                writer.writerow(['CUENTAS BLOQUEADAS'])
                writer.writerow(['Usuario', 'Email', 'Bloqueado hasta', 'Intentos fallidos', 'Última IP'])
                for acc in report_data['cuentas_bloqueadas']:
                    writer.writerow([
                        acc['usuario'],
                        acc['email'],
                        acc['bloqueado_hasta'],
                        acc['intentos_fallidos'],
                        acc['ultima_ip']
                    ])
            
            # IPs sospechosas
            if report_data['ips_sospechosas']:
                writer.writerow([])
                writer.writerow(['IPS SOSPECHOSAS'])
                writer.writerow(['IP', 'Intentos', 'Usuarios', 'Primer intento', 'Último intento', 'Minutos entre intentos'])
                for ip in report_data['ips_sospechosas']:
                    writer.writerow([
                        ip['ip'],
                        ip['intentos'],
                        ip['usuarios_unicos'],
                        ip['primer_intento'],
                        ip['ultimo_intento'],
                        f"{ip['minutos_entre_intentos']:.1f}"
                    ])
            
            # Intentos por hora
            writer.writerow([])
            writer.writerow(['INTENTOS POR HORA'])
            writer.writerow(['Hora', 'Intentos'])
            for hour in report_data['intentos_por_hora']:
                writer.writerow([f"{int(hour['hora']):02d}:00", hour['intentos']])
            
            return output.getvalue()
        
        else:  # Formato de texto
            # Crear informe en formato de texto
            report = []
            
            # Encabezado
            report.append("=" * 80)
            report.append("INFORME DE SEGURIDAD".center(80))
            report.append("{} al {}".format(start_date, end_date).center(80))
            report.append("=" * 80)
            
            report.append("""
            
            RESUMEN:
            ---------
            • Intentos fallidos totales: {0}
            • Cuentas bloqueadas: {1}
            • IPs sospechosas: {2}
            • Promedio diario: {3:.1f} intentos/día
            
            INTENTOS POR DÍA:
            -----------------""".format(total_attempts, total_locked, total_suspicious, report_data['resumen']['promedio_diario']))
            
            # Intentos por día
            report.append("Fecha       Intentos  IPs únicas  Usuarios únicos")
            report.append("----------  --------  ----------  ----------------")
            for day in report_data['intentos_por_dia']:
                report.append("{0}  {1:8d}  {2:10d}  {3:15d}".format(
                    day['fecha'], day['intentos'], day['ips_unicas'], day['usuarios_unicos']
                ))
            
            # Cuentas bloqueadas
            if report_data['cuentas_bloqueadas']:
                report.append("""
            
            CUENTAS BLOQUEADAS:
            -------------------""")
                report.append("Usuario            Email                     Bloqueado hasta       Intentos  Última IP")
                report.append("-----------------  ------------------------  -------------------  ---------  ----------------")
                for acc in report_data['cuentas_bloqueadas']:
                    bloqueado_hasta = acc['bloqueado_hasta'].split('T')[0] if acc['bloqueado_hasta'] else 'N/A'
                    report.append("{0:17s}  {1:24s}  {2:19s}  {3:8d}  {4}".format(
                        acc['usuario'], acc['email'] or 'N/A', bloqueado_hasta, 
                        acc['intentos_fallidos'], acc['ultima_ip'] or 'N/A'
                    ))
            
            # IPs sospechosas
            if report_data['ips_sospechosas']:
                report.append("""
            
            IPS SOSPECHOSAS:
                ----------------""")
                report.append("IP               Intentos  Usuarios  Primer intento       Último intento        Min. entre intentos")
                report.append("---------------  --------  --------  -------------------  -------------------  --------------------")
                for ip in report_data['ips_sospechosas']:
                    primer_intento = ip['primer_intento'].split('.')[0].replace('T', ' ')
                    ultimo_intento = ip['ultimo_intento'].split('.')[0].replace('T', ' ')
                    report.append("{0:15s}  {1:8d}  {2:8d}  {3:19s}  {4:19s}  {5:19.1f}".format(
                        ip['ip'], ip['intentos'], ip['usuarios_unicos'], 
                        primer_intento, ultimo_intento, float(ip['minutos_entre_intentos'])
                    ))
            
            # Intentos por hora
            report.append("""
            
            INTENTOS POR HORA DEL DÍA:
            ------------------------""")
            
            report.append("Hora    Intentos  Gráfico")
            report.append("------  --------  ----------------------------------------")
            
            max_attempts = max(hour['intentos'] for hour in report_data['intentos_por_hora']) if report_data['intentos_por_hora'] else 1
            scale = 50.0 / max_attempts if max_attempts > 0 else 1
            
            for hour in sorted(report_data['intentos_por_hora'], key=lambda x: x['hora']):
                bar = '■' * int(hour['intentos'] * scale)
                report.append("{0:02d}:00   {1:7d}  {2}".format(
                    int(hour['hora']), hour['intentos'], bar
                ))
            
            report.append("""
            
            FIN DEL INFORME
            ===============""")
            
            return "\n".join(report)

def parse_date(date_str):
    """Parsea una cadena de fecha en formato YYYY-MM-DD."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError("Fecha inválida: {0}. Use el formato YYYY-MM-DD".format(date_str))

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Genera informes de seguridad')
    parser.add_argument('--start', type=parse_date, 
                       default=(datetime.now() - timedelta(days=7)).date(),
                       help='Fecha de inicio (YYYY-MM-DD)')
    parser.add_argument('--end', type=parse_date, 
                       default=datetime.now().date(),
                       help='Fecha de fin (YYYY-MM-DD)')
    parser.add_argument('--output', choices=['text', 'csv', 'json'], 
                       default='text',
                       help='Formato de salida (por defecto: text)')
    
    args = parser.parse_args()
    
    # Asegurarse de que la fecha de inicio sea anterior a la de fin
    if args.start > args.end:
        print("Error: La fecha de inicio debe ser anterior a la fecha de fin", file=sys.stderr)
        sys.exit(1)
    
    # Ajustar la fecha de fin para incluir todo el día
    end_date = datetime.combine(args.end, datetime.max.time())
    
    # Generar el informe
    reporter = SecurityReporter(DB_CONFIG)
    report = reporter.generate_report(args.start, end_date, args.output)
    
    # Imprimir el informe
    print(report)

if __name__ == "__main__":
    main()
