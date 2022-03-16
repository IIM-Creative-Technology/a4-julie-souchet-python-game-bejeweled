from pygame import mixer


class SoundEngine:
    def __init__(self):
        mixer.init()
        self.sounds = {
            "delete": mixer.Sound("assets/sparkle.wav"),
            "win": mixer.Sound("assets/win.wav"),
            "lose": mixer.Sound("assets/lose.wav"),
            "impact": mixer.Sound("assets/impact.wav"),
        }

    def play(self, name: str):
        channel = mixer.find_channel()
        if channel is not None:
            channel.play(self.sounds.get(name))
