octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#','A', 'A#', 'B', ]
class Note:
    def __init__(self, note, octave):
        self.note = note
        self.octave = octave
    @staticmethod
    def melodyFactory(melody):
        notes = []
        for note in melody:
            notes.append(Note(*note.split(' ')))
        return notes
    
    def __str__(self):
        return self.note+str(self.octave)
    def __repr__(self):
        return self.note+str(self.octave)
    def __eq__(self, other):
        return self.note == other.note and self.octave == other.octave
    def __ne__(self, other):
        print(self, other, self.note != other.note, self.octave != other.octave)
        return self.note != other.note or self.octave != other.octave
    def __add__(self, other):
       index = octave.index(self.note)
       new_note = octave[(index+other) % len(octave)]
       new_octave = (index+other)//len(octave)+self.octave
       return Note(new_note, new_octave)

strings = [
    Note('E', 4),
    Note('B', 3),
    Note('G', 3),
    Note('D', 3),
    Note('A', 2),
    Note('E', 2),
]
def noteOnString(note, string):
    amount = 0
    print("-"*8)
    while note != string:
        print(note, string, amount, note==string)
        string = string + 1
        amount += 1
        if (amount > 25):
            return None
    return amount

testMelody = Note.melodyFactory(['G 5', 'A# 5', 'C 5', 'G 5', 'A# 5', 'C# 5', 'G 5', 'A# 5', 'C 5', 'G 5'])

possibleTabs = []
for note in testMelody:
    notes = []
    for string in strings[:1]:
        n = noteOnString(note, string)
        notes.append(n)
    possibleTabs.append(notes)

print(possibleTabs)