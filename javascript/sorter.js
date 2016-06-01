'use strict';

// Enumeration for ordering types
const Order = Object.freeze({
    'ASC': 0,
    'DESC': 1
});

// Manages SortingServiceException
class SortingServiceException {

    /**
     * Constructs a new SortingServiceException
     * @param  {string}  msg   Exception message
     */
    constructor (msg) {
        // Initializes the error
        Error.captureStackTrace(this, this.constructor);
        this.name = this.constructor.name;
        this.message = msg;
    }

};

// Main sorting class, receives rules and sort a list of entries
class Sorter {

    /**
     * Initializes sorter variables
     */
    constructor () {
        // List of rules to use
        this.rules = [];
    };

    /**
     * Insert a new rule to sort
     * @param {string}  rule_field    Name of the field to use
     * @param {integer} rule_ordering Ordering type to use
     */
    addRule (rule_field, rule_ordering) {
        this.rules.push({ 'field': rule_field, 'order': rule_ordering });
    };

    /**
     * Sort by inserted rules and return sorted indexes
     * @param  {array} data List of entries to be sorted
     * @return {array}      List of keys for sorted data
     */
    sortedIndexes (data) {

        // Saves 'this' in a variable because it will change in anonymous
        // function
        const sorter = this;
        var indexes = [];

        // Fills the array of indexes
        for (var ind in data) {
            // Method Object.keys and this loop returns only string keys,
            // so this should convert it to integer
            indexes.push(parseInt(ind));
        }

        indexes.sort(
            /**
             * Function to compare two entries
             * @param  {object}  index_one Index of the entry to compare to
             * entry at index_two
             * @param  {object}  index_two Index of the entry to compare to
             * entry at index_one
             * @return {integer}           0 if equal, -1 if index_one should be
             * before index_two, 1 otherwise
             */
            function (index_one, index_two) {
                var result = 0, rule_index = 0;

                do {

                    // Copies properties from objects
                    const
                        rule_field = sorter.rules[ rule_index ].field,
                        rule_ordering = sorter.rules[ rule_index ].order,
                        value_one = data[ index_one ][ rule_field ],
                        value_two = data[ index_two ][ rule_field ];

                    // Make comparison taking order and locale in account
                    if (rule_ordering === Order.ASC) {
                        result = value_one.localeCompare(value_two);
                    } else if (rule_ordering === Order.DESC) {
                        result = value_two.localeCompare(value_one);
                    }

                    // Next rule
                    ++rule_index;

                // If result is not zero, then we found two different fields
                } while (result === 0 && rule_index < sorter.rules.length);

                return result;
            }
        );

        return indexes;
    };
};

// Export the created modules to nodejs
module.exports = {
    'Order': Order,
    'SortingServiceException': SortingServiceException,
    'Sorter': Sorter
};
