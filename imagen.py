from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import textwrap
import os

# ======================================
# ÁREA DE TEXTO
# ======================================

ANCHO_CAJA = 820
ALTO_CAJA = 520

X_CAJA = 130
Y_CAJA = 300


def obtener_fuente(tamano):

    try:
        return ImageFont.truetype(
            "fuentes/Anton-Regular.ttf",
            tamano
        )

    except Exception as e:

        print(f"ERROR CARGANDO FUENTE: {e}")

        return ImageFont.load_default()


def crear_imagen(numero, texto):

    imagen = Image.open("fondo.png").convert("RGB")

    draw = ImageDraw.Draw(imagen)

    # ======================================
    # TEXTO EN MAYÚSCULAS
    # ======================================

    texto = texto.upper()

    # ======================================
    # NÚMERO DE CONFESIÓN
    # ======================================

    fuente_numero = obtener_fuente(42)

    draw.text(
        (300, 388),
        str(numero),
        fill="white",
        font=fuente_numero
    )

    # ======================================
    # AJUSTE AUTOMÁTICO DE FUENTE
    # ======================================

    tamano_fuente = 90

    while tamano_fuente >= 30:

        fuente_texto = obtener_fuente(
            tamano_fuente
        )

        ancho_wrap = max(
            12,
            int(26 - ((90 - tamano_fuente) * 0.25))
        )

        lineas = textwrap.wrap(
            texto,
            width=ancho_wrap
        )

        texto_envuelto = "\n".join(
            lineas
        )

        bbox = draw.multiline_textbbox(
            (0, 0),
            texto_envuelto,
            font=fuente_texto,
            spacing=18,
            align="center"
        )

        ancho_texto = bbox[2] - bbox[0]
        alto_texto = bbox[3] - bbox[1]

        if (
            ancho_texto <= ANCHO_CAJA
            and
            alto_texto <= ALTO_CAJA
        ):
            break

        tamano_fuente -= 4

    # ======================================
    # CENTRADO
    # ======================================

    x = X_CAJA + (
        (ANCHO_CAJA - ancho_texto) / 2
    )

    y = Y_CAJA + (
        (ALTO_CAJA - alto_texto) / 2
    )

    # ======================================
    # EFECTO NEGRITA
    # ======================================

    for dx, dy in [
        (-2, 0),
        (2, 0),
        (0, -2),
        (0, 2),
        (-1, -1),
        (1, 1),
        (-1, 1),
        (1, -1)
    ]:

        draw.multiline_text(
            (x + dx, y + dy),
            texto_envuelto,
            font=fuente_texto,
            fill="white",
            align="center",
            spacing=18
        )

    draw.multiline_text(
        (x, y),
        texto_envuelto,
        font=fuente_texto,
        fill="white",
        align="center",
        spacing=18
    )

    # ======================================
    # GUARDAR
    # ======================================

    os.makedirs(
        "generadas",
        exist_ok=True
    )

    ruta = f"generadas/confesion_{numero}.png"

    imagen.save(
        ruta,
        quality=95
    )

    return ruta