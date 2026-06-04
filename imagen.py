from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import textwrap
import os

# =====================================
# ZONA DEL TEXTO
# =====================================

ANCHO_CAJA = 820
ALTO_CAJA = 520

X_CAJA = 130
Y_CAJA = 300


def obtener_fuente(tamano):

    ruta_fuente = os.path.join(
        os.path.dirname(__file__),
        "fuentes",
        "Anton-Regular.ttf"
    )

    print(f"RUTA FUENTE: {ruta_fuente}")
    print(f"EXISTE FUENTE: {os.path.exists(ruta_fuente)}")

    fuente = ImageFont.truetype(
        ruta_fuente,
        tamano
    )

    return fuente


def crear_imagen(numero, texto):

    print("========== DEBUG ==========")

    print("ARCHIVOS RAIZ:")
    print(os.listdir("."))

    if os.path.exists("fuentes"):
        print("ARCHIVOS FUENTES:")
        print(os.listdir("fuentes"))

    print("===========================")

    imagen = Image.open("fondo.png").convert("RGB")

    draw = ImageDraw.Draw(imagen)

    texto = texto.upper()

    # =====================================
    # NUMERO DE CONFESION
    # =====================================

    fuente_numero = obtener_fuente(44)

    draw.text(
        (285, 388),
        str(numero),
        fill="white",
        font=fuente_numero
    )

    # =====================================
    # AJUSTE AUTOMATICO
    # =====================================

    tamano_fuente = 60

    while tamano_fuente >= 30:

        fuente_texto = obtener_fuente(
            tamano_fuente
        )

        lineas = textwrap.wrap(
            texto,
            width=18
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

        tamano_fuente -= 5

    print(
        f"TAMAÑO FINAL DE FUENTE: {tamano_fuente}"
    )

    x = X_CAJA + (
        (ANCHO_CAJA - ancho_texto) / 2
    )

    y = Y_CAJA + (
        (ALTO_CAJA - alto_texto) / 2
    )

    # =====================================
    # TEXTO
    # =====================================

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

    os.makedirs(
        "generadas",
        exist_ok=True
    )

    ruta = (
        f"generadas/confesion_{numero}.png"
    )

    imagen.save(ruta)

    return ruta