# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 10:58:59 2019

@author: v-jakrah
"""

from __future__ import division
import pygame
from pyknon.genmidi import Midi
import os
from pyknon.music import Note, NoteSeq
import math
from abjad import Staff, show, attach, KeySignature, TimeSignature, Clef

pattern = [0,2,4,5,7,9,11]
majorScales = {}
for i in range(12):
    majorScales[i] = [(j+i)%12 for j in pattern]
    
octaveDict = {0:",,,,",
              1:",,,",
              2:",,",
              3:",",
              4 : "", 
              5 : "'", 
              6: "''", 
              7:"'''",
              8:"''''",
              9:"'''''"
        }

def mod12(n):
    return n%12
def note_name(number,scale): 
    if scale == -1:
        notes = 'C C# D Eb E F F# G Ab A Bb B'.split()
    elif scale in (5,10,3,8,1):
        notes = 'C Df D Ef E F Gf G Af A Bf B'.split()
    else:
        notes = 'C Cs D Ds E F Fs G Gs A As B'.split()
    
    return notes[mod12(number)]
def accidentals( note_string):
    acc = len(note_string[1:])
    if '#' in note_string:
        return acc
    elif 'b' in note_string:
        return -acc
    else:
        return 0
def name_to_number(note_string):
    notes = 'C . D . E F . G . A . B'.split()
    name = note_string[0:1].upper()
    number = notes.index(name)
    acc = accidentals(note_string)
    return mod12(number + acc)
def writeMidi(path, seq):
    if type(seq[0]) == Note:
        print("One Track")
        midi = Midi(1, tempo=100)
        midi.seq_notes(seq)
    else:
        midi = Midi(len(seq), tempo=100)
        i = 0
        for track in seq:
            midi.seq_notes(track, track=i)
            print(track)
            i+=1
    midi.write(path)
def playMidi(path):
    print("play")
    clock = pygame.time.Clock()
    pygame.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(60)
    print("end")
    os.remove(path)
def getScales(notes):
    notes = [note.value for note in notes]
    for note in notes:
        print(note)
    ans = []
    for scale in majorScales:
        if all(note in majorScales[scale] for note in notes):
            ans.append(scale)
    return ans

def mod7(x):
    return x % 7
def getNoteNums(notes, scaleNum):
    #input is NoteSeq, translate to numbers
    durations = [note.dur for note in notes]
    NoteNums = [note.value for note in notes]
    scale = majorScales[scaleNum]
    ans = []
    for note in NoteNums:
        for i in range(len(scale)):
            if note==scale[i]:
                ans.append(i)
    #print(ans)
    return ans, durations
def getNotesFromNums(nums, scaleNum, durations):
    #convert back to noteSeq
    scale = majorScales[scaleNum]
    ans = NoteSeq()
    j = 0
    for num in nums:
        for i in range(len(scale)):
            if num==i:
                ans.append(Note(scale[i], dur=durations[j]))
                j+=1
    #print(ans)
    return ans
#invert
def scaleInvert(notes, scaleNum, index=6):
    print('invert', index)
    NoteNums, durations = getNoteNums(notes, scaleNum)
    inverted = [mod7(index - n) for n in NoteNums]
    durations.reverse()
    return getNotesFromNums(inverted, scaleNum, durations)
#transpose
def scaleTranspose(notes, scaleNum, distance=1):
    print('transpose', distance)
    NoteNums, durations = getNoteNums(notes, scaleNum)
    transposed = [mod7(n + distance) for n in NoteNums]
    return getNotesFromNums(transposed, scaleNum, durations)
def scaleInvertAtIndex(notes, scaleNum, index=0):
    NoteNums, durations = getNoteNums(notes, scaleNum)
    intervals = [NoteNums[0] - NoteNums[i] for i in range(1,len(NoteNums))]
    newNotes = [index]
    for i in intervals:
        newNotes.append((index+i)%7)
    return getNotesFromNums(newNotes, scaleNum, durations)
#stretch_Duration
def scaleStretchDuration(notes, scaleNum, factor):
    print('stretchdur',factor)
    notes.stretch_dur(factor)
    return notes
#stretch_interval
def scaleStretchInterval(notes, scaleNum, factor):
    print('stretchinterval', factor)
    NoteNums, durations = getNoteNums(notes, scaleNum)
    #print(NoteNums)
    intervals = [NoteNums[i+1] - NoteNums[i] for i in range(len(NoteNums)-1)]
    #print(intervals)
    stretched = [math.ceil(n+factor) for n in intervals]
    #print(stretched)
    resultNums = [NoteNums[0]]
    for i in stretched:
        resultNums.append((resultNums[-1]+i) % 7)
    return getNotesFromNums(resultNums, scaleNum, durations)
def rotation(notes, scaleNum, degree):
    print('rotation', degree)
    notes.rotate(degree)
    return notes
def reverse(notes, scaleNum, degree):
    print('reverse')
    notes.reverse()
    return notes

def getSheetMusic(Melody, scale):
    print(scale)
    melodyNotes = [note_name(n,name_to_number(scale[0])).lower() for n in [note.value for note in Melody]]
    print(melodyNotes)
    durations = [int(1/note.dur) for note in Melody]
    octaves = [note.octave for note in Melody]
    abjadArr = []
    for i in zip(melodyNotes, durations, octaves):
        abjadArr.append(i[0] + octaveDict[i[2]] + str(i[1]))
    abjadString = ' '.join(abjadArr)
    staff = Staff(abjadString)
    #attach(KeySignature('c','major'), staff[0])
    attach(KeySignature(scale[0],scale[1]), staff[0])
    attach(TimeSignature((3,4)),staff[0])
    #attach(Clef("bass"), staff[0])
    show(staff)