from otter.test_files import test_case

OK_FORMAT = False

name = "q52"
points = None

@test_case(points=None, hidden=False)
def test_get_songs(env):
    brit_artists = {'The Beattles': ['Yesterday', 'Hey Jude', 'Let it be', 'Come Together'], 'Queen': ['Bohemian Rhapsody', 'We Will Rock You', 'We Are The Champions', 'Another One Bites The Dust'], 'Elton John': ['Rocket man', 'Your Song', 'Tiny Dancer', 'Crocodile Rock'], 'David Bowie': ['Space Oddity', 'Life on Mars', 'Heroes', 'Starman'], 'The Rolling Stones': ['Paint it Black', 'Sympathy for the Devil', 'Gimme Shelter', 'Angie']}
    assert 'get_artist' in env, 'The function get_artist is not defined!'
    assert env['get_artist'](brit_artists, 'Bohemian Rhapsody') == 'Queen'
    assert env['get_artist'](brit_artists, 'Space Oddity') == 'David Bowie'
    assert env['get_artist'](brit_artists, 'Yesterday') == 'The Beattles'

