default nivel = 1
default patron = ["verde", "verde", "azul"]
default progreso = 0               # cuántos pasos correctos del patrón llevamos
default orden_puertas = ["verde", "roja", "azul"]  # se baraja en cada nivel

default gather = False          
default gather_dur = 0.35        
default gather_pause = 0.20


init python:
    import random
    from renpy.display.im import MatrixColor, matrix

    SCAMPI  = "#4e4b7c"
    SCAMPI_DARK = "#3a3760"      # un poco más oscuro para fondos/transiciones
    SCAMPI_T = "#4e4b7ccc"       # translúcido para paneles
    SAFFRON = "#f6c042"
    MISCHKA = "#cacadb"

    def generar_patron(longitud=5):
        colores = ["verde", "roja", "azul"]
        return [random.choice(colores) for _ in range(longitud)]

    def barajar_puertas_animado(pausa=0.20, dur=0.35):
        store.gather = True
        store.gather_dur = dur
        store.gather_pause = pausa
        renpy.restart_interaction()

    def _do_shuffle():
        random.shuffle(store.orden_puertas)
        store.gather = False
        renpy.restart_interaction()

    def elegir_puerta(color):
        global progreso, nivel
        paso_correcto = patron[progreso]

        if color == paso_correcto:
            progreso += 1
            nivel += 1
            renpy.play("heal.mp3", channel="sound")
            barajar_puertas_animado()

            renpy.show("flash_ok", at_list=[flash_pulse], layer="transient")
            renpy.show_screen("toast", msg="¡Correcto!", kind="ok")
            renpy.transition(Dissolve(0.12)) 

            if progreso == len(patron):
                progreso = 0
                renpy.restart_interaction()  # refresca la UI

                # ¿Ganaste?
                if nivel >= 20:
                    store.gather = False          # por las dudas, que no anime más
                    renpy.show_screen("final_ganaste")
                    return                        # IMPORTANTE: no sigas barajando
                else:
                    # Seguir jugando normalmente
                    barajar_puertas_animado()
                    renpy.show_screen("toast", msg="¡Nivel {}!".format(nivel), kind="ok")
                    renpy.transition(Dissolve(0.12))
            
        else:
            # Error: reset total
            renpy.show("flash_error", at_list=[flash_pulse], layer="transient")
            renpy.show_screen("toast", msg="Patrón incorrecto", kind="error")
            renpy.transition(hpunch)
            renpy.play("hit.mp3", channel="sound")

            nivel = 1
            progreso = 0
            barajar_puertas_animado()
            renpy.restart_interaction()

    def tint_matrix(r, g, b, bright=0.0):
        m = matrix.saturation(0.0) * matrix.tint(r, g, b)
        if bright != 0.0:
            m = m * matrix.brightness(bright)
        return m




screen toast(msg, kind="ok"):
    zorder 100
    frame:
        align (0.5, 0.18)
        padding (24, 14)
        background Solid("#3a3760CC")    # panel oscuro scampi
        $ toast_color = SAFFRON if kind=="ok" else "#e74c3c"
        text msg size 48 color toast_color outlines [(2, "#000000")]
    timer 1.2 action Hide("toast")

screen hud_nivel():
    frame:
        background Solid("#4e4b7ccc")    # panel scampi translúcido
        xfill True
        yalign 0.02
        padding (12, 10)

        fixed:
            xfill True
            ysize 60

            text "Nivel: [nivel]" size 38 xalign 0.02 yalign 0.5 color MISCHKA
            textbutton "Reiniciar":
                xalign 0.80
                yalign 0.5
                xpadding 14
                ypadding 8
                text_color SAFFRON
                action Jump("start")

            $ marcados = ["✓" if i < progreso else "•" for i in range(len(patron))]
            text "Progreso: [\" \".join(marcados)]" size 28 xalign 0.98 yalign 0.5 color MISCHKA


image flash_ok    = Solid("#2ecc71AA")
image flash_error = Solid("#e74c3cAA")
image bg_menu = im.Scale("bg_menu.png", config.screen_width, config.screen_height)
image bg_game = im.Scale("bg_game.png", config.screen_width, config.screen_height)
image door_base = "door.png"

# Oscurece un poco el fondo amarillo para dar contraste a la UI
image bg_tint   = Solid("#2e2b5450")    # scampi bien translúcido (B=~0.73 alpha)
image bg_tint_l = Solid("#2e2b5451")    # versión un poco más liviana por si querés

# --- VARIANTES IDLE ---
image door_green = MatrixColor("door.png", tint_matrix(0.18, 0.99, 0.24))
image door_red   = MatrixColor("door.png", tint_matrix(0.99, 0.10, 0.13))
image door_blue  = MatrixColor("door.png", tint_matrix(0.10, 0.10, 0.96))

