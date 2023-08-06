# Copyright @ 2019 Alibaba. All rights reserved.
# Created by ruhuan on 2019.08.31
""" mnn tool summary entry """
from __future__ import print_function
import os
import sys
def usage():
    print("mnn toolsets has following command line tools")
    print("    $mnn")
    print("        list out the command line tools")
    print("    $mnnops")
    print("        get supported ops in mnn engine")
    print("    $mnnconvert")
    print("        convert other model file to mnn file")
    print("    $mnnquant")
    print("        quant a mnn model")
    print("    $mnnvisual")
    print("        write the mnn model structure to a pic file")
def main():
    """ main function """
    usage()    
    return 0
if __name__ == "__main__":
    main()
