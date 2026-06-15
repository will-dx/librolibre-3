#!/usr/bin/env python3
# Script simplificado para crear tablas MySQL esenciales de LibroLibre

import sys
import os

def create_essential_tables():
    """Create only the essential tables for LibroLibre"""
    
    # Configuración de conexión MySQL
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'librolibre',
        'charset': 'utf8mb4'
    }
    
    try:
        import MySQLdb
        
        # Conectar a MySQL
        print("Conectando a MySQL...")
        conn = MySQLdb.connect(**DB_CONFIG)
        conn.autocommit(True)
        
        print("Ejecutando migracion simplificada...")
        cursor = conn.cursor()
        
        # SQL de eliminación primero
        drop_sql = """
DROP TABLE IF EXISTS favoritos;
DROP TABLE IF EXISTS mensajes;
DROP TABLE IF EXISTS materias;
DROP TABLE IF EXISTS libros;
DROP TABLE IF EXISTS usuarios;
"""
        
        # SQL de creación
        create_sql = """
CREATE TABLE usuarios (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    username VARCHAR(150) NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE libros (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(200) NULL,
    estado ENUM('disponible', 'prestado', 'donado') NOT NULL DEFAULT 'disponible',
    foto VARCHAR(255) NULL,
    usuario_id BIGINT UNSIGNED NOT NULL,
    INDEX idx_titulo (titulo),
    INDEX idx_estado (estado),
    INDEX idx_usuario (usuario_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE materias (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT NULL,
    icono VARCHAR(10) NOT NULL DEFAULT '📖',
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE mensajes (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    contenido TEXT NOT NULL,
    fecha_envio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    leido BOOLEAN NOT NULL DEFAULT 0,
    remitente_id BIGINT UNSIGNED NOT NULL,
    destinatario_id BIGINT UNSIGNED NOT NULL,
    libro_id BIGINT UNSIGNED NULL,
    INDEX idx_fecha_envio (fecha_envio),
    INDEX idx_leido (leido),
    INDEX idx_remitente (remitente_id),
    INDEX idx_destinatario (destinatario_id),
    INDEX idx_libro (libro_id),
    FOREIGN KEY (remitente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (destinatario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE favoritos (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fecha_agregado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_id BIGINT UNSIGNED NOT NULL,
    libro_id BIGINT UNSIGNED NOT NULL,
    UNIQUE KEY unique_usuario_libro (usuario_id, libro_id),
    INDEX idx_fecha_agregado (fecha_agregado),
    INDEX idx_usuario (usuario_id),
    INDEX idx_libro (libro_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO usuarios (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, nombre) 
VALUES (
    'pbkdf2_sha256$260000$dummy$dummy',
    NULL,
    1,
    'admin',
    'Administrador',
    'Sistema',
    'admin@librolibre.com',
    1,
    1,
    NOW(),
    'Administrador Sistema'
);

INSERT INTO materias (nombre, slug, descripcion, icono) VALUES
('Matemáticas', 'matematicas', 'Materias relacionadas con las matemáticas', '📐'),
('Física', 'fisica', 'Materias relacionadas con la física', '⚛️'),
('Química', 'quimica', 'Materias relacionadas con la química', '🧪'),
('Biología', 'biologia', 'Materias relacionadas con la biología', '🧬'),
('Historia', 'historia', 'Materias relacionadas con la historia', '📚');
"""
        
        # Ejecutar SQL de eliminación primero
        cursor.execute(drop_sql)
        
        # Luego ejecutar SQL de creación
        cursor.execute(create_sql)
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("MIGRACION SIMPLIFICADA COMPLETADA")
        print("="*60)
        print("5 tablas esenciales creadas exitosamente!")
        print("\nTablas creadas:")
        print("  1. usuarios (CustomUser)")
        print("  2. libros (Libro)")
        print("  3. materias (Materia)")
        print("  4. mensajes (Mensaje)")
        print("  5. favoritos (Favorito)")
        print("\nTodas las tablas incluyen indices y restricciones de clave foranea.")
        
        return True
        
    except Exception as e:
        print("Error: %s" % e)
        return False

if __name__ == '__main__':
    print("=== LibroLibre MySQL Migration (Simplificada) ===\n")
    
    if create_essential_tables():
        print("\nListo para continuar!")
        print("\nProximos pasos:")
        print("1. Ejecutar: python test_mysql_setup.py")
        print("2. Ejecutar: python manage.py migrate")
        print("3. Iniciar servidor: python manage.py runserver")
    else:
        print("\nLa migracion fallo.")
        sys.exit(1)