#!/usr/bin/env python3

import sys, os

from .paratextTextPicker import process, showMsg

def main():

    if len(sys.argv) < 2:
        showMsg('Please supply the name of a definition/configuration file.')
        showMsg('Exiting ...')
        exit()

    cfile = sys.argv[1]

    if not(os.path.exists(cfile)):
        showMsg("Definition/configuration file not found!")
        showMsg('Exiting ...')
        exit()

    process(cfile)

    print("[*]: Finished!")

if __name__ == '__main__':
    main()
