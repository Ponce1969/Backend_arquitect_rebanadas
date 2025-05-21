#!/usr/bin/env python3
"""
Script para monitorear los intentos de inicio de sesión fallidos en tiempo real.

Este script se conecta a la base de datos y muestra los intentos fallidos
de inicio de sesión a medida que ocurren, junto con información sobre
cuentas bloqueadas y actividad sospechosa.

Uso:
    python monitor_logins.py [--interval SECONDS] [--threshold COUNT]

Opciones:
    --interval SECONDS  Intervalo de actualización en segundos (por defecto: 5)
    --threshold COUNT   Umbral para resaltar IPs con muchos intentos (por defecto: 3)
"""
import time
import argparse
import signal
import sys
from datetime import datetime
from collections import defaultdict

import psycopg2

from psycopg2.extras import RealDictCursor

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
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'host': 'localhost',
    'port': '5432'
}

# Colores para la salida en consola
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class LoginMonitor:
    def __init__(self, db_config, update_interval=5, threshold=3):
        """Inicializa el monitor de inicios de sesión.
        
        Args:
            db_config: Configuración de la base de datos
            update_interval: Intervalo de actualización en segundos
            threshold: Umbral para resaltar IPs con muchos intentos
        """
        self.db_config = db_config
        self.update_interval = update_interval
        self.threshold = threshold
        self.running = True
        self.stats = {
            'total_attempts': 0,
            'failed_attempts': 0,
            'locked_accounts': 0,
            'suspicious_ips': defaultdict(int)
        }
        self.last_check = datetime.now()
        
        # Configurar el manejador de señales para salir limpiamente
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Maneja las señales de interrupción."""
        print("\n\nDeteniendo el monitor...")
        self.running = False
    
    def get_db_connection(self):
        """Establece una conexión a la base de datos."""
        try:
            conn = psycopg2.connect(**self.db_config)
            conn.autocommit = True
            return conn
        except Exception as e:
            print(f"{Colors.FAIL}Error al conectar a la base de datos: {e}{Colors.ENDC}")
            return None
    
    def get_failed_logins(self):
        """Obtiene los inicios de sesión fallidos desde la última verificación."""
        conn = self.get_db_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT id, username, ip_address, user_agent, created_at, success
                    FROM login_attempts
                    WHERE created_at > %s
                    ORDER BY created_at DESC
                """
                cur.execute(query, (self.last_check,))
                attempts = cur.fetchall()
                
                # Actualizar la hora de la última verificación
                self.last_check = datetime.now()
                
                return attempts
        except Exception as e:
            print(f"{Colors.FAIL}Error al obtener inicios de sesión fallidos: {e}{Colors.ENDC}")
            return []
        finally:
            conn.close()
    
    def get_locked_accounts(self):
        """Obtiene las cuentas actualmente bloqueadas."""
        conn = self.get_db_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                query = """
                    SELECT id, username, email, bloqueado_hasta, 
                           EXTRACT(EPOCH FROM (bloqueado_hasta - NOW()))/60 as minutos_restantes
                    FROM usuarios
                    WHERE bloqueado_hasta IS NOT NULL 
                    AND bloqueado_hasta > NOW()
                    ORDER BY bloqueado_hasta
                """
                cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            print(f"{Colors.FAIL}Error al obtener cuentas bloqueadas: {e}{Colors.ENDC}")
            return []
        finally:
            conn.close()
    
    def get_suspicious_activity(self):
        """Identifica actividad sospechosa (múltiples intentos desde la misma IP)."""
        conn = self.get_db_connection()
        if not conn:
            return []
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Buscar IPs con múltiples intentos fallidos en los últimos 15 minutos
                query = """
                    SELECT ip_address, COUNT(*) as intentos
                    FROM login_attempts
                    WHERE created_at > NOW() - INTERVAL '15 minutes'
                    AND success = false
                    GROUP BY ip_address
                    HAVING COUNT(*) >= %s
                    ORDER BY COUNT(*) DESC
                """
                cur.execute(query, (self.threshold,))
                return cur.fetchall()
        except Exception as e:
            print(f"{Colors.FAIL}Error al obtener actividad sospechosa: {e}{Colors.ENDC}")
            return []
        finally:
            conn.close()
    
    def print_header(self):
        """Imprime el encabezado del monitor."""
        print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'MONITOR DE INICIOS DE SESIÓN'.center(80)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"  {Colors.OKBLUE}•{Colors.ENDC} Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  {Colors.OKBLUE}•{Colors.ENDC} Intervalo de actualización: {self.update_interval} segundos")
        print(f"  {Colors.OKBLUE}•{Colors.ENDC} Umbral de IPs sospechosas: {self.threshold} intentos")
        print(f"  {Colors.OKBLUE}•{Colors.ENDC} {Colors.WARNING}Ctrl+C para salir{Colors.ENDC}")
        print(f"{Colors.HEADER}{'-'*80}{Colors.ENDC}")
    
    def print_failed_logins(self, logins):
        """Imprime los inicios de sesión fallidos."""
        if not logins:
            return
        
        print(f"\n{Colors.FAIL}ÚLTIMOS INTENTOS FALLIDOS:{Colors.ENDC}")
        print(f"{'Hora':<20} {'Usuario':<20} {'IP':<15} {'Navegador'}")
        print("-" * 80)
        
        for attempt in logins:
            timestamp = attempt['created_at'].strftime('%H:%M:%S')
            username = attempt['username'] or 'Desconocido'
            ip = attempt['ip_address'] or '0.0.0.0'
            user_agent = (attempt['user_agent'] or 'Desconocido')[:40] + '...' \
                        if attempt['user_agent'] and len(attempt['user_agent']) > 40 \
                        else (attempt['user_agent'] or 'Desconocido')
            
            # Resaltar si es un intento reciente (últimos 30 segundos)
            time_ago = (datetime.now() - attempt['created_at']).total_seconds()
            time_str = f"{Colors.WARNING}{timestamp}{Colors.ENDC}" if time_ago < 30 else timestamp
            
            print(f"{time_str:<20} {username:<20} {ip:<15} {user_agent}")
            
            # Actualizar estadísticas
            self.stats['total_attempts'] += 1
            if not attempt['success']:
                self.stats['failed_attempts'] += 1
                if ip:
                    self.stats['suspicious_ips'][ip] += 1
    
    def print_locked_accounts(self, accounts):
        """Imprime las cuentas actualmente bloqueadas."""
        if not accounts:
            return
        
        print(f"\n{Colors.WARNING}CUENTAS BLOQUEADAS:{Colors.ENDC}")
        print(f"{'Usuario':<20} {'Email':<30} {'Desbloqueo en'}")
        print("-" * 80)
        
        for account in accounts:
            username = account['username']
            email = account['email'] or 'Sin email'
            minutos = int(account['minutos_restantes'])
            
            if minutos <= 0:
                tiempo = "Inmediato"
            elif minutos < 60:
                tiempo = f"{minutos} min"
            else:
                horas = minutos // 60
                mins = minutos % 60
                tiempo = f"{horas}h {mins}m"
            
            print(f"{username:<20} {email[:28]:<30} {tiempo}")
            
            # Actualizar estadísticas
            self.stats['locked_accounts'] = len(accounts)
    
    def print_suspicious_ips(self, suspicious):
        """Imprime las IPs con actividad sospechosa."""
        if not suspicious:
            return
        
        print(f"\n{Colors.FAIL}ACTIVIDAD SOSPECHOSA:{Colors.ENDC}")
        print(f"{'IP':<15} {'Intentos'}")
        print("-" * 25)
        
        for item in suspicious:
            ip = item['ip_address']
            count = item['intentos']
            
            # Resaltar si supera el umbral
            if count >= self.threshold * 2:
                count_str = f"{Colors.FAIL}{count}{Colors.ENDC}"
            elif count >= self.threshold:
                count_str = f"{Colors.WARNING}{count}{Colors.ENDC}"
            else:
                count_str = str(count)
            
            print(f"{ip:<15} {count_str}")
    
    def print_stats(self):
        """Imprime las estadísticas de monitoreo."""
        print(f"\n{Colors.HEADER}ESTADÍSTICAS:{Colors.ENDC}")
        print(f"  • Intentos totales: {self.stats['total_attempts']}")
        print(f"  • Intentos fallidos: {self.stats['failed_attempts']}")
        print(f"  • Cuentas bloqueadas: {self.stats['locked_accounts']}")
        
        # Mostrar IPs más problemáticas
        if self.stats['suspicious_ips']:
            top_ips = sorted(
                self.stats['suspicious_ips'].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]  # Top 3 IPs
            
            print("  • IPs más activas:")
            for ip, count in top_ips:
                print(f"    - {ip}: {count} intentos")
    
    def run(self):
        """Ejecuta el bucle principal del monitor."""
        print(f"{Colors.OKGREEN}Iniciando monitor de inicios de sesión...{Colors.ENDC}")
        print(f"Presiona {Colors.WARNING}Ctrl+C{Colors.ENDC} para salir\n")
        
        try:
            while self.running:
                # Limpiar la pantalla (funciona en la mayoría de terminales Unix/Linux)
                print("\033[H\033[J", end="")
                
                # Obtener y mostrar datos
                self.print_header()
                
                # Obtener datos
                failed_logins = self.get_failed_logins()
                locked_accounts = self.get_locked_accounts()
                suspicious_ips = self.get_suspicious_activity()
                
                # Mostrar datos
                self.print_failed_logins(failed_logins)
                self.print_locked_accounts(locked_accounts)
                self.print_suspicious_ips(suspicious_ips)
                self.print_stats()
                
                # Esperar antes de la siguiente actualización
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            print("\nDeteniendo el monitor...")
        except Exception as e:
            print(f"\n{Colors.FAIL}Error en el monitor: {e}{Colors.ENDC}")
        finally:
            print(f"{Colors.OKGREEN}Monitor detenido.{Colors.ENDC}")

def parse_args():
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description='Monitor de inicios de sesión fallidos')
    parser.add_argument('--interval', type=int, default=5,
                       help='Intervalo de actualización en segundos (por defecto: 5)')
    parser.add_argument('--threshold', type=int, default=3,
                       help='Umbral para resaltar IPs con muchos intentos (por defecto: 3)')
    return parser.parse_args()

def main():
    """Función principal."""
    args = parse_args()
    
    # Configuración de la base de datos
    db_config = DEFAULT_DB_CONFIG
    
    # Crear e iniciar el monitor
    monitor = LoginMonitor(
        db_config=db_config,
        update_interval=args.interval,
        threshold=args.threshold
    )
    
    try:
        monitor.run()
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
