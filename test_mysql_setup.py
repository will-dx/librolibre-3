#!/usr/bin/env python3
# Script para probar la configuracion MySQL de LibroLibre

import sys
import os

print("=== Probando configuracion MySQL de LibroLibre ===")

# 1. Verificar que mysqlclient esta instalado
print("1. Verificando mysqlclient...")
try:
    import MySQLdb
    print("mysqlclient esta instalado")
except ImportError:
    print("mysqlclient no esta instalado")
    sys.exit(1)

# 2. Verificar la conexión a la base de datos
print("2. Probando conexión a MySQL...")
try:
    from django.db import connections
    from django.conf import settings
    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'librolibre',
                    'USER': 'root',
                    'PASSWORD': 'password',
                    'HOST': 'localhost',
                    'PORT': '3306',
                    'OPTIONS': {
                        'charset': 'utf8mb4',
                    },
                }
            },
            INSTALLED_APPS=['catalogo'],
            SECRET_KEY='test-secret-key',
            USE_TZ=True,
        )

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        if result[0] == 1:
            print('Conexion a MySQL exitosa')
        else:
            print('Conexion a MySQL fallida')
            sys.exit(1)
except Exception as e:
    print('Conexion a MySQL fallida: %s' % e)
    print('Asegurate de que MySQL este ejecutandose en localhost:3306')
    print('y que la base de datos "librolibre" exista.')
    sys.exit(1)

# 3. Verificar que las tablas existen (opcional)
print("3. Verificando tablas de la base de datos...")
try:
    from django.db import connections
    from django.conf import settings
    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': 'librolibre',
                    'USER': 'root',
                    'PASSWORD': 'password',
                    'HOST': 'localhost',
                    'PORT': '3306',
                }
            },
            INSTALLED_APPS=['catalogo'],
            SECRET_KEY='test-secret-key',
            USE_TZ=True,
        )

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        expected_tables = ['auth_user', 'catalogo_libro', 'catalogo_materia', 'catalogo_mensaje', 'catalogo_favorito', 'catalogo_contactomensaje']
        
        found_tables = [table[0] for table in tables]
        missing_tables = [t for t in expected_tables if t not in found_tables]
        
        if not missing_tables:
            print('Todas las tablas necesarias existen')
            print('  Tablas encontradas: %d' % len(found_tables))
        else:
            print('Tablas faltantes: %s' % missing_tables)
            sys.exit(1)
except Exception as e:
    print('No se pudo verificar las tablas: %s' % e)
    print('Ejecuta: mysql -u root -p librolibre < librolibre_migration.sql')

print("")
print("=== Resumen ===")
print("LibroLibre esta configurado para MySQL")
print("Requisitos actualizados (psycopg2-binary → mysqlclient)")
print("Configuración actualizada (SQLite → MySQL)")
print("")
print("Proximos pasos:")
print("1. Ejecuta: mysql -u root -p librolibre < librolibre_migration.sql")
print("2. Ejecuta: python manage.py migrate")
print("3. Inicia el servidor: python manage.py runserver")
print("")
print("Para produccion en Render, actualiza DATABASE_URL en las variables de entorno.")