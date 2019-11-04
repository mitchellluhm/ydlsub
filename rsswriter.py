import sys
# user: https://www.youtube.com/feeds/videos.xml?user=smtown
# id  : https://www.youtube.com/feeds/videos.xml?channel_id=smtown
base_url_channel = "https://www.youtube.com/feeds/videos.xml?channel_id="
base_url_user = "https://www.youtube.com/feeds/videos.xml?user="
channel = "/channel/"
user = "/user/"

if len(sys.argv) != 3:
    print("Incorrect number of program arguments")
    sys.exit()

if sys.argv[1] == sys.argv[2]:
    print("Arguments are the same")
    sys.exit()

input_lines = []
with open(sys.argv[1], 'r') as input_f:
    input_lines = input_f.readlines()

lines_to_write = []
for line in input_lines:
    l = line.strip()
    i = l.find(channel)
    if i > 0:
        feed_url = base_url_channel + l[i + len(channel):]
        lines_to_write.append(feed_url)
        continue

    i = l.find(user)
    if i > 0:
        feed_url = base_url_user + l[i + len(user):]
        lines_to_write.append(feed_url)

for l in lines_to_write:
    print(l)

# dont write lines already in output file
'''
with open(sys.argv[2], 'a') as output_f:
    output_f.writelines(lines_to_write)
    '''
