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

# compare if search author a is equivalent to author b
def author_match(a, b):
    if a == b or a in b:
        return True

    # check without spaces or underscores
    a = a.upper().replace(' ', '').replace('_', '')
    b = b.upper().replace(' ', '').replace('_', '')
    return a == b or a in b


# quit
def quit():
    sys.exit()


# ls < author : optional >
def ls(entries_dict, cmd_args):
    if len(cmd_args) == 1:
        for dest, entries in entries_dict.items():
            print("Author: " + entries[0].author)
            print("Download Location: " + dest)
            print("Unsaved Count: " + str(len(entries)))
            print("")
        return True
    else:
        dl_id_n = 0
        for dest, entries in entries_dict.items():
            if author_match(cmd_args[1], entries[0].author):
                print("Author: (" + str(dl_id_n) + ") " + entries[0].author)
                print("Download Location: " + dest)
                print("Unsaved Count: " + str(len(entries)))
                dl_id_a = 'a'
                for entry in entries:
                    print("|---- (" + str(dl_id_n) + str(dl_id_a) + ") " + entry.title)
                    print("|            * " + entry.published)
                    dl_id_a = chr(ord(dl_id_a) + 1)
                print("")
                return True
            
            dl_id_n += 1

    print("ERROR: ls could not be performed.")
    return False


# dl < author | author list | id | id list | all > < path_override : optional >
# examples `dl author1;author2;1;2;1a-1d /media/mitchell/Archive4_2000/youtubenew/brassagainst
def dl(entries_dict, cmd_args):
    if len(cmd_args) == 1:
        # dl all or quit?
        return False
    else:
        def get_to_downloads(target):
            dl_id_n = 0
            for dest, entries in entries_dict.items():
                if target[0] == str(dl_id_n):
                    dl_id_a = 'a'
                    for entry in entries:
                        if (str(dl_id_n) + str(dl_id_a)).upper() == target.upper():
                            return (dest, [entry])
                        dl_id_a = chr(ord(dl_id_a) + 1)
                elif not target[0].isnumeric() and author_match(target, entries[0].author):
                    return (dest, entries)
                dl_id_n += 1
            return ("", [])

        def parse_to_dl_arg(to_dl_arg):
            dl_targets = [to_dl_arg]
            if to_dl_arg.find(';') > 0:
                dl_targets = to_dl_arg.split(';')

            retList = []
            for target in dl_targets:
                if len(target) > 0:
                    retList.append(get_to_downloads(target))

            return retList

        #dest, entries = parse_to_dl_arg(cmd_args[1])
        pending_dls = parse_to_dl_arg(cmd_args[1])
        print(pending_dls)
        for dest, entries in pending_dls:
            if len(dest) > 0 and len(entries) > 0:
                os.makedirs(dest)
                os.chdir(dest)
                print("Downloading " + str(len(entries)) + " to " + dest)
                for dl in entries:
                    os.system(CMD_HQ + dl.link)
                return True

    print("ERROR: dl could not be performed.")
    return False


def process_command_input(entries_dict, cmd):
    cmd_args = cmd.split(' ')
    if len(cmd_args) == 0:
        return False

    if cmd_args[0] in ['q', 'quit', 'exit']:
        quit()
    elif cmd_args[0] in ['l', 'ls', 'list']:
        ls(entries_dict, cmd_args)
    elif cmd_args[0] in ['d', 'dl', 'download']:
        dl(entries_dict, cmd_args)
    elif cmd_args[0] in ['s', 'sp', 'set', 'setp', 'setpath', 'setdlpath']:
        set_download_path(entries_dict, cmd_args)

    return False
