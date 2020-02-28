import sys
import feedparser
import commands
import config

CMD_HQ = 'youtube-dl \
        --download-archive "~/archive.log" \
        -i \
        --add-metadata \
        --all-subs \
        --embed-subs \
        --embed-thumbnail \
        -f "(bestvideo[vcodec^=av01][height>=1080][fps>30]/bestvideo[vcodec=vp9.2][height>=1080][fps>30]/bestvideo[vcodec=vp9][height>=1080][fps>30]/bestvideo[vcodec^=av01][height>=1080]/bestvideo[vcodec=vp9.2][height>=1080]/bestvideo[vcodec=vp9][height>=1080]/bestvideo[height>=1080]/bestvideo[vcodec^=av01][height>=720][fps>30]/bestvideo[vcodec=vp9.2][height>=720][fps>30]/bestvideo[vcodec=vp9][height>=720][fps>30]/bestvideo[vcodec^=av01][height>=720]/bestvideo[vcodec=vp9.2][height>=720]/bestvideo[vcodec=vp9][height>=720]/bestvideo[height>=720]/bestvideo)+(bestaudio[acodec=opus]/bestaudio)/best" \
        --merge-output-format mkv \
        --yes-playlist '

CMD_LQ = 'youtube-dl \
        --download-archive "~/archive.log" \
        -i \
        --add-metadata \
        --all-subs \
        --embed-subs \
        --embed-thumbnail \
        -f best \
        --merge-output-format mkv \
        --yes-playlist '

BASE_URL_CHANNEL = "https://www.youtube.com/feeds/videos.xml?channel_id="
BASE_URL_USER = "https://www.youtube.com/feeds/videos.xml?user="
CHANNEL = "/channel/"
USER = "/user/"
CURRENT_GROUP = ""
WATCH = "watch\?"
ENTRIES = [] # (lineInfo, entries)
QUIT = False


def get_lines(filename):
    with open(filename, 'r') as f:
        return f.readlines()
    return []


def is_comment_or_empty(line):
    for c in line:
        if c not in [' ', '#']:
            return False

    return len(line) == 0 or line[0] == '#'


def get_rss_url(line):
    line = line.strip()
    i = line.find(CHANNEL)
    if i > 0:
        return BASE_URL_CHANNEL + line[i + len(CHANNEL):]

    i = line.find(USER)
    if i > 0:
        return BASE_URL_USER + line[i + len(USER):]

    return line


def get_line_parts(line):
    parts = line.split(' ')
    if len(parts) < 2:
        return {}

    partsDict = {
        'url': get_rss_url(parts[0]),
        'group': CURRENT_GROUP,
        'name': parts[1].strip()
    }

    return partsDict


def is_group(line):
    return len(line) > 0 and ' ' not in line


def interpret_line(line):
    global CURRENT_GROUP

    if is_comment_or_empty(line):
        return {}

    if is_group(line):
        CURRENT_GROUP = line.strip()

    return get_line_parts(line)


ARCHIVED_LINES = get_lines("/home/mitchell/archive.log")
def already_downloaded(watch_id):
    for line in ARCHIVED_LINES:
        if watch_id in line:
            return True

    return False


if len(sys.argv) < 2:
    print("Not enough arguments")
    sys.exit()

config.parse_config()

# URL HQ LOCATION
for line in get_lines(sys.argv[1]):
    lineInfo = interpret_line(line)
    if lineInfo == {}:
        continue

    unsavedEntries = []
    feed = feedparser.parse(lineInfo['url'])
    for entry in feed.entries:
        if not already_downloaded(entry.link[-11:]):
            unsavedEntries.append(entry)

    if len(unsavedEntries) == 0:
        continue

    ENTRIES.append( (lineInfo, list(unsavedEntries)) )
    #ENTRIES_DICT[lineInfo['name']] = list(unsavedEntries)

if len(ENTRIES) != 1:
    print(str(len(ENTRIES)) + " unique youtube channels were read.")
else:
    print("1 unique youtube channel was read.")


while True:
    commands.process_command_input(ENTRIES, input("> "))
