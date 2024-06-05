import music21 as m21
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

TOLERANCE=1e-5
REST = -1
HOLD = -2

def melodies_to_piano_roll_df(streams: list[m21.stream.Stream], time_step, max_time_steps=None) -> pd.DataFrame:
    """
    Convert multiple music21 streams to a DataFrame where each row is a melody in piano roll format.
    
    Parameters:
    - streams: list of music21.stream.Stream objects
    - time_step: float, duration of each time step in quarter lengths
    - max_time_steps: int, maximum number of time steps to include in the DataFrame (optional)
    
    Returns:
    - pandas DataFrame where each row is a melody and columns represent time steps
    """
    melodies = []
    max_length = 0

    for stream in streams:
        # Get the total length of the stream in quarter lengths
        total_length = stream.highestTime
        num_time_steps = int(math.ceil(total_length / time_step))
        if max_time_steps:
            num_time_steps = min(num_time_steps, max_time_steps)
        
        max_length = max(max_length, num_time_steps)
        
        # Initialize a list for the melody
        melody = [None] * num_time_steps
        
        for element in stream.flatten().notesAndRests:
            start_time = element.offset
            end_time = start_time + element.quarterLength
            start_idx = int(start_time / time_step)
            end_idx = int(end_time / time_step)
            
            if isinstance(element, m21.note.Note):
                pitch = element.pitch.midi
            else:
                pitch = REST

            if start_idx < num_time_steps:
                melody[start_idx] = pitch
            for i in range(start_idx + 1, end_idx):
                if i < num_time_steps:
                    melody[i] = HOLD
        melodies.append(melody)

    # Fill None with REST or HOLD (holding rest) if they occur at the end
    for i, melody in enumerate(melodies):
        for j in range(len(melody)):
            if melodies[i][j] == None:
                if j == 0 or melodies[i][j-1] != REST:
                    melodies[i][j] = REST
                else:
                    melodies[i][j] = HOLD
    
    # Create a DataFrame from the list of melodies
    df = pd.DataFrame(melodies, columns=[f"Time_{i*time_step}" for i in range(max_length)])
    
    return df

def stream_to_df(stream: m21.stream.Stream, include_rests: bool=False) -> pd.DataFrame:
    notes = {'pitch': [], 'duration': [], 'start': [], 'end': [], 'step': []}
    prev_start = 0
    #prev_end = 0
    start = 0

    for event in stream.flatten().notesAndRests:
        if isinstance(event, m21.note.Note):
            dur = event.duration.quarterLength
            notes['pitch'].append(event.pitch.midi)
            notes['duration'].append(dur)

            notes['start'].append(start)
            notes['end'].append(start + dur)
            notes['step'].append(start - prev_start)
            prev_start = start
            start += dur
            #prev_end = start
        if isinstance(event, m21.chord.Chord):
            dur = event.duration.quarterLength          
            for pitch in event.pitches:
                dur = event.duration.quarterLength
                notes['pitch'].append(pitch.midi)
                notes['duration'].append(dur)

                notes['start'].append(start)
                notes['end'].append(start + dur)
                notes['step'].append(start - prev_start)
            prev_start = start
            start += dur
        elif isinstance(event, m21.note.Rest):
            if include_rests:
                dur = event.duration.quarterLength
                notes['pitch'].append(REST)
                notes['duration'].append(dur)

                notes['start'].append(start)
                notes['end'].append(start + dur)
                notes['step'].append(start - prev_start)
                prev_start = start
                start += dur
            else:
                dur = event.duration.quarterLength
                start += dur 
    df = pd.DataFrame({name: np.array(value) for name, value in notes.items()})
    sorted_df = df.sort_values(by='start')
    return sorted_df


