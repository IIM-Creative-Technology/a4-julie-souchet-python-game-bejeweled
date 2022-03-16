from pygame import mixer


class SoundEngine:
    def __init__(self):
        mixer.init()
        self.sounds = {
            "delete": mixer.Sound("assets/sparkle.wav"),
            "win": mixer.Sound("assets/win.wav"),
            "impact": mixer.Sound("assets/impact.wav"),
        }

    def play(self, name: str):
        mixer.find_channel().play(self.sounds.get(name))
