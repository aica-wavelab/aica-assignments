from otter.test_files import test_case

OK_FORMAT = False

name = "q51"
points = None

@test_case(points=None, hidden=False)
def test_get_songs(env):
    brit_artists = {'The Beattles': ['Yesterday', 'Hey Jude', 'Let it be', 'Come Together'], 'Queen': ['Bohemian Rhapsody', 'We Will Rock You', 'We Are The Champions', 'Another One Bites The Dust'], 'Elton John': ['Rocket man', 'Your Song', 'Tiny Dancer', 'Crocodile Rock'], 'David Bowie': ['Space Oddity', 'Life on Mars', 'Heroes', 'Starman'], 'The Rolling Stones': ['Paint it Black', 'Sympathy for the Devil', 'Gimme Shelter', 'Angie']}
    assert 'get_songs' in env, 'The function get_songs is not defined!'
    assert env['get_songs'](brit_artists, 'Elton John') == ['Rocket man', 'Your Song', 'Tiny Dancer', 'Crocodile Rock']
    assert env['get_songs'](brit_artists, 'Queen') == ['Bohemian Rhapsody', 'We Will Rock You', 'We Are The Champions', 'Another One Bites The Dust']
    assert env['get_songs'](brit_artists, 'David Bowie') == ['Space Oddity', 'Life on Mars', 'Heroes', 'Starman']
    assert env['get_songs']({'A': ['test']}, 'A') == ['test']

