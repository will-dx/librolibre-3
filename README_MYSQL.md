# LibroLibre - Configuración MySQL

## Resumen

Este proyecto ha sido migrado de Supabase (PostgreSQL) a MySQL para su despliegue en Render. El stack ahora es:

- **Backend**: Python/Django
- **Base de datos**: MySQL (en lugar de Supabase PostgreSQL)
- **Hosting**: Render
- **Autenticación**: Django Auth (CustomUser con email como username)

## Requisitos

```bash
# requirements.txt
mysqlclient  # Reemplaza psycopg2-binary
python-dotenv
dj-database-url
gunicorn
Pillow
whitenoise
```

## Configuración de la Base de Datos

### 1. Crear la base de datos MySQL

```bash
# Conectar a MySQL como root
mysql -u root -p

# Crear la base de datos
CREATE DATABASE librolibre CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Salir
exit
```

### 2. Ejecutar las migraciones

```bash
# Ejecutar el script de migración
mysql -u root -p librolibre < librolibre_migration.sql

# O ejecutar desde Python
python manage.py migrate
```

## Configuración de Visual Studio

### Opción A: Conexión Directa

1. **Instalar MySQL Connector/NET 8.0**
2. **Crear cadena de conexión**:
   ```
   Server=localhost;Port=3306;Database=librolibre;Uid=root;Pwd=password;Charset=utf8mb4;
   ```

### Opción B: Docker (Recomendado)

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```docker-compose.yml
version: '3.8'
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: librolibre
      MYSQL_CHARSET: utf8mb4
      MYSQL_COLLATION: utf8mb4_unicode_ci
    ports:
      - "3306:3306"
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql://root:root@db:3306/librolibre
    depends_on:
      - db
```

## Configuración de Render

### Variables de Entorno

```bash
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,librolibre-2.onrender.com
CSRF_TRUSTED_ORIGINS=https://librolibre-2.onrender.com
DATABASE_URL=mysql://root:password@localhost:3306/librolibre
```

### Comandos

```bash
# Build command
./build.sh

# Start command
"gunicorn config.wsgi:application"
```

## Tablas de la Base de Datos

### auth_user
- Usuarios personalizados con email como username
- Hereda de AbstractUser de Django

### catalogo_materia
- Materias (asignaturas) para clasificación de libros
- Campos: nombre, slug, descripcion, icono

### catalogo_libro
- Libros publicados por usuarios
- Campos: titulo, autor, estado, foto, usuario, materia, fecha_publicacion
- Estado: disponible/prestado/donado (ENUM)

### catalogo_mensaje
- Mensajes entre usuarios
- Campos: contenido, fecha_envio, leido, remitente, destinatario, libro

### catalogo_favorito
- Libros favoritos de usuarios
- Campos: usuario, libro, fecha_agregado
- Restricción única: usuario_id + libro_id

### catalogo_contactomensaje
- Mensajes del formulario de contacto
- Campos: nombre, email, asunto, mensaje, fecha_envio, leido

## Scripts de Utilidad

### test_mysql_setup.py
```bash
# Probar la configuración MySQL
python test_mysql_setup.py
```

### librolibre_migration.sql
```bash
# Ejecutar migraciones SQL directamente
mysql -u root -p librolibre < librolibre_migration.sql
```

## Diferencias Clave

### De Supabase (PostgreSQL) a MySQL

| Característica | Supabase (PostgreSQL) | MySQL |
|---------------|----------------------|-------|
| Driver | psycopg2-binary | mysqlclient |
| URL de conexión | postgresql://... | mysql://... |
| Tipos de datos | ENUM, JSONB | ENUM, JSON |
| Autoincremento | SERIAL | AUTO_INCREMENT |
| Valores por defecto | CURRENT_TIMESTAMP | CURRENT_TIMESTAMP |

### Ajustes Específicos de MySQL

1. **Tipos ENUM**: Usar `ENUM('disponible', 'prestado', 'donado')`
2. **Campos de imagen**: Almacenar URLs en VARCHAR(255)
3. **Usuarios personalizados**: Usar email como username (reemplaza username)
4. **Unicode**: Usar charset=utf8mb4 para soporte completo de emojis

## Problemas Comunes y Soluciones

### Error: "No module named 'app'"

**Causa**: Comando de inicio incorrecto en Render

**Solución**: Cambiar a `gunicorn config.wsgi:application`

### Error: Conexión rechazada

**Causa**: MySQL no está ejecutándose o contraseña incorrecta

**Solución**: 
```bash
# Iniciar MySQL (Linux/macOS)
sudo systemctl start mysql

# En Docker
./start-mysql.sh
```

### Error: Base de datos no existe

**Causa**: La base de datos 'librolibre' no existe

**Solución**:
```bash
mysql -u root -p -e "CREATE DATABASE librolibre CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

## Próximos Pasos

1. **Desarrollo Local**:
   ```bash
   # Iniciar MySQL
   sudo systemctl start mysql
   
   # Crear base de datos
   mysql -u root -p -e "CREATE DATABASE librolibre CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   
   # Ejecutar migraciones
   python manage.py migrate
   
   # Iniciar servidor
   python manage.py runserver
   ```

2. **Despliegue en Render**:
   - Conectar el repo `will-dx/librolibre-2`
   - Configurar variables de entorno
   - Hacer deploy

3. **Pruebas**:
   ```bash
   # Probar la configuración
   python test_mysql_setup.py
   
   # Probar endpoints
   curl http://localhost:8000/
   ```

## Recursos

- [Documentación de MySQL Connector/NET](https://dev.mysql.com/doc/connector-net/en/)
- [Documentación de Django sobre MySQL](https://docs.djangoproject.com/en/4.2/ref/databases/#mysql-database-backends)
- [Guía de Render para Python](https://render.com/docs/deploy-python)

---

**Nota**: Esta configuración es compatible con el stack original de LibroLibre y mantiene todas las funcionalidades mientras se migra de Supabase a MySQL.