import sys
import os
'''
FEATURES TO ADD:
** time limit
** size limit
** backup locations when drive only has certain amount of space remaining
** vids per channel limit
** other than youtube support (reddit downloaders?)
** multithreading perhaps
** audio only
'''

CMD_HQ='youtube-dl \
        --download-archive "~/archive.log" \
        -i \
        --add-metadata \
        --all-subs \
        --embed-subs \
        --embed-thumbnail \
        -f "(bestvideo[vcodec^=av01][height>=1080][fps>30]/bestvideo[vcodec=vp9.2][height>=1080][fps>30]/bestvideo[vcodec=vp9][height>=1080][fps>30]/bestvideo[vcodec^=av01][height>=1080]/bestvideo[vcodec=vp9.2][height>=1080]/bestvideo[vcodec=vp9][height>=1080]/bestvideo[height>=1080]/bestvideo[vcodec^=av01][height>=720][fps>30]/bestvideo[vcodec=vp9.2][height>=720][fps>30]/bestvideo[vcodec=vp9][height>=720][fps>30]/bestvideo[vcodec^=av01][height>=720]/bestvideo[vcodec=vp9.2][height>=720]/bestvideo[vcodec=vp9][height>=720]/bestvideo[height>=720]/bestvideo)+(bestaudio[acodec=opus]/bestaudio)/best" \
        --merge-output-format mkv \
        --yes-playlist '

CMD_LQ='youtube-dl \
        --download-archive "~/archive.log" \
        -i \
        --add-metadata \
        --all-subs \
        --embed-subs \
        --embed-thumbnail \
        -f best \
        --merge-output-format mkv \
        --yes-playlist '

def getLines(filename):
    with open(filename, 'r') as f:
        return f.readlines()
    return ""

def isCommentOrEmpty(line):
    return len(line) == 0 or line[0] == '#'

def getLineParts(line):
    parts = line.split(' ')
    if len(parts) != 3:
        return { }

    partsDict = 
    {
        'url' : parts[0],
        'hq' : 'y' in parts[1].lower(),
        'name' : parts[2].lower()
    }

def interpretLine(line):
    if isCommentOrEmpty(line):
        return { }

    return getLineParts(line)

if len(sys.argv) < 3:
    print("Not enough arguments")
    sys.exit()

lines = getLines(sys.argv[1])
BASEPATH = sys.argv[2]

# URL HQ LOCATION
for line in lines:
    lineInfo = interpretLine(line)
    if lineInfo == { }:
        continue

    linePath = os.path.join(BASEPATH, lineInfo['name'])
    os.chdir(linePath)

    if lineInfo['hq']:
        print("~~~ Begin high quality download for URL: " + url)
        os.system(CMD_HQ + " '" + lineInfo['url'] + "'")
    else:
        print("~~~ Begin low quality download for URL: " + url)
        os.system(CMD_LQ + " '" + lineInfo['url'] + "'")

