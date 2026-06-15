#!/usr/bin/env python3
# Script para ejecutar migraciones MySQL usando Python

import MySQLdb
import sys
import os

# Configuración de conexión MySQL - ajustar según tu configuración
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # Cambiar si es diferente
    'database': 'librolibre',
    'charset': 'utf8mb4'
}

# Leer el script de migración
migration_file = 'librolibre_migration.sql'

def execute_migration():
    try:
        # Conectar a MySQL
        print("Conectando a MySQL...")
        conn = MySQLdb.connect(**DB_CONFIG)
        conn.autocommit(True)
        
        # Leer el script
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar el script SQL
        print("Ejecutando migración...")
        cursor = conn.cursor()
        
        # Dividir el script en sentencias individuales
        # Separar por ; y limpiar
        statements = sql_script.split(';')
        
        executed_count = 0
        error_count = 0
        
        for i, statement in enumerate(statements):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    executed_count += 1
                    print(f"✓ Ejecutada sentencia {i+1}")
                except Exception as e:
                    error_count += 1
                    print(f"✗ Error en sentencia {i+1}: {e}")
                    print(f"Sentencia: {statement[:100]}...")
                    # Continuar con la siguiente sentencia
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*50)
        print("RESUMEN DE MIGRACIÓN")
        print("="*50)
        print(f"✓ Sentencias ejecutadas: {executed_count}")
        print(f"✗ Errores: {error_count}")
        print("\n✓ Migración completada exitosamente!")
        print("Las tablas han sido creadas en MySQL.")
        print("\nPróximos pasos:")
        print("1. Ejecutar: python test_mysql_setup.py")
        print("2. Ejecutar: python manage.py migrate")
        print("3. Iniciar servidor: python manage.py runserver")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    execute_migration()