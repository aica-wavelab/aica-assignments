import warnings
import music21 as m21
from fractions import Fraction
from pianoroll import has_acceptable_duration

TERM_SYMBOL = '.'
TIME_STEP = 1.0
HOLD_SYMBOL = '_'

class Encoder:
    def __init__(self, time_step=TIME_STEP):
        self.time_step = time_step
    
    def has_acceptable_duration(self, stream: m21.stream.Stream):
        return has_acceptable_duration(stream, self.time_step)

    def encode_streams(self, streams: list[m21.stream.Stream], flatten=False, terminal=False) -> list[list[str]]:
        encoded_songs = []
        invalid_song_indices = []
        for i, song in enumerate(streams):
            # filter out songs that have non-acceptalbe durations
            if not self.has_acceptable_duration(song):
                warnings.warn(f"{song} gets ignored since it is incompatible with the time step {self.time_step}", UserWarning)
                invalid_song_indices.append(i)
                continue
            # encode songs with music time series representation
            encoded_song = self.encode_stream(song)
            if terminal:
                encoded_song = [TERM_SYMBOL] + encoded_song

            if flatten:
                encoded_songs += encoded_song
            else:
                encoded_songs.append(encoded_song)
        return encoded_songs, invalid_song_indices
    
    def decode_streams(self, melodies: list[list[str]]) -> list[m21.stream.Score]:
        songs = []
        for melody in melodies:
            songs.append(self.decode_stream(melody))
        return songs

    def encode_stream(self, stream: m21.stream.Stream) -> list[str]:
        pass

    def decode_stream(self, melody: list[str]) -> m21.stream.Stream:
        pass
    
    def take_notes(self, melody: list[str], n_notes: int) -> list[str]:
        pass

class PianoRollEncoder(Encoder):
    """
    Encoder that encode each single beat, meaning that each token represents the exact same amount of time.
    One can also say this encoding is equitemporal.
    """

    def __init__(self, time_step=TIME_STEP):
        super().__init__(time_step)
        self.time_step = time_step
    
    def encode_stream(self, song : m21.stream.Score) -> list[str]:
        # p = 60, d = 1.0 -> [60, "_", "_", "_"]
        
        encoded_song = []
        
        for event in song.flatten().notesAndRests:
            
            # handle notes
            if isinstance(event, m21.note.Note):
                symbol = event.pitch.midi # e.g. 60
            
            #handle rests
            elif isinstance(event, m21.note.Rest):
                symbol = 'r'
            
            # convert the note/rest into time series notation
            steps = int(round(event.duration.quarterLength / self.time_step))
            for step in range(steps):
                if step == 0:
                    encoded_song.append(str(symbol))
                else:
                    encoded_song.append(HOLD_SYMBOL)
                    
        #encoded_song = ' '.join(map(str, encoded_song))
        
        return encoded_song

    def decode_stream(self, melody: list[str]) -> m21.stream.Stream:

        # create a music21 stream
        stream = m21.stream.Stream()

        # parse all the symbols in the melody and create note/rest objects
        start_symbol = None
        step_counter = 1

        for i, symbol in enumerate(melody):
            if symbol != HOLD_SYMBOL or i + 1 == len(melody):

                if start_symbol is not None:
                    quater_length_duration = self.time_step * step_counter

                    if start_symbol == 'r':
                        m21_event = m21.note.Rest()

                    else:
                        m21_event = m21.note.Note(int(start_symbol))

                    dur = m21.duration.Duration()
                    dur.quarterLength = quater_length_duration
                    m21_event.duration = dur
                    stream.append(m21_event)

                    # reset the step counter
                    step_counter = 1

                start_symbol = symbol
            else:
                step_counter += 1
        return stream
    
    def take_notes(self, melody: list[str], n_notes: int) -> list[str]:
        part = []
        note_count = 0
        for symbol in melody:
            
            if symbol != HOLD_SYMBOL:
                if note_count >= n_notes:
                    break
                note_count += 1
            part.append(symbol)
            
        return part
    
class EventEncoder(Encoder):
    """
    Encoder that encode each single note, meaning that each token represents one note (of different length/duration).
    One can also say this encoding is not equitemporal.
    """

    def __init__(self, time_step=TIME_STEP):
        super().__init__(time_step)
        self.time_step = time_step

    def encode_stream(self, stream: m21.stream.Stream) -> list[str]:
        # p = 60, d = 1.0 -> 60/4 assuming 0.25 min duration

        encoded_song = []

        for event in stream.flatten().notesAndRests:

            # handle notes
            if isinstance(event, m21.note.Note):
                symbol = event.pitch.midi  # e.g. 60

            # handle rests
            elif isinstance(event, m21.note.Rest):
                symbol = 'r'

            # convert the note/rest into time series notation
            steps = int(round(event.duration.quarterLength / self.time_step))
            encoded_song.append(str(symbol)+'/'+str(steps))
        return encoded_song
            
    def has_acceptable_duration(self, stream: m21.stream.Stream):
        return True
    
    def decode_stream(self, melody: list[str]) -> m21.stream.Stream:
        # create a music21 stream
        part = m21.stream.Part()

        for i, symbol in enumerate(melody):

            split = symbol.split('/')
            pitch, steps = split[0], split[1]

            if pitch == 'r':
                m21_event = m21.note.Rest()
            else:
                m21_event = m21.note.Note(int(pitch))

            dur = m21.duration.Duration()
            dur.quarterLength = self.time_step*int(steps)
            m21_event.duration = dur
            
            part.append(m21_event)
        return part

    def take_notes(self, melody: list[str], n_notes: int) -> list[str]:
        return melody[:min(n_notes, len(melody))]

