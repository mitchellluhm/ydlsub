import sys

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
                            return [entry]
                        dl_id_a = chr(ord(dl_id_a) + 1)
                elif not target[0].isnumeric() and author_match(target, entries[0].author):
                    return entries

                
                dl_id_n += 1

        def parse_to_dl_arg(to_dl_arg):
            dl_targets = to_dl_arg.split(';')
            for target in dl_targets:
                if len(target) > 0:
                    entries_to_dl = get_to_downloads(target)
                    print(entries_to_dl[0].title)

        to_dl = parse_to_dl_arg(cmd_args[1])

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
