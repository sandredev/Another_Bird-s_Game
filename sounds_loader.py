from sound import Sounds

class Sounds_loader:
    def __init__(self):
        self.sounds = Sounds()
        music_dict = {
            'main_menu': "sound/musics/main_menu.mp3"}
        sfx_dict = {
            'jump': "sound/effects/jump.mp3",
            'tube': "sound/effects/tube.mp3",
            'hit': "sound/effects/skill_issue.mp3",
            'game_over': "sound/effects/game_over.mp3"}

        self.sounds.set_music(music_dict)
        self.sounds.set_sfx(sfx_dict)

