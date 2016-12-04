class hershey_char(object):
    """A single Hershey character"""
    def __init__(self,char_data=None):
        self.index=int(char_data[0:5])
        self.vertices=int(char_data[5:8])
        self.left=ord(char_data[8])-ord('R')
        self.right=ord(char_data[9])-ord('R')
        vector_src=char_data[10:]
        vectors=[]

        originx = 50
        originy = 50

        draw_flag = False        
        stroke=[]

        for xy in range(0,len(vector_src),2):
            vector = vector_src[xy:xy+2]
            if vector == " R":
                draw_flag = False
                vectors.append(tuple(stroke))
                stroke=[]
            else:
                x = originx + ord(vector[0])-ord('R')
                y = originy + ord(vector[1])-ord('R')
                stroke.append(x)
                stroke.append(y)
                draw_flag = True

        vectors.append(tuple(stroke))
        self.vectors=tuple(vectors)
        

def parse_hershey_file(filename):
    chars = {}
    f = open(filename)
    lines = f.readlines()
    f.close()
    lines.append(' ')
    line = ''
    for i in range(len(lines)-1):
        line = line + lines[i].rstrip()
        if lines[i+1][0] == " " and lines[i+1][:2] != " R":
            c = hershey_char(line)
            chars[c.index]=c
            line = ''
    
    return chars


roman_chars = parse_hershey_file("hershey")
japanese_chars = parse_hershey_file("japanese")

print("Parsed Hershey data.")