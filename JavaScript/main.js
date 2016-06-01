'use strict';

if (process.argv.length > 3) {

    // Import modules
    var sorter = require('./sorter.js'), fs = require('fs');

    var rules, sort = new sorter.Sorter();

    try {
        // Read and parse the JSON of the rules file synchronously
        rules = JSON.parse(fs.readFileSync(process.argv[2]));
    } catch (_) {
        // NULL rules exception
        throw new sorter.SortingServiceException('Rules set is null.');
    }

    // Default result for empty rules
    var result = [];

    if (rules.length > 0) {

        // Read and parse the JSON of the entries file synchronously
        var entries = JSON.parse(fs.readFileSync(process.argv[3]));

        for (var i in rules) {
            // Copies rule and sets the default ordering
            var rule = rules[ i ], order = sorter.Order.ASC;

            if (rule.order === 'DESC') {
                order = sorter.Order.DESC;
            }

            // Add new sorting rule
            sort.addRule(rule.field, order);
        }

        // Make the sort
        result = sort.sortedIndexes(entries);
    }

    // Log the results as JSON
    console.log(JSON.stringify(result));
}
