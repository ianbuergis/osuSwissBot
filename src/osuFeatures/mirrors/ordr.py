import requests

class Ordr:

    session: requests.Session

    defaultGetParameter: dict = {
        'replayFile': None,
        'username': None,
        'customSkin': False,
        'resolution': '1920x1080',
        'globalVolume': 50,
        'musicVolume': 50,
        'hitsoundVolume': 50,
        'useSkinHitsounds': False,
        'playNightcoreSamples': True,
        'showHitErrorMeter': True,
        'showScore': True,
        'showHPBar': True,
        'showComboCounter': True,
        'showPPCounter': True,
        'showKeyOverlay': True,
        'showScoreboard': True,
        'showAvatarsOnScoreboard': True,
        'showBorders': False,
        'showMods': True,
        'showResultScreen': True,
        'showHitCounter': True,
        'showSliderBreaks': True,
        'showAimErrorMeter': True,
        'showStrainGraph': False,
        'useSkinCursor': True,
        'useSkinColors': True,
        'useBeatmapColors': False,
        'cursorScaleToCS': False,
        'cursorRainbow': False,
        'cursorTrailGlow': False,
        'drawFollowPoints': True,
        'scaleToTheBeat': False,
        'sliderMerge': False,
        'objectsRainbow': False,
        'objectsFlashToTheBeat': False,
        'useHitCircleColor': True,
        'seizureWarning': False,
        'loadStoryboard': True,
        'loadVideo': True,
    }
    def __init__(self):
        self.session = requests.session()

    async def authenticate(self):
        self.session.get('https://account.issou.best/login/osu?redirect=https://ordr.issou.best')




