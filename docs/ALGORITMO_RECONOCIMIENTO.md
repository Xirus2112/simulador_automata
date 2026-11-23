# Reconocimiento y generación de palabras

## Reconocer una palabra

`AFD.procesar_palabra` aplica δ repetidamente desde q₀. Guarda el primer estado en `recorrido` y registra cada transición como una terna de origen, símbolo y destino. Si encuentra un carácter fuera de Σ, devuelve su posición y los pasos válidos anteriores. Al consumir toda la palabra, decide si el estado actual pertenece a F.

```text
actual ← q₀
recorrido ← [actual]
para cada símbolo y su posición en la palabra:
    si el símbolo está fuera de Σ:
        devolver rechazo, posición y recorrido parcial
    siguiente ← δ(actual, símbolo)
    registrar transición de actual a siguiente
    agregar siguiente al recorrido
    actual ← siguiente
devolver aceptación si actual ∈ F y el recorrido completo
```

Para A2 y `abab`:

| Paso | Estado actual | Símbolo | Estado siguiente |
| --- | --- | --- | --- |
| 1 | s0 | a | s1 |
| 2 | s1 | b | s2 |
| 3 | s2 | a | s1 |
| 4 | s1 | b | s2 |

El resultado es aceptación porque s2 ∈ F. Para ε, el ciclo se ejecuta cero veces y la comprobación se realiza sobre q₀.

## Enumerar hasta cinco palabras

1. Invierta las transiciones y recorra el grafo en anchura desde F. Así obtiene los estados desde los que es posible llegar a algún final.
2. Calcule `posibles[n]`, los estados con algún camino de exactamente n pasos hasta F. `posibles[0]` es F. Para cada n ≥ 1, un estado pertenece a ese nivel si alguna de sus transiciones llega a `posibles[n - 1]`.
3. Recorra las longitudes de 0 a 10. Para cada longitud, extienda un prefijo probando los símbolos en el orden de Σ. Conserve junto al prefijo el estado que alcanza. Si su destino no permite completar la longitud objetivo, omita esa extensión.
4. Compruebe las palabras completas con `procesar_palabra` y deténgase al obtener cinco.

La poda conserva el resultado de la búsqueda exhaustiva. Una palabra aceptada de longitud n siempre tiene, después de cualquier prefijo, un sufijo que llega a F en el número de pasos restantes. Los prefijos descartados carecen de ese sufijo. El orden se mantiene porque se recorren primero longitudes menores y en cada longitud se examinan los símbolos según Σ.

Para explicar el caso A4, distinga ambos recorridos en anchura. El recorrido inverso sale de F para hallar estados capaces de llegar a un final. El recorrido directo sale de q₀ para mostrar qué estados pueden visitarse. En A4, ambos conjuntos son disjuntos.
