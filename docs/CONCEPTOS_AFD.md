# Conceptos de autómatas finitos deterministas

Un AFD lee una palabra de izquierda a derecha. En cada momento está en un solo estado. Con el estado actual y el siguiente símbolo se determina el destino de forma única.

## La 5-tupla

`M = (Q, Σ, δ, q₀, F)`

| Elemento | Significado | Ejemplo A2 |
| --- | --- | --- |
| Q | Conjunto finito de estados | {s0, s1, s2} |
| Σ | Alfabeto de símbolos | {a, b} |
| δ | Función de transición Q × Σ → Q | δ(s1, b) = s2 |
| q₀ | Estado desde el que se empieza a leer | s0 |
| F | Conjunto de estados de aceptación, con F ⊆ Q | {s2} |

El AFD es completo cuando δ está definida para todos los pares de Q × Σ. Con tres estados y dos símbolos, δ necesita seis destinos. Un estado sumidero puede servir para completar la tabla. En A3, `m` recibe las transiciones descartadas y tiene bucles para todo Σ.

## Palabras, aceptación y rechazo

Una palabra es una secuencia finita de símbolos de Σ. `ab` y `ba` son distintas porque sus símbolos se leen en distinto orden. `ε` denota la palabra vacía y tiene longitud cero.

La palabra se acepta si el estado al terminar pertenece a F. Para A2, el recorrido de `ab` es s0 → s1 → s2 y s2 ∈ F. Con `aba`, el último estado es s1 y se rechaza. Si un carácter está fuera de Σ, la lectura se detiene en ese carácter y la entrada se rechaza.

ε deja al autómata en q₀ y se acepta exactamente cuando q₀ ∈ F. En A1 el estado inicial es final, por eso acepta ε. En A2, s0 no es final y ε se rechaza.

## Alcanzabilidad

Un estado es alcanzable si existe una palabra cuyo recorrido llega a él desde q₀. El conjunto de estados alcanzables incluye q₀ por el recorrido de ε. Si F está vacío, toda palabra se rechaza. Si F tiene estados y ninguno es alcanzable, el lenguaje también es vacío. A4 ilustra este último caso con q0 alcanzable y q1 final pero inaccesible desde q0.
