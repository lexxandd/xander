VENTAJAS = [
    {
        "titulo": "Es gratis y de código abierto",
        "texto": "No pagas licencias y cualquiera puede revisar, modificar o auditar el código fuente.",
    },
    {
        "titulo": "Seguridad",
        "texto": "Menos objetivo de virus y malware, permisos de usuario más estrictos por defecto.",
    },
    {
        "titulo": "Personalización total",
        "texto": "Puedes cambiar el escritorio, el kernel, el gestor de arranque... casi cualquier pieza del sistema.",
    },
    {
        "titulo": "Ligero y rápido",
        "texto": "Muchas distros corren bien en computadoras viejas donde Windows se sentiría lento.",
    },
    {
        "titulo": "Sin telemetría invasiva",
        "texto": "No hay anuncios en el menú de inicio ni recolección agresiva de datos por defecto.",
    },
    {
        "titulo": "Comunidad y soporte",
        "texto": "Foros, wikis y comunidades activas resuelven casi cualquier problema que puedas tener.",
    },
]

DESVENTAJAS = [
    {
        "titulo": "Curva de aprendizaje",
        "texto": "La terminal y algunos conceptos (permisos, paquetes) toman tiempo acostumbrarse.",
    },
    {
        "titulo": "Compatibilidad de software",
        "texto": "Programas como Adobe Photoshop o algunos juegos no tienen versión nativa para Linux.",
    },
    {
        "titulo": "Drivers de hardware",
        "texto": "Algunas tarjetas gráficas, impresoras o periféricos pueden requerir configuración extra.",
    },
    {
        "titulo": "Fragmentación",
        "texto": "Hay cientos de distros distintas, lo que puede confundir a quien recién empieza.",
    },
]

CATEGORIAS = ["Testimonio", "Pregunta", "Tutorial", "Recomendación", "Debate"]

RECURSOS = [
    {
        "titulo": "Crear un USB booteable",
        "texto": "Herramientas gratuitas para grabar el instalador de tu distro en una memoria USB.",
        "enlace": "https://etcher.balena.io/",
        "enlace_texto": "balenaEtcher",
    },
    {
        "titulo": "Probar Linux sin instalarlo",
        "texto": "Corre cualquier distro dentro de tu sistema actual, sin arriesgar nada, usando una máquina virtual.",
        "enlace": "https://www.virtualbox.org/",
        "enlace_texto": "VirtualBox",
    },
    {
        "titulo": "Documentación oficial de Ubuntu",
        "texto": "Guías paso a paso para instalación, drivers, y solución de problemas comunes.",
        "enlace": "https://help.ubuntu.com/",
        "enlace_texto": "help.ubuntu.com",
    },
    {
        "titulo": "ArchWiki",
        "texto": "Aunque uses otra distro, es la documentación técnica de Linux más completa que existe.",
        "enlace": "https://wiki.archlinux.org/",
        "enlace_texto": "wiki.archlinux.org",
    },
    {
        "titulo": "Comprobar compatibilidad de juegos",
        "texto": "Antes de migrar por completo, revisa si tus juegos de Steam funcionan bien en Linux.",
        "enlace": "https://www.protondb.com/",
        "enlace_texto": "ProtonDB",
    },
    {
        "titulo": "Alternativas a programas de Windows",
        "texto": "Directorio de programas libres equivalentes a software popular de Windows/Mac.",
        "enlace": "https://alternativeto.net/platform/linux/",
        "enlace_texto": "AlternativeTo",
    },
]

DISTROS = [
    {
        "nombre": "Linux Mint",
        "ideal_para": "Principiantes que vienen de Windows",
        "base": "Ubuntu / Debian",
        "escritorio": "Cinnamon",
        "nota": "Interfaz muy familiar, todo funciona out-of-the-box.",
    },
    {
        "nombre": "Ubuntu",
        "ideal_para": "Uso general y desarrollo",
        "base": "Debian",
        "escritorio": "GNOME",
        "nota": "La más popular, enorme comunidad y documentación.",
    },
    {
        "nombre": "Fedora",
        "ideal_para": "Quien quiere software reciente y estable",
        "base": "Independiente (Red Hat)",
        "escritorio": "GNOME",
        "nota": "Cercana a las tecnologías que luego usa Red Hat Enterprise Linux.",
    },
    {
        "nombre": "Pop!_OS",
        "ideal_para": "Gamers y creadores de contenido",
        "base": "Ubuntu",
        "escritorio": "COSMIC",
        "nota": "Excelente soporte para GPUs NVIDIA/AMD desde la instalación.",
    },
    {
        "nombre": "Debian",
        "ideal_para": "Servidores y estabilidad máxima",
        "base": "Independiente",
        "escritorio": "Varios (configurable)",
        "nota": "Base de muchas otras distros; prioriza estabilidad sobre novedad.",
    },
    {
        "nombre": "Arch Linux",
        "ideal_para": "Usuarios avanzados que quieren control total",
        "base": "Independiente",
        "escritorio": "Ninguno por defecto",
        "nota": "Instalación manual, aprendes a fondo cómo funciona el sistema.",
    },
]
