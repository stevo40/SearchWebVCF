import requests
import math

#string = "X"
#print(int(ord(string)))
#exit(0)

urlLocation = "https://sra-download.ncbi.nlm.nih.gov/srapub_files/SRZ189891_722g.990.SNP.INDEL.chrAll.vcf"
args = {}
downloaded = 100
size = 0

byte_map = []
byte_to_chrpos = {}

def setup():
    x = requests.head(urlLocation)
    size = int(x.headers["Content-Length"])
    #genetic_map.append(0)
    #genetic_map.append(size)

    # setup start (TODO: skip headers):
    start = closest_pair(0 + 200000)

    start_pos = start[0]
    byte_map.append(start_pos)
    byte_to_chrpos[start_pos] = start[1]

    # setup end (TODO: handle small chromosomes at the end of the file):
    end = closest_pair(size-100000)

    end_pos = end[0]
    byte_map.append(end_pos)
    byte_to_chrpos[end_pos] = end[1]


    print(byte_map)


def closest_pair(location):
    new_pos = scan_newline(location)
    pair = extract_chr_pos(new_pos)
    return new_pos, pair



def request_chunk(loc, chunk_size=10000):

    args["Range"] = "bytes=" + str(loc) + "-" + str(loc+chunk_size)

    x = requests.get(urlLocation, headers=args)

    #if (x.status_code==200):
    return(x.text)


def scan_newline(loc, chunk_size=10000, attempts=10):
    ''' Find first newline near block start '''

    for i in range(attempts):

        target_loc = loc + (i*chunk_size)

        chunk = request_chunk(target_loc)
        newline_position = chunk.find("\n")

        #print("iteration: " + str(i) + " location: " + str(target_loc) + " Newline pos: " + str(newline_position))

        if (newline_position>=0):
            return target_loc + newline_position + 1


def extract_chr_pos(loc):
    string = request_chunk(loc, chunk_size=50)
    return extract_chr_pos_from_str(string)

def extract_chr_pos_from_str(string):

    split_string = string.split("\t")
    chrom = split_string[0]

    if (chrom[0]=="c"):
        chrom = chrom.replace('chr', '')
    try:
        chrom = int(chrom)
    except:
        #print("oops")
        #print(chrom)
        #print(chrom[0])
        #print(ord(chrom))
        chrom = int(ord(chrom[0]))

    pos = int(split_string[1])
    return chrom, pos


def seek(chrom, pos):

    search_chrpos = (chrom, pos)

    done = False

    for iteration in range(40):

        if done:
            return

        print("Iteration:" + str(iteration))

        last_byte_pos = byte_map[0]
        last_chrpos = byte_to_chrpos[last_byte_pos]

        create_position = -1
        create_byte_pos = -1

        for i in range(1, len(byte_map)):

            byte_pos = byte_map[i]
            chrpos = byte_to_chrpos[byte_pos]

            #print(str(i) + " " + str(last_byte_pos) + " " + str(last_chrpos) + " " + str(byte_pos) + " " + str(chrpos)
            #      + " : " + str(search_chrpos))

            if last_chrpos <= search_chrpos < chrpos:
                # Need to insert at this position
                pos_difference = byte_pos - last_byte_pos
                # can use pos difference to figure out the match.

                if pos_difference < 50000:
                    done = True
                    show_byte_map()

                    sub_text = request_chunk(last_byte_pos, chunk_size=pos_difference)
                    sub_lines = sub_text.split("\n")
                    for line in sub_lines:
                        sub_chrpos = (-1, -1)
                        try:
                            sub_chrpos = extract_chr_pos_from_str(line)
                        except:
                            print("no chrpos")
                        #print (sub_chrpos)
                        #print(line)
                        if (sub_chrpos == search_chrpos):
                            return line


                    return ""

                create_byte_pos = int(last_byte_pos + math.ceil(pos_difference / 2))
                create_position = i

                #print(pos_difference)
                #print(create_byte_pos)
                print("Inserting at: " + str(create_position))

                break

            last_byte_pos = byte_pos
            last_chrpos = chrpos

        if create_position > 0:
            #print ("Creating:")
            new_position = closest_pair(create_byte_pos)

            byte_map.insert(create_position, new_position[0])
            byte_to_chrpos[new_position[0]] = new_position[1]

        #show_byte_map()
    # default return value:
    return ""






def show_byte_map():
    for i in range(0, len(byte_map)):
        byte_pos = byte_map[i]
        chrpos = byte_to_chrpos[byte_pos]

        print(str(i) + " " + str(byte_pos) + " " + str(chrpos))


setup()

# early chr1:
#location = 18740509905

#location = genetic_map[1]-100000
#location = 0 + 200000

#print(location)
#new_pos = scan_newline(location)
#pair = extract_chr_pos(new_pos)
#print(pair)

returns = seek(1, 22792776)
print("result:" + returns)
