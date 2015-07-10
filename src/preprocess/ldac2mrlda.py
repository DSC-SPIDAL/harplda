import sys
    
if __name__ == "__main__":    
    inp = open(sys.argv[1])
    outp = open(sys.argv[2],'w')

    docid = 0
    for line in inp:
        index = line.find(' ')
        outp.write("doc%d\t%s"%(docid, line[index+1:]))
        docid += 1
