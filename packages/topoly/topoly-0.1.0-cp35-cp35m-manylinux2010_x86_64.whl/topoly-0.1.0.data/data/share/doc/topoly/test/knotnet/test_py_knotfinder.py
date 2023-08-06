#!/usr/bin/python3
import sys

from topoly_knot import find_knots
#from topoly_preprocess import chain_read

if __name__ == "__main__":
    # arg 1 - input file path
    # arg 2 - output file path
    print("Testing PY KnotFinder")
 #   read, unable = chain_read(sys.argv[1].encode('utf-8'))
    #read, unable = chain_read("blabla".encode('utf-8'))
#    print("unable: " + str(unable))
#    print(str(read))
    ret = find_knots(sys.argv[1].encode('utf-8'), sys.argv[2].encode('utf-8'), 2)
    print(str(ret))
