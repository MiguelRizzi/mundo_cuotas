// funcion para animar teniendo segun la direccion
function direccionAnimacion(elem, direction) {
    direction = direction || 1;
    var x = 0,
        y = direction * 100;

    // Determina las coordenadas de traducción según la dirección
    if (elem.classList.contains("izquierda")) {
        x = -100;
        y = 0;
    } else if (elem.classList.contains("derecha")) {
        x = 100;
        y = 0;
    }

    elem.style.transform = "translate(" + x + "px, " + y + "px)";
    elem.style.opacity = "0";

    // animacion
    gsap.fromTo(elem, { x: x, y: y, autoAlpha: 0 }, {
        duration: 2.5,
        x: 0,
        y: 0,
        autoAlpha: 1,
        ease: "expo",
        overwrite: "auto"
    });
}

// funcion para ocultar el elemento
function ocultar(elem) {
    gsap.set(elem, { autoAlpha: 0 });
}

document.addEventListener("DOMContentLoaded", function () {
    if (window.matchMedia("(min-width: 1200px)").matches) {
        gsap.registerPlugin(ScrollTrigger);

        // ScrollTriger para cada elemento con la clase .revelar     
        gsap.utils.toArray(".revelar").forEach(function (elem) {
            ScrollTrigger.create({
                trigger: elem,
                markers: false,
                onEnter: function () { direccionAnimacion(elem) }, // anima el elemento al entrar en la vista
                onEnterBack: function () { direccionAnimacion(elem, -1) }, // anima el elemento al retroceder a la vista
                onLeave: function () { ocultar(elem) } // oculta el elemento al salir de la vista
            });
        });
    }
});