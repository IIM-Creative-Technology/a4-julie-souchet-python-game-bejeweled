from pygame import time, display

from src import screen
from src.GameObject import GameObject


class GameEngine:
    def __init__(self):
        self.objects = [
            GameObject("assets/red.png", (0, 0)),
            GameObject("assets/green.png", (50, 50)),
            GameObject("assets/yellow.png", (100, 100))
        ]
        screen.init()

    def tick(self):
        must_update = False
        for item in self.objects:
            must_update = item.move() or must_update

        if must_update:
            screen.draw_background()
            for item in self.objects:
                screen.draw_object(item)
            display.flip()

        time.wait(10)

    def draw_screen(self):
        screen.draw_background()
        for item in self.objects:
            screen.draw_object(item)
        display.flip()
