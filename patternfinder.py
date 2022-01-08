# patternfinder 4th iteration

from music21 import *
from Levenshtein import *
from random import randint
environment.set('musescoreDirectPNGPath', "/Applications/MuseScore 3.5.app")

def translatePiece(thePieceParsed):
    # converts musical score to list of note names
    correctedLine = ''
    notesPerPart = []
    # parse every instrument part in piece (currently only one part)
    for partNum in range(0, len(thePieceParsed.getElementsByClass(stream.Part))):
        thisPart = thePieceParsed.getElementsByClass(stream.Part)[partNum]
        segments, measureLists = search.segment.translateMonophonicPartToSegments(thisPart, 
            overlap=0, segmentLengths=1000, algorithm=search.translateDiatonicStreamToString)

        # translate music21 notation to regular notes names for now
        lineOfNotes = segments[0]
        notesPerPart.append(len(segments[0]))
        for letter in lineOfNotes:
            if letter == 'H' or letter == 'O':
                correctedLine += 'A'
            elif letter == 'I' or letter == 'P':
                correctedLine += 'B'
            elif letter == 'J' or letter == 'Q':
                correctedLine += 'C'
            elif letter == 'K' or letter == 'R':
                correctedLine += 'D'
            elif letter == 'L' or letter == 'S':
                correctedLine += 'E'
            elif letter == 'M' or letter == 'T':
                correctedLine += 'F'
            elif letter == 'N' or letter == 'U':
                correctedLine += 'G'
            else:
                correctedLine += letter

    lineOfNotes = correctedLine
    print("Piece displayed in terms of note names: ", lineOfNotes)
    return lineOfNotes
    
def toSegments(thePieceParsed, lineOfNotes):
    l = len(lineOfNotes)
    # divdes music into segments
    listOfSegLists = [] # list of segments, separated by size
    for x in range(0,l-2): 
        listOfSegLists.append([])
    timeSignature = thePieceParsed.recurse().getElementsByClass(meter.TimeSignature)[0]
    for x in range(3,l+1): 
        index = 0
        # For current music samples, longest pattern is at most two measures of sixteenth notes
        while index + x <= l and x < 4*timeSignature.denominator:
            seg = lineOfNotes[index:index+x]
            listOfSegLists[len(seg)-3].append(seg)
            index += 1
    return l, listOfSegLists

def findRepeatedSegments(l, listOfSegLists):
    # creates tuples of segments pairs and their levenstein distance (how similar they are)
    repeatedSegs = []
    listOfTupLists = []
    # This for loop section is very inefficient and is being replaced by the Rabin-Karp algorithm
    # in the next iteration of the code
    for x in range(0, l-2): 
        tupList = []
        sList = listOfSegLists[x]
        for i in range(0, len(sList)):
            for y in range(i+1, len(sList)):
                lev = distance(sList[i], sList[y])
                tup = (sList[i], i, sList[y], y, lev)
                tupList.append(tup)

                m = search.segment.getDifflibOrPyLev()
                m.set_seq1(sList[i])
                m.set_seq2(sList[y])
                # currently searching only for perfect matches, 
                # future iterations will account for slight variations in musical phrases
                if lev == 0: 
                    if len(tup[0]) + tup[1] - 1 < tup[3]: 
                        repeatedSegs.append(tup)
        listOfTupLists.append(tupList)

    # removes invalid overlapping repeated segments
    cleanerList = [] 
    for s in repeatedSegs:
        if len(s[0]) + s[1] - 1 < s[3]: 
            cleanerList.append(s)

    repeatedSegs = cleanerList
    return repeatedSegs

