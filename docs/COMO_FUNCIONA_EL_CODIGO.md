# Cómo funciona el código

## Correspondencia con la definición formal

| Concepto | Representación en `afd/automata.py` |
| --- | --- |
| Q | Lista `estados` en el orden ingresado |
| Σ | Lista `alfabeto` en el orden ingresado |
| δ | Diccionario `transiciones[(estado, simbolo)]` |
| q₀ | Cadena `estado_inicial` |
| F | Lista `estados_finales`, que puede estar vacía |

La tabla usa las filas de Q y las columnas de Σ. Cada celda es el destino del par correspondiente en el diccionario. El constructor de `AFD` verifica que cada par tenga destino en Q y que q₀ y F pertenezcan a Q. El lector de JSON detecta pares repetidos antes de crear el diccionario.

## Del formulario al AFD activo

1. `routes/main.py` recibe cada paso y llama a las validaciones de `afd/validator.py`. Solo avanza después de una respuesta válida.
2. `routes/borrador.py` mantiene los datos de trabajo. Cuando cambia Q o Σ, conserva las transiciones cuyos tres componentes siguen siendo válidos. El formulario marca las demás celdas para completarlas y solicita revisar q₀ o F si se eliminaron estados seleccionados.
3. El resumen crea una instancia validada. Al pulsar **Activar autómata**, `activar_afd` sustituye la referencia en `afd/estado_app.py` y limpia el historial.
4. Cada visita a los Módulos 2 y 3 obtiene esa referencia. Durante una edición, siguen utilizando el AFD que ya estaba activo hasta que se confirme el borrador.

## De δ a una gráfica

`afd/graph_dot.py` genera el texto DOT. Asigna identificadores internos como `n0` a los nodos, utiliza los nombres como etiquetas y agrupa símbolos que comparten origen y destino. La flecha de entrada sale de un punto invisible. Los nodos finales tienen forma de doble círculo.

La plantilla entrega ese DOT al navegador. `static/js/app.js` llama a Viz.js y añade el SVG a la página. A partir de `Resultado.pasos`, el Módulo 3 colorea los pares de estados recorridos y acumula los números de paso en cada flecha.

## Cómo explicarlo en clase

Señale una celda de la tabla, por ejemplo fila s1 y columna b. En A2, el diccionario devuelve `transiciones[("s1", "b")] == "s2"`. La misma relación aparece como flecha. Después cambie el destino desde la interfaz, active el AFD y consulte de nuevo la definición, las palabras y el recorrido.
