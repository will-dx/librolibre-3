# AGENTS.md - LibroLibre (Proyecto Django)

## Resumen del Proyecto
- **Nombre**: LibroLibre - plataforma de intercambio de libros para estudiantes universitarios
- **Stack**: Python/Django, Supabase (PostgreSQL), Render (hosting)
- **Auth**: Autenticación integrada de Django (registro, login, sesiones, vistas protegidas)

## Esquema de Base de Datos (2 tablas)
- **Usuarios**: id, nombre, correo_institucional, contraseña
- **Libros**: id, titulo (NOT NULL), autor, estado, foto, usuario_id (FK)
- Relación: Un usuario → muchos libros

## Comandos Clave (Django)
```bash
# Configuración inicial
python -m venv venv && source venv/bin/activate
pip install django psycopg2 dj-database-url python-dotenv gunicorn

# Desarrollo
python manage.py runserver

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Archivos estáticos
python manage.py collectstatic

# Superusuario
python manage.py createsuperuser
```

## Variables de Entorno Requeridas
```
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://... (string de conexión Supabase)
```

## Despliegue (Render)
- Build command: Usar `./build.sh` (ejecuta pip install, collectstatic, migrate)
- Start command: `gunicorn config.wsgi:application`
- Agregar DATABASE_URL, SECRET_KEY, ALLOWED_HOSTS, DEBUG en variables de entorno de Render
- DATABASE_URL: `mysql://root:password@localhost:3306/librolibre`

## Estructura de la App (Django)
```
config/          # Configuración del proyecto, wsgi, urls
core/            # App principal: catálogo, CRUD libros, perfil
accounts/        # Modelo de usuario personalizado si se necesita (o usar auth de Django)
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── registro.html
    ├── catalogo.html
    ├── publicar.html
    └── perfil.html
```

## Notas de Implementación
- Campo `titulo` en modelo Libro DEBE tener `null=False, blank=False` (restricción NOT NULL)
- Usar `LoginRequiredMixin` de Django para vistas protegidas
- Catálogo de libros: layout de cards con imagen, título, autor, estado, botón "Solicitar"
- No se requiere integración de pagos (solo préstamos/donaciones)
- 4 pantallas principales: login, catálogo, formulario publicación, perfil
- Paleta de colores: `--primary: #6C5CE7` (púrpura), `--accent: #FF7675` (coral), `--gold: #FDCB6E` (dorado), `--teal: #00B894` (verde)
- Animaciones: fadeInUp en cards/secciones, shimmer en skeletons, heroFloat en hero, pulse en botones, slideDown en navbar
- CSS con custom properties para fácil re-theming y modo responsive