def stream_to_piano_roll_df(stream: m21.stream.Stream, time_step) -> pd.DataFrame:
    """
    Convert a music21 stream to a piano roll DataFrame.
    
    Parameters:
    - stream: music21.stream.Stream object
    - time_step: float, duration of each time step in quarter lengths
    
    Returns:
    - pandas DataFrame representing the piano roll
    """
    # Find the total length of the piece in quarter lengths
    total_length = stream.highestTime

    # Create a time index
    time_index = pd.RangeIndex(start=0, stop=int(math.ceil(total_length / time_step)))
    
    # Collect used pitches
    used_pitches = set()
    for element in stream.flatten().notes:
        if isinstance(element, m21.note.Note):
            used_pitches.add(element.pitch.midi)
        elif isinstance(element, m21.chord.Chord):
            for pitch in element.pitches:
                used_pitches.add(pitch.midi)
    
    if not used_pitches:
        return pd.DataFrame()  # Return 
    
    # Determine the range of used pitches
    min_pitch = min(used_pitches)
    max_pitch = max(used_pitches)

    # Create an empty DataFrame with the time index and MIDI pitches as columns
    pitches = list(range(min_pitch, max_pitch + 1))  # MIDI pitches range from 0 to 127
    piano_roll = pd.DataFrame(0, index=time_index, columns=pitches)
    
    for element in stream.flatten().notes:
        if isinstance(element, m21.note.Note):
            start_time = element.offset
            end_time = start_time + element.quarterLength
            start_idx = int(start_time / time_step)
            end_idx = int(math.ceil(end_time / time_step)) - 1 # since start_idx:end_idx is inclusive!
            pitch = element.pitch.midi
            piano_roll.loc[start_idx:end_idx, pitch] = 1
        elif isinstance(element, m21.chord.Chord):
            start_time = element.offset
            end_time = start_time + element.quarterLength
            start_idx = int(start_time / time_step)
            end_idx = int(math.ceil(end_time / time_step)) - 1
            for pitch in element.pitches:
                piano_roll.loc[start_idx:end_idx, pitch.midi] = 1
    
    return piano_roll

def plot_df(notes: pd.DataFrame, title = None, count = None):
    if title == None:
        if count:
            title = f'First {count} notes'
        else:
            title = f'Whole track'
            count = len(notes['pitch'])
    fig, ax = plt.subplots(figsize=(20, 10))
    plot_pitch = np.stack([notes['pitch'], notes['pitch']], axis=0)
    plot_start_stop = np.stack([notes['start'], notes['end']], axis=0)
    ax.plot(
        plot_start_stop[:, :count], plot_pitch[:, :count], c='b', alpha=0.6, linewidth=3.0)
    ax.set_xlabel('Time in quarter Notes')
    ax.set_ylabel('Pitch')
    ax.set_title(title)

    ax.set_xticks(np.arange(0, notes['end'].max(), 1.0))
    
    # Add grid lines
    ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
    
    # Hide the tick labels
    ax.set_xticklabels([])
    
    plt.show()


def plot_piano_roll(piano_roll_df: pd.DataFrame, time_step):
    """
    Plot the piano roll from a DataFrame.
    
    Parameters:
    - piano_roll_df: pandas DataFrame representing the piano roll
    - time_step: float, duration of each time step in quarter lengths
    """
    fig, ax = plt.subplots(figsize=(20, 10))
    
    time_indices, pitch_indices = piano_roll_df.stack().index.to_frame().values.T
    values = piano_roll_df.stack().values
    
    # Plot the piano roll
    ax.scatter(time_indices, pitch_indices, c=values, marker='s', s=5, cmap='Blues', alpha=0.6)
    
    # Set the labels and title
    ax.set_xlabel('Time (quarter lengths)')
    ax.set_ylabel('MIDI Pitch')
    ax.set_title('Piano Roll')

    # Invert the y-axis to have the higher pitches at the top
    #ax.set_ylim(ax.get_ylim()[::-1])
    
    # Invert the y-axis to have the lower pitches at the bottom
    #ax.invert_yaxis()
    
    plt.show()

def has_acceptable_duration(stream: m21.stream.Stream, time_step: float) -> bool:
    """
    Tests if all notes and rests of the stream (piece of music) are a multiple of the time_step.
    If this is not the case a time discretization (e.g. a piano roll) using time_step chunks of time can not
    accurately represent the stream.
    
    Parameters:
    - stream: Stream, the stream to test
    - time_step: float, duration of each time step that defines the grids resolution in quarter lengths
    
    Returns:
    - True, if the stream is can be represented by a piano roll with a time step equal to time_step
    - False, otherwise
    """
    for note in stream.flatten().notesAndRests:
        n = note.duration.quarterLength / time_step
        closest_int = round(n)
        if not math.isclose(n, closest_int, abs_tol=TOLERANCE):
            return False
    return True