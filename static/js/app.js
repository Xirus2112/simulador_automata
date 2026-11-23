"use strict";

async function renderizarGraficas() {
  const contenedores = document.querySelectorAll("[data-grafica]");
  if (contenedores.length === 0) return;

  let instancia;
  try {
    instancia = await Viz.instance();
  } catch {
    contenedores.forEach((contenedor) => {
      contenedor.querySelector(".estado-grafica").textContent = "No se pudo iniciar el visor local.";
    });
    return;
  }
  for (const contenedor of contenedores) {
    try {
      // La plantilla trae el DOT de Python. Viz.js lo dibuja como SVG.
      const dot = contenedor.querySelector("template").content.textContent;
      const svg = instancia.renderSVGElement(dot);
      svg.setAttribute("aria-hidden", "true");
      contenedor.replaceChildren(svg);
    } catch {
      contenedor.querySelector(".estado-grafica").textContent = "No se pudo dibujar el diagrama.";
    }
  }
}

const seleccionFinales = document.querySelector("[data-finales]");
if (seleccionFinales) {
  seleccionFinales.addEventListener("change", () => {
    // Mostramos el aviso cuando se quita la última selección de F.
    const aviso = seleccionFinales.querySelector("[data-aviso-finales]");
    aviso.hidden = Boolean(seleccionFinales.querySelector("input:checked"));
  });
}

renderizarGraficas();