class StringToIntEncoder:
    def __init__(self, enc_songs: list[list[str]]):
        self.symbols = sorted(
            list(set([item for sublist in enc_songs for item in sublist])))
        
        self.stoi = dict()
        j = 0
        for i, s in enumerate(self.symbols):
            # TODO: this is dirty!
            if s != TERM_SYMBOL:
                self.stoi[s] = i+1-j
            else:
                j = 1

        self.stoi[TERM_SYMBOL] = 0
        self.itos = {i: s for s, i in self.stoi.items()}

    def __len__(self) -> int:
        return len(self.stoi)
    
    def encode_sequence(self, symbols: list[str]):
        return [self.encode(symbol) for symbol in symbols]
    
    def decode_sequence(self, numbers: list[int]):
        return [self.decode(k) for k in numbers]

    def encode(self, symbol: str) -> int:
        return self.stoi[symbol]
    
    def decode(self, index: int) -> str:
        return self.itos[index]
    
    def encode_sequences(self, sequences: list[list[str]]):
        return [self.encode_sequence(sequence) for sequence in sequences]
    
    def decode_sequences(self, sequences: list[list[int]]):
        return [self.decode_sequence(sequence) for sequence in sequences]
    
class NoteToIntEncoder:
    def __init__(self, enc_songs: list[m21.stream.Stream]):        
        elements = []
        for score in enc_songs:
            for element in score.recurse():
                if isinstance(element, (m21.note.Rest, m21.note.Note)):
                    elements.append(element)

        self.symbols = NoteToIntEncoder.filter_notes_rests(elements)
        self.stoi = {s: i+1 for i, s in enumerate(self.symbols)}
        self.stoi[TERM_SYMBOL] = 0
        self.itos = {i: s for s, i in self.stoi.items()}

    @staticmethod
    def filter_notes_rests(list_of_notes):
        def filter_notes(notes):
            notes = list(map(lambda note: (note.pitch.midi, note.duration.quarterLength), notes))
            notes.sort()
            filtered_notes = []
            for element in notes:
                if len(filtered_notes) == 0:
                    filtered_notes.append(element)
                else:
                    tail = filtered_notes[len(filtered_notes)-1]
                    if element > tail:
                        filtered_notes.append(element)
            return filtered_notes

        def filter_rests(rests):
            rests = list(map(lambda rest: rest.duration.quarterLength, rests))
            rests.sort()
            filtered_rests = []
            for rest in rests:
                if len(filtered_rests) == 0:
                    filtered_rests.append(rest)
                elif rest > filtered_rests[len(filtered_rests)-1]:
                    filtered_rests.append(rest)
            return filtered_rests
        notes = []
        rests = []

        for el in list_of_notes:
            if isinstance(el, m21.note.Note):
                notes.append(el)
            if isinstance(el, m21.note.Rest):
                rests.append(el)

        notes = filter_notes(notes)
        rests = filter_rests(rests)
        return notes + rests

    def __len__(self) -> int:
        return len(self.stoi)

    def encode(self, symbol: m21.note.Note | m21.note.Rest | str) -> int:
        if isinstance(symbol, str):
            return self.stoi[symbol]
        if isinstance(symbol, m21.note.Note):
            return self.stoi[(symbol.pitch.midi, symbol.duration.quarterLength)]
        elif isinstance(symbol, m21.note.Rest):
            return self.stoi[symbol.duration.quarterLength]
        else:
            warnings.warn(f"{symbol} gets ignored since it is of type {type(symbol)}, which is not supported", UserWarning)
            return None
    
    def decode(self, index: int) -> m21.note.Note | m21.note.Rest:
        element = self.itos[index]
        if isinstance(element, tuple):
            midi, dur = element
            note = m21.note.Note()
            note.pitch.midi = midi
            note.duration.quarterLength = dur
            return note
        elif isinstance(element, (float, int, Fraction)):
            return m21.note.Rest(element)
        else:
            return element

    def encode_sequence(self, symbols: m21.stream.Stream) -> list[int]:
        result = []
        for symbol in symbols.recurse().notesAndRests:
            enc = self.encode(symbol)
            if enc != None:
                result.append(enc)
        return result
    
    def decode_sequence(self, numbers: list[int]) -> m21.stream.Stream:
        part = m21.stream.Part()
        part.append([self.decode(k) for k in numbers])
        return part
    
    def encode_sequences(self, sequences: list[m21.stream.Stream]):
        return [self.encode_sequence(sequence) for sequence in sequences]
    
    def decode_sequences(self, sequences: list[list[int]]):
        return [self.decode_sequence(sequence) for sequence in sequences]

    def __repr__(self) -> str:
        return str(f'stoi: {self.stoi} itos: {self.itos}')