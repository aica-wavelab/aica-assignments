from otter.test_files import test_case

OK_FORMAT = False

name = "q75"
points = None

@test_case(points=None, hidden=False)
def test_get_artist(env):
    brit_artists = {
        "The Beatles": ["Yesterday", "Hey Jude", "Let it be", "Come Together"],
        "Queen": ["Bohemian Rhapsody", "We Will Rock You", "We Are The Champions", "Another One Bites The Dust"],
        "Elton John": ["Rocket man", "Your Song", "Tiny Dancer", "Crocodile Rock"],
        "David Bowie": ["Space Oddity", "Life on Mars", "Heroes", "Starman"],
        "The Rolling Stones": ["Paint it Black", "Sympathy for the Devil", "Gimme Shelter", "Angie"],
    }

    assert 'get_artist' in env, 'The function get_artist is not defined!'
    assert env['get_artist'](brit_artists, 'Bohemian Rhapsody') == 'Queen', \
        f'get_artist(brit_artists, "Bohemian Rhapsody") should return "Queen", but got {env["get_artist"](brit_artists, "Bohemian Rhapsody")}.'
    assert env['get_artist'](brit_artists, 'Space Oddity') == 'David Bowie', \
        f'get_artist(brit_artists, "Space Oddity") should return "David Bowie", but got {env["get_artist"](brit_artists, "Space Oddity")}.'
    assert env['get_artist'](brit_artists, 'Yesterday') == 'The Beatles', \
        f'get_artist(brit_artists, "Yesterday") should return "The Beatles", but got {env["get_artist"](brit_artists, "Yesterday")}.'

    try:
        env['get_artist'](brit_artists, 'Unknown Song')
        assert False, 'get_artist should raise a ValueError when the song is not found, but no exception was raised.'
    except ValueError:
        pass

