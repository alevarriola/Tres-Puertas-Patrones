# Tres Puertas – Juego de Patrones (Ren'Py)

Pequeño minijuego de **patrones y toma de decisiones** creado con **Ren'Py**, pensado como recurso para trabajar **pensamiento computacional** (patrones, memoria, prueba y error) en clase o como juego casual de navegador.

> El juego está publicado y disponible online en itch.io:  
> **https://alevarriola.itch.io/tres-puertas**

---

## Descripción general

En **Tres Puertas** el jugador se encuentra frente a **tres puertas de colores** (verde, roja y azul).  
En cada nivel existe un **patrón secreto de colores** (por ejemplo: verde → verde → azul) y el objetivo es:

1. **Descubrir** el patrón.
2. **Repetirlo correctamente**, clickeando las puertas en el orden indicado.
3. **Subir de nivel** a medida que se completa el patrón.
4. Alcanzar el nivel final para ver la pantalla de **“¡Ganaste!”**.

Las puertas **cambian de lugar** en cada barajado, así que el jugador debe concentrarse en el **color** y no en la posición.  
Hay un máximo de **20 niveles**, con feedback visual y mensajes que refuerzan el uso de patrones.

---

## Mecánicas principales

- **Tres puertas de colores**: verde, roja y azul.
- **Patrón de colores**:
  - Se genera con `generar_patron(longitud=5)` al comienzo de la partida.
  - El patrón es una lista de colores (p. ej. `["verde", "roja", "azul", ...]`).
- **Progreso del patrón**:
  - Variable `progreso` indica cuántos pasos del patrón se hicieron bien.
  - En el HUD se muestra una fila de puntos que se convierten en “✓” a medida que se avanza.
- **Barajado de puertas**:
  - Lista `orden_puertas = ["verde", "roja", "azul"]` se mezcla en cada ronda.
  - Animación de “juntarse y soltarse” usando la variable `gather` para darle dinamismo.
- **Niveles**:
  - Variable `nivel` empieza en 1 y va aumentando.
  - Al completar correctamente el patrón:
    - Se resetea `progreso`.
    - Se muestra un “toast” de **¡Nivel X!**.
    - Se vuelve a barajar y el juego continúa.
  - Al llegar al nivel 20 se muestra la pantalla `final_ganaste`.
- **Feedback visual y sonoro**:
  - `flash_ok` y `flash_error` para mostrar flashes de color sobre la pantalla.
  - Sonidos en `audio/` (`heal.mp3`, `hit.mp3`) para reforzar aciertos/errores.
  - Música de fondo `bgn.mp3` en loop.

---

## Enfoque educativo

Este proyecto está pensado para trabajar:

- **Reconocimiento de patrones**: seguir una secuencia de colores.
- **Memoria de trabajo**: recordar el patrón a través de varios intentos.
- **Abstracción**: enfocarse en el color y no en la posición física de la puerta.
- **Tolerancia al error**: cometer errores, recibir feedback inmediato y volver a intentar.

Es ideal para:

- Talleres de **Pensamiento Computacional**.
- Clases introductorias de **lógica** o **diseño de juegos**.
- Mostrar a estudiantes cómo un proyecto pequeño puede tener:
  - Variables de estado.
  - HUD con información útil.
  - Animaciones y feedback visual.

---

## Stack técnico

- **Engine:** [Ren'Py](https://www.renpy.org/) (motor para novelas visuales y juegos narrativos).
- **Lenguaje:** Lenguaje de scripts de Ren'Py + Python embebido.
- **Assets:**
  - Imágenes en `game/images/` (`bg_game.png`, `bg_menu.png`, `door.png`).
  - GUI personalizada en `game/gui/` (botones, barras, scrollbars).
  - Audio en `game/audio/`.
- **Paleta de colores propia**, definida en `script.rpy`:
  - `SCAMPI`, `SAFFRON`, `MISCHKA`, etc., para lograr un estilo consistente.

---

## Estructura del proyecto

```text
Tres-Puertas-Patrones-main/
├─ project.json           # Configuración del proyecto Ren'Py
└─ game/
   ├─ script.rpy          # Lógica del juego, pantallas personalizadas y mecánicas
   ├─ options.rpy         # Nombre del juego, build.name, opciones básicas
   ├─ screens.rpy         # Screens base del GUI de Ren'Py
   ├─ gui.rpy             # Configuración visual y estilos
   ├─ bgn.mp3             # Música de fondo
   ├─ audio/              # Efectos de sonido (hit, heal, etc.)
   ├─ images/             # Fondos y sprite de puerta
   ├─ gui/                # Elementos gráficos de la interfaz
   ├─ libs/               # Librerías adicionales (si aplica)
   └─ tl/                 # Carpeta de traducciones (plantilla)
```

---

## ▶️ Cómo jugar

### Opción 1 – Directo en la web

La forma más simple es jugarlo desde itch.io:

> **Tres Puertas en itch.io:**  
> https://alevarriola.itch.io/tres-puertas

No requiere instalación, solo un navegador moderno.

---

### Opción 2 – Ejecutar localmente con Ren'Py

1. **Descargar Ren'Py** desde la página oficial.
2. Abrir el **Ren'Py Launcher**.
3. En “Open Project”, seleccionar la carpeta del proyecto  
   `Tres-Puertas-Patrones-main/`.
4. Elegir **“Launch Project”** para ejecutar el juego.
5. Opcional: desde el launcher también se pueden generar builds:
   - Windows / Linux / macOS.
   - Web (HTML5), si tenés configurado el toolchain.

---

## Ideas de uso en clase

- Pedir a los estudiantes que:
  - Cambien la longitud del patrón (`generar_patron(longitud=…)`).
  - Modifiquen la cantidad máxima de niveles.
  - Ajusten los colores o agreguen un cuarto color.
- Proponer variantes:
  - Patrones que crecen en cada nivel.
  - Penalizaciones de tiempo o intentos.
  - Indicadores de “racha” de aciertos.

---

## Autor

**Alejandro Arriola**  
Docente de programación y desarrollador de experiencias educativas jugables en constante formación.

- Itch.io: https://alevarriola.itch.io
- GitHub: [@alevarriola](https://github.com/alevarriola)
