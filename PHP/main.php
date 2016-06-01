<?php

    // Set UTF-8 as internal encoding
    mb_internal_encoding('UTF-8');

    require_once 'sorter.php';

    if (sizeof($argv) > 2) {
        $sort = new Sorter();
        $result = [];

        // Decode json from rules file
        $rules = json_decode(file_get_contents($argv[1]), true);

        // If JSON has an error, the result is NULL
        if ($rules !== NULL) {
            if (sizeof($rules)) {

                foreach ($rules as $rule) {
                    // Default ordering
                    $order = Order::ASC;

                    if ($rule[ 'order' ] == 'DESC') {
                        $order = Order::DESC;
                    }

                    // Add sorting rule
                    $sort->addRule($rule[ 'field' ], $order);
                }

                $entries = json_decode(file_get_contents($argv[2]), true);

                $result = $sort->sortedIndexes($entries);
            }
        } else {
            // NULL rules exception
            throw new SortingServiceException('Rules set is null.');
        }

        // Print the results as JSON
        echo json_encode($result), PHP_EOL;
    }
