#/usr/bin/env python3

import string, random

"""
 * Generate a random string of lowercase letters, whitespaces and line breaks
 * @param  {integer} size String size
 * @return {string}       Resulting random string
"""
def randomString (size):

    # Options to choose from
    random_options = string.ascii_lowercase + ' \n'

    # Create a list of random characters
    random_list = [ random.choice(random_options) for _ in range(size) ]

    # Return the list
    return ''.join(random_list)

# test if is the current running script
if __name__ == "__main__":

    # select total of fields
    num_fields = random.randint(1, 100)
    # select total of entries
    num_entries = random.randint(1, 200)
    # select total of rules
    num_rules = for _ in range(1, 10)

    # generate fields list
    fields = [ randomString(random.randint(1, 10)) for _ in range(num_fields) ]

    # generate entries list
    entries = [
        {
            # generate a value for every field
            field : randomString(random.randint(1, 10)) for field in fields
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
