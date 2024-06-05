import os
import music21 as m21
from pianoroll import has_acceptable_duration

def load_midi_files(folder_path: str, time_step: float | None= None, max_files: float | None=None, transpose_to_major: bool=False) -> list[m21.stream.Stream]:
    """
    Load MIDI files from a given folder and return a list of music21 stream objects.
    
    Parameters:
    - folder_path: str, path to the folder containing MIDI files
    
    Returns:
    - List of music21.stream.Score objects
    """
    midi_streams = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.mid') or file_name.endswith('.midi'):
            file_path = os.path.join(folder_path, file_name)
            midi_stream = m21.converter.parse(file_path)
            if time_step == None or has_acceptable_duration(midi_stream, time_step):
                if transpose_to_major:
                    midi_stream = transpose(midi_stream)
                if max_files != None and max_files <= len(midi_streams):
                    break
                else:
                    midi_streams.append(midi_stream)
    return midi_streams

def transpose(stream: m21.stream.Stream) -> m21.stream.Score:
    # get key from the song
    #parts = stream.getElementsByClass(m21.stream.Part)
    #measures_part0 = parts[0].getElementsByClass(m21.stream.Measure)
    #key = measures_part0[0][4]

    # estimate key using music21
    #if not isinstance(key, m21.key.Key):
    key = stream.analyze('key')

    # get interval for transposition, e.g., Bmaj -> Cmaj
    if key.mode == 'major':
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch('C'))
    elif key.mode == 'minor':
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch('A'))

    # transpose song by calculated interval
    transpose_song = stream.transpose(interval)

    return transpose_song