import os, textwrap, json
from pilmoji import Pilmoji
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, ImageOps
from typing import TYPE_CHECKING
from ballsdex.core.models import Regime, Economy

if TYPE_CHECKING:
    from ballsdex.core.models import BallInstance


SOURCES_PATH = Path(os.path.dirname(os.path.abspath(__file__)), "./src")
WIDTH = 1500
HEIGHT = 2000

RECTANGLE_WIDTH = WIDTH - 40
RECTANGLE_HEIGHT = (HEIGHT // 5) * 2

CORNERS = ((34, 261), (1393, 992))
artwork_size = [b - a for a, b in zip(*CORNERS)]

title_font = ImageFont.truetype(str(SOURCES_PATH / "ArsenicaTrial-Extrabold.ttf"), 170)
capacity_name_font = ImageFont.truetype(str(SOURCES_PATH / "Bobby Jones Soft.otf"), 110)
capacity_description_font = ImageFont.truetype(str(SOURCES_PATH / "OpenSans-Semibold.ttf"), 75)
stats_font = ImageFont.truetype(str(SOURCES_PATH / "Bobby Jones Soft.otf"), 130)
credits_font = ImageFont.truetype(str(SOURCES_PATH / "arial.ttf"), 40)

f = open(SOURCES_PATH / "flags.json")
FLAGS = json.loads(f.read())
f.close()

async def draw_card(ball_instance):
    ball = ball_instance.countryball
    ball_health = (237, 115, 101, 255)
    regime: Regime = await ball.cached_regime
    economy: Economy = await ball.cached_economy

    if ball_instance.shiny:
        image = Image.open(str(SOURCES_PATH / "shiny.png"))
        ball_health = (255, 255, 255, 255)
    elif special_image := ball_instance.special_card:
        image = Image.open("." + special_image)
    else:
        image = Image.open("." + regime.background)
    icon = Image.open("." + economy.icon) if economy else None

    draw = ImageDraw.Draw(image)
    draw.text((50, 20), ball.short_name or ball.country, font=title_font)
    for i, line in enumerate(textwrap.wrap(f"Ability: {ball.capacity_name}", width=28)):
        draw.text(
            (100, 1050 + 100 * i),
            line,
            font=capacity_name_font,
            fill=(230, 230, 230, 255),
            stroke_width=2,
            stroke_fill=(0, 0, 0, 255),
        )
    for i, line in enumerate(textwrap.wrap(ball.capacity_description, width=33)):
        draw.text(
            (60, 1300 + 60 * i),
            line,
            font=capacity_description_font,
            stroke_width=1,
            stroke_fill=(0, 0, 0, 255),
        )
    draw.text(
        (320, 1670),
        str(ball_instance.health),
        font=stats_font,
        fill=ball_health,
        stroke_width=1,
        stroke_fill=(0, 0, 0, 255),
    )
    draw.text(
        (960, 1670),
        str(ball_instance.attack),
        font=stats_font,
        fill=(252, 194, 76, 255),
        stroke_width=1,
        stroke_fill=(0, 0, 0, 255),
    )
    draw.text(
        (30, 1870),
        "Made on Planet Earth by Pantonian Coders. Visit Pantonia!\n" f"Artist(s): {ball.credits}",
        font=credits_font,
        fill=(0, 0, 0, 255),
        stroke_width=0,
        stroke_fill=(255, 255, 255, 255),
    )

    artwork = Image.open("." + ball.collection_card)
    image.paste(ImageOps.fit(artwork, artwork_size), CORNERS[0])

    if icon:
        icon = ImageOps.fit(icon, (192, 192))
        image.paste(icon, (1200, 30), mask=icon)
        icon.close()
    artwork.close()

    try:
        pilmoji = Pilmoji(image)
        pilmoji.text((1240,1860), FLAGS[ball.location], (0,0,0), capacity_name_font)
    except KeyError:
        pilmoji.text((1240,1860), FLAGS["N/A"], (0,0,0), capacity_name_font)

    return image
