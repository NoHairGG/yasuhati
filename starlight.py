import pyaudio
import numpy
import audioop
import os
import random
import math
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

    def rest(self):
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        #print("resting")

    def move(self):
        """actually move the background"""
        self.image = self.images[1]
        print("moving")

    def jump(self):
        """show state change"""
        self.image = self.images[2]
        print("jumping")

    def jump_volume(self, value):
        """move upward and downward"""
        self.image = self.images[2]
        self.rect.top = 684 - (value / 20)
        print("jumping")

SCREENRECT = pg.Rect(0, 0, 1280, 720)
    
def main(winstyle=0):
    """audio input setup"""
    pa = pyaudio.PyAudio()
    stream = pa.open(format = pyaudio.paInt16,channels=1,rate=44100,input_device_index=3,input=True)
    """program flow"""
    clock = pg.time.Clock()
    scroll = 0
    running = True
    pg.init()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        """display setup"""
        winstyle = 0  #full screen
        bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
        # pg.display.flip()
        """resource initiazation after screen setup"""
        Player.images = [load_image(im) for im in ("idle.jpg", "move.jpg", "jump.jpg")]
        # create the background, tile the bgd image
        bgdtile = load_image("background.jpg")
        # background = pg.Surface(SCREENRECT.size)
        # for x in range(0 , SCREENRECT.width, bgdtile.get_width()):
        #     background.blit(bgdtile, (x, 0))
        #screen.blit(bgdtile, (0, 0))
        tiles = math.ceil(720 / bgdtile.get_width()) + 1
        pg.display.update()
        """set player """
        all = pg.sprite.RenderUpdates()
        player = Player(all)
        while player.alive():
            clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
            keystate = pg.key.get_pressed()
            jump = keystate[pg.K_SPACE]
            # print(jump)
            if jump:
                player.jump()
            # check volume
            raws=stream.read(1024, exception_on_overflow = False)
            samples=numpy.frombuffer(raws, dtype=numpy.int16)
            numpy.set_printoptions(threshold=numpy.inf)
            rms = audioop.rms(samples, 2)
            # print(rms)
            if rms > 1000:
                player.jump_volume(rms)
            else:
                player.rest()
            # scroll da background
            i = 0
            while(i < tiles): 
                screen.blit(bgdtile, (bgdtile.get_width()*i + scroll, 0)) 
                i += 1
            scroll -= 6
            if abs(scroll) > bgdtile.get_width():
                scroll = 0
            print(scroll)
            pg.display.flip()
            # clear/erase the last drawn sprites
            all.clear(screen, bgdtile)
            # update all the sprites
            all.update()
            dirty = all.draw(screen)
            pg.display.update(dirty) 
        # draw the elements

# call the "main" function
if __name__ == "__main__":
    main()
    pg.quit()