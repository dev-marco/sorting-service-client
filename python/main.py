#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sorter, json, sys

"""
 * Read json by filename
 * @param  string       Name of the file containing JSON
 * @return {dict|None}  Dictionary generated from JSON or None on error
"""
def jsonFromFileName (filename):
    json_file = open(filename, 'r')

    try:
        rules = json.load(json_file)
    except:
        rules = None
    finally:
        # Ensures that the file is closed
        json_file.close()

    return rules

# test if is the current running script
if __name__ == "__main__":

    # if has enough arguments
    if len(sys.argv) > 2:

        sort = sorter.Sorter()
        rules = jsonFromFileName(sys.argv[1])

        if rules is None:
            # NULL rules exception
            raise sorter.SortingServiceException('Rules set is null.')

        result = []

        if len(rules) > 0:

            # Parse rules to Sorter
            for rule in rules:
                reverse = True if rule['order'] == 'DESC' else False
                sort.addRule(rule['field'], reverse)

            entries = jsonFromFileName(sys.argv[2])

            # Sort result
            result = sort.sortedIndexes(entries)

        # Print result as a json encoded string
        print(json.dumps(result))
