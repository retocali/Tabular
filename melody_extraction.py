# import aubio
# import numpy as np
# from midiutil import MIDIFile
import vamp
import librosa
import guitar_tab_finder as gt
# import sys
# audio_file = sys.argv[1]

path = "files/"
def launcher(filename, sp, op):
    gt.string_penalty = float(sp)
    gt.penalize_open = op == None
    print(filename)
    name, extension = filename.split(".")
    if extension == "csv" or extension == "txt":
        return text_launcher(filename)
    # This is how we load audio using Librosa
    audio, sr = librosa.load(path+filename, sr=44100, mono=True)

    params = {"minfqr": 100.0, "maxfqr": 800.0, "voicing": 0.2, "minpeaksalience": 0.0}

    data = vamp.collect(audio, sr, "mtg-melodia:melodia", parameters=params)
    hop, melody = data['vector']

    notes = []
    prev_m = None
    for m in melody:
        if m != prev_m and m > 0:
            notes.append(gt.freq_to_note(int(m)))
            prev_m = m

    print(notes)
    pruned_notes = []
    prev_note = None
    for n in notes:
        if n != prev_note:
            pruned_notes.append(n)
            prev_note = n

    print(pruned_notes)
    return gt.launcher(pruned_notes)

        

def text_launcher(filename):
    file = open(path+filename, "r")
    notes = []
    for line in file.readlines():
        parsed = [x for x in line.split(",")]
        notes.extend(gt.Note.melody_factory(parsed))
    return gt.launcher(notes)


if __name__ == "__main__":
    # This is how we load audio using Librosa
    audio, sr = librosa.load(audio_file, sr=44100, mono=True)

    params = {"minfqr": 100.0, "maxfqr": 800.0, "voicing": 0.2, "minpeaksalience": 0.0}

    data = vamp.collect(audio, sr, "mtg-melodia:melodia", parameters=params)
    hop, melody = data['vector']

    notes = []
    prev_m = None
    for m in melody:
        if m != prev_m and m > 0:
            notes.append(gt.freq_to_note(int(m)))
            prev_m = m

    print(notes)
    pruned_notes = []
    prev_note = None
    for n in notes:
        if n != prev_note:
            pruned_notes.append(n)
            prev_note = n

    print(pruned_notes)

    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 60   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                        # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(pruned_notes):
        MyMIDI.addNote(track, channel, int(pitch), time + i, duration, volume)

    with open("output.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)