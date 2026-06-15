-- MySQL Migration Script for LibroLibre
-- Ejecutar con: mysql -u root -p librolibre < librolibre_migration.sql

-- Configuración de la base de datos
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Eliminar tablas si existen (para desarrollo)
DROP TABLE IF EXISTS catalogo_contactomensaje;
DROP TABLE IF EXISTS catalogo_favorito;
DROP TABLE IF EXISTS catalogo_mensaje;
DROP TABLE IF EXISTS catalogo_libro;
DROP TABLE IF EXISTS catalogo_materia;
DROP TABLE IF EXISTS auth_user;
DROP TABLE IF EXISTS auth_group;
DROP TABLE IF EXISTS auth_permission;
DROP TABLE IF EXISTS auth_group_permissions;
DROP TABLE IF EXISTS django_content_type;
DROP TABLE IF EXISTS django_session;
DROP TABLE IF EXISTS auth_user_groups;
DROP TABLE IF EXISTS auth_user_user_permissions;

-- Tabla de usuarios (CustomUser)
CREATE TABLE auth_user (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT 0,
    username VARCHAR(150) NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    UNIQUE KEY email_unique (email),
    INDEX idx_username (username),
    INDEX idx_is_staff (is_staff),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de materias
CREATE TABLE catalogo_materia (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT NULL,
    icono VARCHAR(10) NOT NULL DEFAULT '📖',
    INDEX idx_nombre (nombre),
    INDEX idx_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de libros
CREATE TABLE catalogo_libro (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(200) NULL,
    estado ENUM('disponible', 'prestado', 'donado') NOT NULL DEFAULT 'disponible',
    foto VARCHAR(255) NULL,
    usuario_id BIGINT UNSIGNED NOT NULL,
    materia_id BIGINT UNSIGNED NULL,
    fecha_publicacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_titulo (titulo),
    INDEX idx_estado (estado),
    INDEX idx_fecha_publicacion (fecha_publicacion),
    INDEX idx_usuario (usuario_id),
    INDEX idx_materia (materia_id),
    FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES catalogo_materia(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de mensajes
CREATE TABLE catalogo_mensaje (
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
    FOREIGN KEY (remitente_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (destinatario_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (libro_id) REFERENCES catalogo_libro(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de favoritos
CREATE TABLE catalogo_favorito (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fecha_agregado DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_id BIGINT UNSIGNED NOT NULL,
    libro_id BIGINT UNSIGNED NOT NULL,
    UNIQUE KEY unique_usuario_libro (usuario_id, libro_id),
    INDEX idx_fecha_agregado (fecha_agregado),
    INDEX idx_usuario (usuario_id),
    INDEX idx_libro (libro_id),
    FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (libro_id) REFERENCES catalogo_libro(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de mensajes de contacto
CREATE TABLE catalogo_contactomensaje (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    asunto VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    leido BOOLEAN NOT NULL DEFAULT 0,
    INDEX idx_fecha_envio (fecha_envio),
    INDEX idx_leido (leido),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tablas de Django auth
CREATE TABLE auth_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE auth_permission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content_type_id INT NOT NULL,
    codename VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    UNIQUE KEY content_type_id_codename_unique (content_type_id, codename),
    INDEX idx_content_type (content_type_id),
    INDEX idx_codename (codename)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE auth_group_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    permission_id INT NOT NULL,
    UNIQUE KEY group_id_permission_id_unique (group_id, permission_id),
    INDEX idx_group (group_id),
    INDEX idx_permission (permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE django_content_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE KEY app_label_model_unique (app_label, model),
    INDEX idx_app_label (app_label),
    INDEX idx_model (model)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date DATETIME NOT NULL,
    INDEX idx_expire_date (expire_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tablas many-to-many
CREATE TABLE auth_user_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    group_id INT NOT NULL,
    UNIQUE KEY user_id_group_id_unique (user_id, group_id),
    INDEX idx_user (user_id),
    INDEX idx_group (group_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE auth_user_user_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    permission_id INT NOT NULL,
    UNIQUE KEY user_id_permission_id_unique (user_id, permission_id),
    INDEX idx_user (user_id),
    INDEX idx_permission (permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar usuario administrador por defecto
INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, nombre) 
VALUES (
    'pbkdf2_sha256$260000$dummy$dummy',  -- contraseña dummy, cambiar después
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

-- Insertar algunas materias de ejemplo
INSERT INTO catalogo_materia (nombre, slug, descripcion, icono) VALUES
('Matemáticas', 'matematicas', 'Materias relacionadas con las matemáticas', '📐'),
('Física', 'fisica', 'Materias relacionadas con la física', '⚛️'),
('Química', 'quimica', 'Materias relacionadas con la química', '🧪'),
('Biología', 'biologia', 'Materias relacionadas con la biología', '🧬'),
('Historia', 'historia', 'Materias relacionadas con la historia', '📚'),
('Literatura', 'literatura', 'Materias relacionadas con la literatura', '📖');

SET FOREIGN_KEY_CHECKS = 1;

-- Mostrar tablas creadas
SHOW TABLES;