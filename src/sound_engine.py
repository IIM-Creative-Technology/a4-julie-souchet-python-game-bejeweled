from pygame import mixer


class SoundEngine:
    def __init__(self):
        mixer.init()
        self.sounds = {
            "delete": mixer.Sound("assets/sounds/sparkle.wav"),
            "win": mixer.Sound("assets/sounds/win.wav"),
            "lose": mixer.Sound("assets/sounds/lose.wav"),
            "impact": mixer.Sound("assets/sounds/impact.wav"),
        }

    def play(self, name: str):
        channel = mixer.find_channel()
        if channel is not None:
            channel.play(self.sounds.get(name))