def eliminateOverlaps(repeatedSegs):
    # removing the repeats of the repeats
    if repeatedSegs == []:
        print("no repeated segments found")
    else: 
        repeatedSegs = repeatedSegs[::-1]
        largeRepSegList = [repeatedSegs[0]]
        # compare each repeated segment to other segment in largeSegmentList
        # this loop section is also inefficient and will be revised in later iterations. 
        start = 0
        for pair in repeatedSegs:
            pairBookends = (pair[1], pair[1] + len(pair[0]))
            overlap = False;
            largeRepSegListCopy = largeRepSegList
            for l in largeRepSegList: 
                largeSegBookends = (l[1],l[1] + len(l[0]))
                # if starting index within boundaries
                if largeSegBookends[0] <= pairBookends[0] and pairBookends[0] <= largeSegBookends[1]:
                    overlap = True
                    # if new segment is longer, replace shorter segment
                    if len(l[0]) < len(pair[0]):
                        largeRepSegListCopy.remove(l)
                        largeRepSegListCopy.append(pair)
                # if end index within boundaries
                elif largeSegBookends[0] <= pairBookends[1] and pairBookends[1] <= largeSegBookends[1]:
                    overlap = True
                    # if new segment is longer, replace shorter segment
                    if len(l[0]) < len(pair[0]):
                        largeRepSegListCopy.remove(l)
                        largeRepSegListCopy.append(pair)
            largeRepSegList = largeRepSegListCopy
            # if no indexes overlap, add to largeRepSegList
            if overlap == False:
                largeRepSegList.append(pair) 
                  
        return largeRepSegList
 
def outputTuple(notePosition):
    # useful tuple formatting
    justTheNotes = thePieceParsed.recurse().notes
    startingNote = justTheNotes[notePosition]
    startingMeasure = startingNote.measureNumber
    startingBeat = startingNote.beat
    theTup = (startingNote, startingMeasure, startingBeat, notePosition)
    return theTup 
    
def arrangeOutput(largeRepSegList):
    # combining repeated indices into one list of tuples per segment
    newTupleList = []
    indicesAccountedFor = [] # all indices added to an index list 
    for tup1 in largeRepSegList:
        if tup1[1] not in indicesAccountedFor and tup1[3] not in indicesAccountedFor: # if index not in list
            indicesAccountedFor += [tup1[1],tup1[3]]
            indexList = [outputTuple(tup1[1]), outputTuple(tup1[3])] # list of indices with specific pattern
            newTup = (tup1[0], indexList)
            newTupleList.append(newTup)
        else: # index already accounted for, add to appropriate list
            j = 0
            found = False
            while found == False:
                tup2 = newTupleList[j]
                if outputTuple(tup1[1]) in tup2[1]: 
                    tup2[1].append(outputTuple(tup1[3]))
                    found = True
                elif outputTuple(tup1[3]) in tup2[1]: 
                    tup2[1].append(outputTuple(tup1[1]))
                    found = True
                else:
                    j+=1
                    if j >= len(newTupleList):
                        print('something went wrong, j= ', j)
    return newTupleList
                    
def colorCode(thePieceParsed, newTupleList):
    # color coding different patterns
    colors = []
    for i in range(len(newTupleList)):
        colors.append('#%06X' % randint(0, 0xFFFFFF))
    justTheNotes = thePieceParsed.recurse().notes
    counter = 0
    for tup in newTupleList: 
        print(tup)
        for startNote in tup[1]:
            for x in range(startNote[3], startNote[3] + len(tup[0])): 
                aNote = justTheNotes[x]
                aNote.style.color = colors[counter]
        counter += 1
    thePieceParsed.show()
    
def patternfinder(thePieceParsed):
    # assembling the crew
    lineOfNotes = translatePiece(thePieceParsed)
    pieceLength, listOfSegLists = toSegments(thePieceParsed, lineOfNotes)
    repeatedSegs = findRepeatedSegments(pieceLength, listOfSegLists)
    largeRepSegList = eliminateOverlaps(repeatedSegs)
    newTupleList = arrangeOutput(largeRepSegList)
    colorCode(thePieceParsed, newTupleList)
    return newTupleList
    
# choosing piece from music21's ryansMammoth library
# functionality is currently limited to short monophonic musical scores like these
ryans = corpus.search('ryansMammoth')
thePiece = ryans.search('The Boston -- Reel') 
thePieceParsed = thePiece[0].parse()

# activating patternfinder
out = patternfinder(thePieceParsed)
print("Formatting: each pattern includes (pattern, list of occurences)")
print("Formatting: each occurence includes (startingNote, startingMeasure, startingBeat, notePosition)")
print("Patterns found in piece: ")
for pat in out:
    print(pat)