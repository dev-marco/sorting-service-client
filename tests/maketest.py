#!/usr/bin/env python3

import string, random, sys, json

"""
 * Generate a random string of lowercase letters, whitespaces and line breaks
 * @param  {integer} size String size
 * @return {string}       Resulting random string
"""
def randomStr (size):

    # Options to choose from
    random_options = string.ascii_lowercase + ' \n'

    # Create a list of random characters
    random_list = [ random.choice(random_options) for _ in range(size) ]

    # Return the list
    return ''.join(random_list)

# test if is the current running script
if __name__ == "__main__":

    if len(sys.argv) > 1:

        num_tests = int(sys.argv[1])

        for test in range(0, num_tests):

            # select total of fields
            num_fields = random.randint(1, 100)
            # select total of entries
            num_entries = random.randint(1, 200)
            # select total of rules
            num_rules = random.randint(1, 10)

            # generate fields list
            fields = [
                randomStr(random.randint(1, 10)) for _ in range(num_fields)
            ]

            # generate entries list
            entries = [
                {
                    # generate a value for every field
                    field : randomStr(random.randint(1, 10)) for field in fields
                } for _ in range(num_entries)
            ]

            # generate rules list
            rules = [
                {
                    # select a random field
                    # repetition is supported but it doesn't change results
                    'field': random.choice(fields),
                    # select a random ordem
                    'order': random.choice([ 'ASC', 'DESC' ])
                } for _ in range(num_rules)
            ]

            # write entries
            file_entries = open(
                'entries/test_' + str(test) + '_entries.json', 'w'
            )
            json.dump(entries, file_entries, indent = 4)
            file_entries.close()

            # write rules
            file_rules = open(
                'rules/test_' + str(test) + '_rules.json', 'w'
            )
            json.dump(rules, file_rules, indent = 4)
            file_rules.close()
