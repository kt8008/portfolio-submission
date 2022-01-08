# portfolio-submission
patternfinder is a python program that aims to find and color codes repeated segments in musical scores for you. It currently accommodates short monophonic music pieces. 

To run the program and see the results, you will have to install python, music21, Levenshtein, and a musicXML reader like MuseScore. 

When running patternfinder.py the first time, if you get the error,
PermissionError: [Errno 13] Permission denied: '/Applications/MuseScore 3.5.app',
run the program again. 

To replace the piece name,go to line 195 in patternfinder.py and replace the text within the quotation marks. 
Ex: thePiece = ryans.search('JacksonsFancyJig')
Here are some more pieces you can try(don't add spaces in between words):

	- EmpressClog
	- FerryBridgeHornpipe
	- NorthEndReel

patternfinder is a work in progress and usually not entirely accurate. Most often, found patterns often overlap, causing existing colors to be painted over in the visualization process. Also, several parts marked by comments in the code are not efficient and slow down the program immensely for longer musical scores. I am in the process of revising these issues.  

Future iterations will also include accessible chord progression analysis and a more abstract visualization. I aim to continue building onto this program and sharing it online eventually so more people can use it and make understanding classical music more accessible to everyone. 
