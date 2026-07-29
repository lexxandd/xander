CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    distro_favorita TEXT DEFAULT '',
    rol TEXT NOT NULL DEFAULT 'miembro',
    creado_en TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS publicaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    contenido TEXT NOT NULL,
    categoria TEXT NOT NULL DEFAULT 'Testimonio',
    fijado INTEGER NOT NULL DEFAULT 0,
    autor_id INTEGER NOT NULL,
    creado_en TEXT NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES usuarios (id)
);

CREATE TABLE IF NOT EXISTS me_gusta (
    usuario_id INTEGER NOT NULL,
    publicacion_id INTEGER NOT NULL,
    creado_en TEXT NOT NULL,
    PRIMARY KEY (usuario_id, publicacion_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (publicacion_id) REFERENCES publicaciones (id)
);

CREATE TABLE IF NOT EXISTS comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contenido TEXT NOT NULL,
    autor_id INTEGER NOT NULL,
    publicacion_id INTEGER NOT NULL,
    creado_en TEXT NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES usuarios (id),
    FOREIGN KEY (publicacion_id) REFERENCES publicaciones (id)
);
