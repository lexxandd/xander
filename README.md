# Comunidad Linux

Proyecto escolar: un sitio web hecho con **Flask (Python)** para fomentar la
migración a Linux, mostrando sus ventajas/desventajas, comparando distros, y
ofreciendo una comunidad real donde los usuarios se registran, publican y
comentan.

## Funciones

- Página de inicio con resumen de ventajas y distros destacadas
- Comparativa completa de ventajas y desventajas de Linux
- Tabla comparativa de distros (Ubuntu, Mint, Fedora, Pop!_OS, Debian, Arch)
- Página de recursos con herramientas para instalar/probar Linux
- Registro e inicio de sesión de usuarios (contraseñas cifradas)
- Publicaciones de la comunidad con categorías (Testimonio, Pregunta,
  Tutorial, Recomendación, Debate)
- Comentarios en cada publicación
- Sistema de "me gusta"
- Perfil público por usuario con sus publicaciones

## Cómo ejecutarlo

1. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```
   python app.py
   ```
3. Abre `http://127.0.0.1:5000` en tu navegador.

La base de datos (`comunidad.db`) se crea automáticamente la primera vez
que se ejecuta, usando SQLite — no necesita instalación aparte.

## Estructura del proyecto

```
comunidad_linux/
├── app.py              # rutas y lógica principal
├── database.py         # conexión a la base de datos SQLite
├── contenido.py        # contenido estático (ventajas, distros, recursos)
├── schema.sql           # definición de las tablas
├── requirements.txt     # dependencias (solo Flask)
├── static/
│   ├── css/estilo.css
│   └── js/principal.js
└── templates/           # todas las vistas HTML
```

## Tecnologías usadas

- **Flask** — framework web de Python
- **SQLite** (vía `sqlite3`, incluido en Python) — base de datos
- **Jinja2** — plantillas HTML (incluido con Flask)
- **Werkzeug** — cifrado de contraseñas (incluido con Flask)
- HTML, CSS y JavaScript vanilla — sin frameworks de frontend
