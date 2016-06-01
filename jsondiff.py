#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, json

if __name__ == "__main__":

    if len(sys.argv) > 2:

        # Open and parse JSON
        file_json = open(sys.argv[1], 'r')
        first_json = json.load(file_json)
        file_json.close()

        for f in range(1, len(sys.argv)):

            # Open and parse JSON
            file_json = open(sys.argv[ f ], 'r')
            next_json = json.load(file_json)
            file_json.close()

            # If dictionaries differ
            if next_json != first_json:
                print(json.dumps(next_json, indent = 4), file = sys.stderr)
                print('different from', file = sys.stderr)
                print(json.dumps(first_json, indent = 4), file = sys.stderr)
                sys.exit(1)

        sys.exit(0)

    sys.exit(1)
