<?php

// Enumeration for ordering types
abstract class Order {
    const ASC = 0;
    const DESC = 1;
};

// Manages SortingServiceException
class SortingServiceException extends Exception {

    /**
     * Constructs a new SortingServiceException
     * @param  string    $msg   Exception message
     * @param  integer   $code  Exception error code
     * @param  Exception $value Previous exception
     */
    public function __construct ($msg, $code = 0, $prev = NULL) {
        parent::__construct($msg, $code, $prev);
    }

    /**
     * Convert SortingServiceException to string
     * @return string Exception string representation
     */
    public function __toString () {
        return __CLASS__ . ': [' . $this->getCode() . ']: ' .
            $this->getMessage() . PHP_EOL;
    }

};

// Main sorting class, receives rules and sort a list of entries
class Sorter {

    /**
     * List of rules to use
     * @var array
     */
    private $rules = [];

    /**
     * Convert string from UTF-8 with accents to lowercase plain ASCII
     * @param  string $value String to be normalized
     * @return string        Normalized string
     */
    private static function normalize ($value) {
        // Set locale to en_US to standardize iconv
        setlocale(LC_ALL, 'en_US');
        // Convert encoding to UTF-8
        $value_utf8 = mb_convert_encoding($value, 'UTF-8',
            mb_detect_encoding($value));
        // Convert it to lowercase
        $value_lower = mb_strtolower($value_utf8);
        // Returns the string converted to ASCII with accents removed
        return iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $value_lower);
    }

    /**
     * Insert a new rule to sort
     * @param string  $rule_field    Name of the field to use
     * @param integer $rule_ordering Ordering type to use
     */
    public function addRule ($rule_field, $rule_ordering) {
        $this->rules[] = [
            'field' => $rule_field,
            'order' => $rule_ordering
        ];
    }

    /**
     * Recursive comparison function
     * @param  array   $data_one   Entry to compare with $data_two
     * @param  array   $data_two   Entry to compare with $data_one
     * @param  integer $rule_index Index of the rule being used in the $rules
     * array
     * @return integer            0 if equal, -1 if data_one should be before
     * data_two, 1 otherwise
     */
    public function compare ($data_one, $data_two, $rule_index = 0) {

        $result = 0;

        // Stop condition
        if ($rule_index < sizeof($this->rules)) {

            // Copy rule
            $rule_field = $this->rules[ $rule_index ][ 'field' ];
            $rule_ordering = $this->rules[ $rule_index ][ 'order' ];

            // Copy values to be compared
            $value_one = $data_one[ $rule_field ];
            $value_two = $data_two[ $rule_field ];

            // Compare strings by ordering
            if ($rule_ordering === Order::ASC) {
                $result = strcmp($value_one, $value_two);
            } elseif ($rule_ordering === Order::DESC) {
                $result = strcmp($value_two, $value_one);
            }

            if ($result === 0) {
                // Test next rule
                $result = $this->compare($data_one, $data_two, $rule_index + 1);
            }
        }

        return $result;
    }

    /**
     * Sort by inserted keys and return sorted indexes
     * @param  array $data List of entries to be sorted
     * @return array       List of keys for sorted data
     */
    public function sortedIndexes ($data) {

        $indexes = [];

        // Fill indexes with ordered and normalized values
        foreach ($data as $index => $entry) {
            $normalized_entry = [];

            foreach ($entry as $key => $value) {
                // Insert normalized inside same key
                $normalized_entry[ $key ] = Sorter::normalize($value);
            }
            
            $indexes[$index] = $normalized_entry;
        }

        // Sort using $this->compare
        uasort($indexes, [ $this, 'compare' ]);

        // Return only keys
        return array_keys($indexes);
    }
};
