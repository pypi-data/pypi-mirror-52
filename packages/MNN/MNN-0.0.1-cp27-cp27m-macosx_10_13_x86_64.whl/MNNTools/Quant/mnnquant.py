# Copyright @ 2019 Alibaba. All rights reserved.
# Created by ruhuan on 2019.08.31
""" python wrapper file for mnn quant tool """
from __future__ import print_function
import os
import sys
import Tools
def usage():
    """ print usage info """
    print("Usage: mnnquant src.mnn dst.mnn config.json")
    print("see more detail in https://www.yuque.com/mnn/en/tool_quantize")
def main():
    """ main function """
    argv = sys.argv
    if len(argv) != 4:
        usage()
        return -1
    src_mnn = argv[1]
    dst_mnn = argv[2]
    config_json = argv[3]
    if not os.path.exists(src_mnn):
        usage()
        return -1
    if not os.path.exists(config_json):
        usage()
        return -1
    Tools.mnnquant(src_mnn, dst_mnn, config_json)
    return 0
if __name__ == "__main__":
    main()
