octave = [
    'C', 'C#', 
    'D', 'D#', 
    'E', 'F', 
    'F#','G', 
    'G#', 'A', 
    'A#', 'B'
]

max_fret = 25
penalize_open = False
string_penalty = 1
num_tabs = 5
spacing = 4

class Note:
    """ Class to make handling notes slightly easier
    represented as a note in the basic ABCDEFG notation
    and the octave with 4 being a middle C
    Only sharps are used internally/supported"""
    def __init__(self, note, octave):
        self.note = note
        self.octave = octave
    @staticmethod
    def melody_factory(melody):
        """Makes a list of Notes from an inputted melody"""
        notes = []
        for note in melody:
            n, o = note.split(' ')
            notes.append(Note(n, int(o)))
        return notes
    
    def __str__(self):
        return self.note+str(self.octave)
    def __repr__(self):
        return self.note+str(self.octave)
    def __eq__(self, other):
        return self.note == other.note and self.octave == other.octave
    def __ne__(self, other):
        return self.note != other.note or self.octave != other.octave
    def __add__(self, other):
       index = octave.index(self.note)
       new_note = octave[(index+other) % len(octave)]
       new_octave = (index+other)//len(octave)+self.octave
       return Note(new_note, new_octave)
    def __hash__(self):
        return hash((self.note, self.octave))

standard = [
    Note('E', 4),
    Note('B', 3),
    Note('G', 3),
    Note('D', 3),
    Note('A', 2),
    Note('E', 2),
]

def note_on_string(note, string):
    """Returns the fret a note would be on given string"""
    amount = 0
    while note != string:
        string = string + 1
        amount += 1
        if (amount > max_fret):
            return None
    return amount

def note_distance_array(melody,  note):
    """Helper to find the distance being a position and note"""
    if penalize_open:
        return note_distance(melody[-1], note)
    s = 0
    for x in range(len(melody)):
        if melody[-x][1] == 0:
            continue
        s = note_distance(melody[-x], note)
        break
    return s

def note_distance(note1, note2):
    """Calculates note distance from fret difference and string switch"""
    s1, f1 = note1
    s2, f2 = note2
    if (f1 == 0) or (f2 == 0):
        return 0
    return abs(f1-f2)+string_penalty*abs(standard.index(s1)-standard.index(s2))

def search(melody, notes_to_frets):
    """Dijkstra's Algorithm for finding frets based on note distance
    Returns list of possible tabs and note distance"""
    
    queue = [(0, [note]) for note in notes_to_frets[melody[0]]]
    possible_tabs = []
    while len(queue) != 0:
        distance, current = queue.pop(0)
        next_note = len(current)

        if (next_note == len(melody)):
            possible_tabs.append((distance, current))
            if len(possible_tabs) > num_tabs:
                return possible_tabs
        else:
            for note in notes_to_frets[melody[next_note]]:
                queue.append((distance+note_distance_array(current,note), current+[note]))
            
            queue.sort(key=lambda x: x[0])
                    
    return possible_tabs

def pretty_print(tab, tuning):
    """Prints a tab in for a txt format"""
    strings = {t: "" for t in tuning}
    space = "-"*spacing
    for string, fret in tab:
        for s in strings:
            if s == string:
                strings[s] += space+str(fret)
            else:
                strings[s] += space+"-"*len(str(fret))
    
    print("_"*100)
    for note in tuning:
        print(note, "|", strings[note])

if __name__ == "__main__":    
    """Simple Smoke on the Water test"""
    test_melody = Note.melody_factory(['G 3', 'A# 3', 'C 4', 'G 3', 'A# 3', 'C# 4', 'C 4', 'G 3', 'A# 3', 'C 4', 'G 3'])

    note_to_frets = {}
    for note in test_melody:
        if note in note_to_frets:
            continue
        notes = []
        for string in standard:
            n = note_on_string(note, string)
            if (n != None):
                notes.append((string , n))
        note_to_frets[note] = notes

    for note, tab in note_to_frets.items():
        print(note, tab)

    for distance, tab in search(test_melody, note_to_frets):
        pretty_print(tab, standard)
        print("Distance:", distance)
        