# Copyright @ 2019 Alibaba. All rights reserved.
# Created by ruhuan on 2019.08.31
""" get mnn supported ops """
from __future__ import print_function
import os
import sys
import MNNTools.Utils.OpName as OpName
def usage():
    """ print usage info """
    print("Usage: mnnops")
    print("see more detail in https://www.yuque.com/mnn/en/mnnops")
def main():
    """ main function """
    print("mnn supported ops:\n")
    for name in OpName.op_dict.values():
        print(name + "\n")
    return 0
if __name__ == "__main__":
    main()
