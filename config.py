import sys
import os

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

CONFIRM_DL = True

def get_lines():
    with open('/home/mitchell/.config/ydlsub.conf', 'r') as f:
        return f.readlines()
    return []


def is_comment_or_empty(line):
    for c in line:
        if c not in [' ', '#']:
            return False

    return len(line) == 0 or line[0] == '#' or line[0] == '\n'



def parse_config():
    for line in get_lines():
        if is_comment_or_empty(line):
            continue
        parts = line.split('=')
        if len(parts) != 2:
            continue
        
        if parts[0].upper() == "CONFIRM_DL":
            CONFIRM_DL = 'Y' in parts[1].upper()
                
