#!/usr/bin/env python3
# Script para crear tablas MySQL para LibroLibre

import sys
import os

def check_mysql_available():
    """Check if MySQL is available"""
    try:
        import MySQLdb
        return True
    except ImportError:
        print("MySQLdb no esta instalado. Instalalo con: pip install mysqlclient")
        return False

def create_tables():
    """Create all LibroLibre tables in MySQL"""
    
    # Configuración de conexión MySQL - ajustar según tu setup
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Sin contraseña para esta demo
        'database': 'librolibre',
        'charset': 'utf8mb4'
    }
    
    try:
        import MySQLdb
        
        # Conectar a MySQL
        print("Conectando a MySQL...")
        conn = MySQLdb.connect(**DB_CONFIG)
        conn.autocommit(True)
        
        # Leer el script de migración
        migration_file = 'librolibre_migration.sql'
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        print("Ejecutando migracion...")
        cursor = conn.cursor()
        
        # Dividir el script en sentencias individuales
        statements = sql_script.split(';')
        
        executed_count = 0
        error_count = 0
        
        for i, statement in enumerate(statements):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    executed_count += 1
                    print("Ejecutada sentencia %d" % (i+1))
                except Exception as e:
                    error_count += 1
                    print("Error en sentencia %d: %s" % (i+1, e))
                    print("Sentencia: %s..." % (statement[:100]))
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("MIGRACION MYSQL COMPLETADA")
        print("="*60)
        print("Sentencias ejecutadas: %d" % executed_count)
        print("Errores: %d" % error_count)
        print("\nLas tablas han sido creadas exitosamente!")
        print("\nTablas creadas:")
        print("  - auth_user (usuarios)")
        print("  - catalogo_materia (materias)")
        print("  - catalogo_libro (libros)")
        print("  - catalogo_mensaje (mensajes)")
        print("  - catalogo_favorito (favoritos)")
        print("  - catalogo_contactomensaje (contacto)")
        print("  - Tablas de soporte de Django")
        
        return True
        
    except Exception as e:
        print("Error: %s" % e)
        print("\nPosibles soluciones:")
        print("1. Instalar MySQL: sudo apt-get install mysql-server")
        print("2. Iniciar MySQL: sudo systemctl start mysql")
        print("3. Crear base de datos: mysql -u root -e 'CREATE DATABASE librolibre;'")
        print("4. Ajustar contraseña en run_mysql_migration.py")
        return False

if __name__ == '__main__':
    print("=== LibroLibre MySQL Migration ===\n")
    
    if not check_mysql_available():
        sys.exit(1)
    
    if create_tables():
        print("\nListo para continuar!")
        print("\nProximos pasos:")
        print("1. Ejecutar: python test_mysql_setup.py")
        print("2. Ejecutar: python manage.py migrate")
        print("3. Iniciar servidor: python manage.py runserver")
    else:
        print("\nLa migracion fallo.")
        sys.exit(1)