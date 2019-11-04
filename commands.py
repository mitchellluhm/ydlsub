import sys

def author_match(search_author, entry_author):
    return search_author == entry_author or search_author in entry_author


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
        search_author = cmd_args[1].upper()
        dl_id_n = 0
        for dest, entries in entries_dict.items():
            entry_author = entries[0].author.upper()
            if author_match(search_author, entry_author):
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

    print("ERROR: ls could not be performed")
    return False


# dl < author | author list | id | id list | all > < path_override : optional >
# examples `dl author1;author2;1;2;1a-1d /media/mitchell/Archive4_2000/youtubenew/brassagainst
def dl(entries_dict, cmd_args):
    if len(cmd_args) == 1:
        # dl all or quit?
        return False
    else:
        def parse_to_dl_arg(to_dl_arg):
            dl_targets = to_dl_arg.split(';')
            for target in dl_targets:
                continue


        to_dl = parse_to_dl_arg(cmd_args[1])

    print("ERROR: dl could not be performed")
    return False

def process_command_input(entries_dict, cmd):
    cmd_args = cmd.split(' ')
    if len(cmd_args) == 0:
        return False

    if cmd_args[0] in ['q', 'quit', 'exit']:
        quit()
    elif cmd_args[0] in ['ls', 'list']:
        ls(entries_dict, cmd_args)
    elif cmd_args[0] in ['dl', 'download']:
        dl(entries_dict, cmd_args)

    return False