# --- VARIANTES HOVER  ---
image door_green_hover = MatrixColor("door.png", tint_matrix(0.18, 0.99, 0.24, bright=0.08))
image door_red_hover   = MatrixColor("door.png", tint_matrix(0.99, 0.10, 0.13, bright=0.08))
image door_blue_hover  = MatrixColor("door.png", tint_matrix(0.10, 0.10, 0.96, bright=0.08))

transform flash_pulse:
    alpha 0.0
    linear 0.05 alpha 1.0
    linear 0.20 alpha 0.0

transform hover_grow:
    on hover:
        linear 0.12 zoom 1.03
    on idle:
        linear 0.12 zoom 1.00

transform press_pop:
    linear 0.08 zoom 0.96
    linear 0.10 zoom 1.00

transform move_door(xa=0.5, ya=0.62, dur=0.35):
    easein dur xalign xa yalign ya
    on reached:
        linear 0.07 zoom 1.02
        linear 0.07 zoom 1.00

transform door_scale(z=0.65):
    zoom z

screen puertas():
    use hud_nivel

    frame:
        align (0.5, 0.55)
        padding (40, 40)
        xsize 0.92
        ysize 0.65
        background None

        # Cuando estamos “juntando”, tras dur+pausa barajamos y soltamos
        if gather:
            timer gather_dur + gather_pause action Function(_do_shuffle)

        # Posiciones destino cuando NO estamos en gather (separadas)
        $ slots = (0.15, 0.50, 0.85)  

        fixed:
            xfill True
            yfill True

        # Dibujamos las puertas según el orden actual
        # i: índice en el orden barajado
        for i, color in enumerate(orden_puertas):

            # Elegir la variante de imagen según el color (idle/hover)
            if color == "verde":
                $ idle_img  = "door_green"
                $ hover_img = "door_green_hover"
            elif color == "roja":
                $ idle_img  = "door_red"
                $ hover_img = "door_red_hover"
            else:
                $ idle_img  = "door_blue"
                $ hover_img = "door_blue_hover"

            # Destino X: si estamos juntando -> centro; si no -> slot por índice
            $ target_x = 0.5 if gather else slots[i]

            imagebutton:
                idle idle_img
                hover hover_img
                at [door_scale(0.62), move_door(target_x, 0.62, gather_dur), hover_grow]
                focus_mask True
                sensitive (not gather)
                action Function(elegir_puerta, color)



screen final_ganaste():
    modal True
    zorder 200
    frame:
        align (0.5, 0.5)
        padding (32, 24)
        background Solid("#4e4b7ccc")
        vbox:
            spacing 20
            text "¡Ganaste!" size 56 color SAFFRON outlines [(3, "#000000")]
            text "¡Felicidades por aplicar patrones para resolver el camino correcto!" size 28 color MISCHKA
            textbutton "Reiniciar":
                action [Hide("final_ganaste"), Jump("start")]
                xpadding 22 ypadding 12
                text_color SAFFRON



# Muestra un fondo opcional + título y cuerpo opcionales.
# Un click (o Enter/Espacio) retorna al label que lo llamó.
screen click_anywhere(bg=None, title=None, body=None, show_hint=True):
    if bg:
        add bg

    if title:
        text title:
            align (0.5, 0.22)
            size 54
            color SCAMPI 
            outlines [(3, "#00000088")]
            at fadein_quick

    if body:
        text body:
            align (0.5, 0.55)
            xmaximum int(config.screen_width * 0.75)
            size 30
            line_spacing 4
            color MISCHKA
            outlines [(2, "#00000066")]
            at fadein_quick

    # capa invisible que capta cualquier click
    button:
        background None
        xfill True
        yfill True
        action Return(True)

    # teclado también
    key "K_RETURN" action Return(True)
    key "K_SPACE"  action Return(True)
    key "mouseup_1" action Return(True)


transform fadein_quick:
    alpha 0.0
    linear 0.25 alpha 1.0

transform blink_hint:
    alpha 1.0
    linear 0.8 alpha 0.35
    linear 0.8 alpha 1.0
    repeat



label start:

    play music "bgn.mp3" loop

    $ patron = generar_patron(5)
    $ nivel = 1
    $ progreso = 0

    $ barajar_puertas_animado()

    # 1) Pantalla de menú con fondo de inicio
    scene bg_menu
    with fade
    call screen click_anywhere(
        bg=None,                    # ya hicimos scene bg_menu arriba
        title=None,
        body=None
    )

    # 2) Mini tutorial (podés usar bg_game o dejar el bg_menu)
    scene bg_game
    show bg_tint
    with dissolve
    call screen click_anywhere(
        bg=None,                    # ya hicimos scene bg_game arriba
        title="¿Cómo se juega?",
        body="Tenés tres puertas. Para avanzar niveles seguí el patrón:\n\nEjemplo: Verde → Verde → Azul → Rojo → Rojo.\n\nSi te equivocás, volvés al nivel 1. En cada nivel las puertas cambian de lugar.\n\n¡Probá repetir el patrón para subir!"
    )

    # 3) Entrar al juego (pantalla de puertas)
    call screen puertas
    return

    



