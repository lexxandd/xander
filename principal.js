// Menú móvil
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("menuToggle");
    const nav = document.getElementById("navPrincipal");
    if (toggle && nav) {
        toggle.addEventListener("click", () => nav.classList.toggle("abierto"));
    }
});

// Efecto de escritura tipo terminal en el hero
function escribirTerminal(texto) {
    const destino = document.getElementById("lineaEscrita");
    if (!destino) return;

    const reducirMovimiento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reducirMovimiento) {
        destino.textContent = texto;
        return;
    }

    let i = 0;
    function escribirSiguiente() {
        if (i <= texto.length) {
            destino.textContent = texto.slice(0, i);
            i++;
            setTimeout(escribirSiguiente, 45);
        }
    }
    escribirSiguiente();
}
