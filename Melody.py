# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 11:07:05 2019

@author: v-jakrah
"""
from __future__ import division
import Music #scaleInvert,scaleTranspose,scaleStretchInterval,rotation,reverse,getScales
from pyknon.music import NoteSeq, Note
from random import choice

durations = [1/4, 1/8, 1/16]
transformations = [Music.scaleInvert,Music.scaleTranspose,Music.scaleStretchInterval,
                   Music.rotation,Music.reverse]

def pickTransform(t):
    pick = choice(t)
    t.remove(pick)
    return pick

def Transform(notes,scale):
    degreeRange = range(-2,2)
    t = transformations.copy()
    t1 = pickTransform(t)
    t2 = pickTransform(t)
    t3 = pickTransform(t)
# =============================================================================
#     transform1 = t1(notes,scale,choice(degreeRange))
#     for note in transform1:
#         print(note.value, end=',')
#     print()
#     transform2 = t2(transform1,scale,choice(degreeRange))
#     for note in transform2:
#         print(note.value, end=',')
#     print()
#     newNotes = t3(transform2,scale,choice(degreeRange))
# =============================================================================
    newNotes = t3(t2(t1(notes,scale,choice(degreeRange)),
                             scale,choice(degreeRange)),
                            scale,choice(degreeRange))
    for note in newNotes:
        print(note.value, end=',')
    print()
    return newNotes

def genMelody(notes):
    scale = choice(Music.getScales(notes))
    scaleName = Music.note_name(scale,-1).lower() + " major"
    print("scale:", scaleName)
    Melody = NoteSeq()
    Melody += notes
    currNotes = notes
    for note in notes:
        note.dur = choice(durations)
    print(notes.items)
    for i in range(4):
        currNotes = Transform(notes,scale)
        Melody+=currNotes
    Melody+=end(currNotes, scale)
    print(Melody.items)
    Music.getSheetMusic(Melody, scaleName.split())
    
    return Melody
def end(notes, scale):
    print(notes.items, scale, (scale-1) % 7)
    end1 = Music.scaleInvertAtIndex(notes, scale, choice([4,6]))
    end1.reverse()
    end1+=NoteSeq([Note(scale, octave=5, dur=0.5)])
    if scale==0:
        end1[-1].octave+=1
    print("end:",end1.verbose)
    return end1


def main():
    notes = NoteSeq("E F G A")
    melody = genMelody(notes)
    Music.writeMidi('test1.mid', melody)
    Music.playMidi('test1.mid')
    
    
if __name__ == "__main__":
    main()