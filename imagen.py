from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import textwrap

# Área donde irá el texto
ANCHO_CAJA = 1000
ALTO_CAJA = 500

X_CAJA = 120
Y_CAJA = 350


def obtener_fuente(tamano):
    """
    Carga una fuente bold.
    """

    try:
        return ImageFont.truetype(
            "arialbd.ttf",
            tamano
        )

    except:
        try:
            return ImageFont.truetype(
                "Arial Bold.ttf",
                tamano
            )
        except:
            return ImageFont.load_default()


def crear_imagen(numero, texto):

    imagen = Image.open("fondo.png")

    draw = ImageDraw.Draw(imagen)

    # ==========================
    # MAYÚSCULAS
    # ==========================

    texto = texto.upper()

    # ==========================
    # NÚMERO DE CONFESIÓN
    # ==========================

    fuente_numero = obtener_fuente(34)

    draw.text(
        (323, 397),
        str(numero),
        fill="white",
        font=fuente_numero
    )

    # ==========================
    # AJUSTE AUTOMÁTICO
    # ==========================

    tamano_fuente = 60

    while tamano_fuente > 20:

        fuente_texto = obtener_fuente(
            tamano_fuente
        )

        ancho_maximo = max(
            20,
            int(
                42 - (
                    (60 - tamano_fuente) * 0.8
                )
            )
        )

        lineas = textwrap.wrap(
            texto,
            width=ancho_maximo
        )

        texto_envuelto = "\n".join(
            lineas
        )

        bbox = draw.multiline_textbbox(
            (0, 0),
            texto_envuelto,
            font=fuente_texto,
            spacing=14
        )

        ancho_texto = bbox[2] - bbox[0]
        alto_texto = bbox[3] - bbox[1]

        if (
            ancho_texto <= ANCHO_CAJA
            and
            alto_texto <= ALTO_CAJA
        ):
            break

        tamano_fuente -= 2

    # ==========================
    # CENTRADO
    # ==========================

    x = X_CAJA + (
        (ANCHO_CAJA - ancho_texto) / 2
    )

    y = Y_CAJA + (
        (ALTO_CAJA - alto_texto) / 2
    )

    # ==========================
    # NEGRITA REFORZADA
    # ==========================

    for dx, dy in [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]:

        draw.multiline_text(
            (x + dx, y + dy),
            texto_envuelto,
            font=fuente_texto,
            fill="white",
            align="center",
            spacing=14
        )

    draw.multiline_text(
        (x, y),
        texto_envuelto,
        font=fuente_texto,
        fill="white",
        align="center",
        spacing=14
    )

    # ==========================
    # GUARDAR
    # ==========================

    ruta = f"generadas/confesion_{numero}.png"

    imagen.save(ruta)

    return ruta