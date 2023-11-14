import os
import random
from typing import List
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()

def load_sound(file):
    """because pygame can be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print(f"Warning, unable to load, {file}")
    return None

class Player(pg.sprite.Sprite):
    """0 for idle, 1 for moving, 2 for jumping"""
    images: List[pg.Surface] = []

    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1
        # print("hello madafaka")

    def move(self):
        """actually move the background"""
        self.image = self.images[1]
        print("moving")
    
    def jump(self):
        """move upward and downward"""
        self.image = self.images[2]
        print("jumping")

SCREENRECT = pg.Rect(0, 0, 1280, 720)
    
clock = pg.time.Clock()
running = True
pg.init()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    """screen setup"""
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pg.display.flip()
    """resource initiazation after screen setup"""
    Player.images = [load_image(im) for im in ("idle.jpg", "move.jpg", "jump.jpg")]
    """set player """
    all = pg.sprite.RenderUpdates()
    player = Player(all)

    # draw the elements
    dirty = all.draw(screen)
    pg.display.update(dirty)
    clock.tick(30)

pg.quit()