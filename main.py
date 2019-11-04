import sys
import os
import requests
import re
import feedparser
import commands as cmds

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


def is_comment_or_empty(line):
    return len(line) == 0 or line[0] == '#'


def get_line_parts(line):
    parts = line.split(' ')
    if len(parts) != 3:
        return { }

    partsDict = {
        'url' : parts[0],
        'hq' : 'y' in parts[1].lower(),
        'name' : parts[2].lower().strip()
    }

    return partsDict


def interpret_line(line):
    if is_comment_or_empty(line):
        return { }

    return get_line_parts(line)


ARCHIVED_LINES = getLines("/home/mitchell/archiveydl.log")
def already_downloaded(watchID):
    print(watchID)
    for line in ARCHIVED_LINES:
        if watchID in line:
            return True

    return False


if len(sys.argv) < 3:
    print("Not enough arguments")
    sys.exit()

lines = getLines(sys.argv[1])
BASE_PATH = sys.argv[2]
WATCH = "watch\?"
ENTRIES_DICT = {}
QUIT = False

# URL HQ LOCATION
for line in lines:
    lineInfo = interpret_line(line)
    if lineInfo == { }:
        continue

    unsavedEntries = []
    feed = feedparser.parse(lineInfo['url'])
    for entry in feed.entries:
        if not already_downloaded(entry.link[-11:]):
            unsavedEntries.append(entry)

    if len(unsavedEntries) == 0:
        continue

    ENTRIES_DICT[lineInfo['name']] = list(unsavedEntries)

print("LEN")
print(len(ENTRIES_DICT))
#for dest, unsaved in ENTRIES_DICT.items():

while True:
    cmd = input("> ")
    #if cmd == "quit" or cmd == "exit":
    #    sys.exit()

    cmds.process_command_input(ENTRIES_DICT, cmd)


'''
    linePath = os.path.join(BASEPATH, lineInfo['name'])
    os.chdir(linePath)

    if lineInfo['hq']:
        print("~~~ Begin high quality download for URL: " + lineInfo['url'])
        os.system(CMD_HQ + " '" + lineInfo['url'] + "'")
    else:
        print("~~~ Begin low quality download for URL: " + lineInfo['url'])
        os.system(CMD_LQ + " '" + lineInfo['url'] + "'")
'''
