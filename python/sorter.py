# -*- coding: utf-8 -*-

import enum, copy, unicodedata

"""
 * Convert {string} from UTF-8 with accents to plain ASCII
 * @param  {string} value String to be normalized
 * @return {string}       Normalized string
"""
def normalize (value):
    # Normalizes the UTF-8 string
    normalized = unicodedata.normalize('NFD', value)
    # Converts the string to ASCII ignoring accents
    ascii_value = normalized.encode('ASCII', 'ignore')
    return ascii_value

class SortingServiceException (Exception):

    """ Manages SortingServiceException """

class Sorter:

    """ Sorts a list of dictionaries by rules """

    # List of tuples containing ( rule_field, rule_order )
    __rules = []

    """
     * Insert a new rule to sort
     * @param {string}  rule_field Name of the field to use
     * @param {boolean} rule_reverse If this ordering is reverse
    """
    def addRule (self, rule_field, rule_reverse):
        self.__rules.append( ( rule_field, rule_reverse ) );

    def sortedIndexes (self, data):

        # List of indexes
        indexes = []
        # List of the entries normalized
        normalized_entries = []

        # Fill the lists
        for index, entry in enumerate(data):

            # Create a new dictionary of normalized values
            normalized_entry = {
                key: normalize(str(value)) for key, value in entry.items()
            }

            # Append normalized entry and index to lists
            normalized_entries.append(normalized_entry)
            indexes.append( index )

        # Python 'sorted' function is stable, so the previous ordering is not
        # affected by this ordering when the values are equal
        for rule_field, rule_reverse in reversed(self.__rules):
            # Sort by the rule
            indexes = sorted(indexes,
                key = lambda x: normalized_entries[ x ][ rule_field ],
            reverse = rule_reverse)

        return indexes
