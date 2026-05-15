from otter.test_files import test_case

OK_FORMAT = False

name = "q74"
points = None

@test_case(points=None, hidden=False)
def test_get_songs(env):
    brit_artists = {
        "The Beatles": ["Yesterday", "Hey Jude", "Let it be", "Come Together"],
        "Queen": ["Bohemian Rhapsody", "We Will Rock You", "We Are The Champions", "Another One Bites The Dust"],
        "Elton John": ["Rocket man", "Your Song", "Tiny Dancer", "Crocodile Rock"],
        "David Bowie": ["Space Oddity", "Life on Mars", "Heroes", "Starman"],
        "The Rolling Stones": ["Paint it Black", "Sympathy for the Devil", "Gimme Shelter", "Angie"],
    }

    assert 'get_songs' in env, 'The function get_songs is not defined!'
    assert env['get_songs'](brit_artists, 'Elton John') == ["Rocket man", "Your Song", "Tiny Dancer", "Crocodile Rock"], \
        f'get_songs(brit_artists, "Elton John") returned {env["get_songs"](brit_artists, "Elton John")}.'
    assert env['get_songs'](brit_artists, 'Queen') == ["Bohemian Rhapsody", "We Will Rock You", "We Are The Champions", "Another One Bites The Dust"], \
        f'get_songs(brit_artists, "Queen") returned {env["get_songs"](brit_artists, "Queen")}.'
    assert env['get_songs'](brit_artists, 'David Bowie') == ["Space Oddity", "Life on Mars", "Heroes", "Starman"], \
        f'get_songs(brit_artists, "David Bowie") returned {env["get_songs"](brit_artists, "David Bowie")}.'

    try:
        env['get_songs'](brit_artists, 'Unknown Artist')
        assert False, 'get_songs should raise a ValueError when the artist is not found, but no exception was raised.'
    except ValueError:
        pass

