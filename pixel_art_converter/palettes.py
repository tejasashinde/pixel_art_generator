# palettes.py

doom_palette = [
    (0,0,0),(31,31,31),(63,63,63),(95,95,95),(127,127,127),(159,159,159),(191,191,191),(223,223,223),
    (255,0,0),(255,63,63),(255,127,127),(255,191,191),(0,255,0),(63,255,63),(127,255,127),(191,255,191),
    (0,0,255),(63,63,255),(127,127,255),(191,191,255),(255,255,0),(255,255,63),(255,255,127),(255,255,191),
    (255,0,255),(255,63,255),(255,127,255),(255,191,255),(0,255,255),(63,255,255),(127,255,255),(191,255,255)
]

stardew_palette = [
    (91, 62, 44),(125, 87, 60),(160, 120, 80),
    (106, 190, 48),(76, 150, 40),(56, 102, 30),
    (64, 164, 223),(135, 206, 235),(176, 224, 230),
    (255, 99, 146),(255, 165, 0),(255, 215, 0),
    (34, 139, 34),(0, 100, 0),
    (140, 140, 140),(180, 180, 180),
    (210, 180, 140),(178, 34, 34),
    (255, 224, 189),(241, 194, 125),
    (45, 45, 45),(20, 20, 20),
    (255, 255, 255),(255, 250, 240),
    (255, 140, 0),(173, 216, 230),(144, 238, 144),(255, 182, 193),
    (200, 170, 120),(120, 200, 160),(80, 120, 200)
]

mario_palette = [
    (0, 0, 0),       # black / outline
    (255, 255, 255), # white / highlights
    (224, 64, 64),   # red (hat, shirt)
    (64, 64, 224),   # blue (overalls)
    (160, 128, 96),  # brown (shoes, hair)
    (255, 192, 160), # skin tone
    (128, 128, 128), # gray (shadow / background)
    (255, 255, 0),   # yellow (buttons / coins)
]

zelda_palette = [
    (0, 0, 0),        # black / outline
    (0, 128, 0),      # green (Link tunic)
    (160, 128, 64),   # brown (boots, belt)
    (255, 224, 160),  # skin tone
    (255, 255, 255),  # white (sword, highlights)
    (192, 192, 0),    # yellow (gold, rupees)
    (64, 64, 64),     # gray (weapons, background)
    (0, 128, 128),    # teal / water accents
]

contra_palette = [
    (0, 0, 0),         # black / outlines
    (255, 255, 255),   # white / highlights
    (192, 0, 0),       # red / main character outfit
    (0, 0, 192),       # blue / outfit or weapon
    (128, 128, 128),   # gray / weapons and metal
    (160, 128, 64),    # brown / hair, boots
    (255, 224, 160),   # skin tone
    (192, 192, 0),     # yellow / ammo or power-ups
    (0, 128, 0),       # green / background foliage
]


# Central registry of all palettes
PALETTES = {
    "doom": doom_palette,
    "stardew": stardew_palette,
    "mario": mario_palette,
    "zelda": zelda_palette,
    "contra": contra_palette,
}
