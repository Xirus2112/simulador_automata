# Guía de sustentación para tres integrantes

Los tres integrantes deben entender la definición, usar los tres módulos y modificar un AFD desde el formulario. Cada integrante prepara una parte principal y practica las otras dos.

## Integrante 1 · Modelo formal

- Explique Q, Σ, δ, q₀ y F con A2. Señale por qué hay seis destinos y qué convierte a δ en función.
- Ejecute a mano `ab` y `aba`. Justifique los resultados usando el estado en el que termina la lectura.
- Compare ε en A1 y A2. Lleve preparada una explicación de un AFD con F vacío y de A4, donde F tiene un estado inalcanzable.

## Integrante 2 · Construcción, representación y gráfica

- Construya un AFD indicado en el momento. Recorra nombre, Q, Σ, δ, q₀ y F. Muestre el error de un destino que no pertenece a Q y corríjalo.
- Relacione una celda de la tabla con `transiciones[(estado, simbolo)]` y con una flecha del DOT. Señale el doble círculo, la flecha inicial y un bucle.
- Edite Q o Σ para demostrar qué celdas se conservan. Active el cambio y muestre que los tres módulos leen el AFD que acaba de guardar.

## Integrante 3 · Reconocimiento y búsqueda

- Procese `abab`, `aba`, ε y `abc` con A2. Explique dónde se actualiza el estado y cómo se obtiene la posición inválida.
- Muestre las cinco primeras palabras de A2 y explique el orden canónico. Use Σ = {b, a} en un ejemplo propio para demostrar el efecto del orden de entrada.
- Explique la poda con A4 y con el estado sumidero de A3. Relacione el recorrido inverso desde F con el descarte de prefijos.

## Ensayo conjunto

1. Inicien el servidor y abran el Módulo 2 antes de cargar un AFD. Comprueben el aviso.
2. Inventen un AFD de dos estados con alfabeto `b, a` y construyan la tabla desde el navegador.
3. Predigan a mano un resultado de cada módulo. Contrasten las predicciones con la interfaz.
4. Cambien el estado inicial o el conjunto de finales y repitan la comparación.
5. Descarguen el AFD, reinicien el servidor y vuelvan a cargar el archivo. Cada integrante explica por qué el AFD inicial se pierde y cómo el JSON permite recuperarlo.
6. Ejecuten `python -m pytest` y elijan una prueba que cada persona pueda explicar.
