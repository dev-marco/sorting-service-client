# Sorting Service Client [![Build Status](https://travis-ci.org/dev-marco/sorting-service-client.svg?branch=master)](https://travis-ci.org/dev-marco/sorting-service-client)

## Setup instructions
Here are implemented 3 versions of the requisited code, one in PHP, other in Python and another in JavaScript (NodeJS). They may look the same (inputs, outputs, portions of code), but in each there are new challenges according to the language specificity.
### Requeriments
#### PHP
Requires PHP 5.6+
##### Installation (Ubuntu)
```bash
sudo apt-get install php5
```

#### Python
Requires Python 3.0+
##### Installation (Ubuntu)
```bash
sudo apt-get install python3
```

#### JavaScript
Requires NodeJS 5.0+
##### Installation (Ubuntu)
```bash
sudo apt-get install npm -y
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
```

### Input
The three versions accept inputs in the following formats:
#### Rules
JSON file containing a list of objects in order of importance.

##### Example
```
[
    {
        "field": "field_0_name",
        "order": "ASC_or_DESC"
    },
    {
        "field": "field_1_name",
        "order": "ASC_or_DESC"
    },
    ...
    {
        "field": "field_N_name",
        "order": "ASC_or_DESC"
    }
]
```

Where `field_*_name` is the name of the field to use and `ASC_or_DESC` is one of:
* ASC: order `field_*_name` from lowest to highest
* DESC: order `field_*_name` from highest to lowest
 
The rules are tested in order of appearance, meaning that the first rule will have more importance than the second and so on. Other examples of rules can be found in `tests/rules/`.

#### Entries
JSON file containing a list of objects in no specific order.

##### Example
```
[
    {
        "field_name_0": "element_0_field_0",
        "field_name_1": "element_0_field_1",
        ...
        "field_name_N": "element_0_field_N"
    },
    {
        "field_name_0": "element_1_field_0",
        "field_name_1": "element_1_field_1",
        ...
        "field_name_N": "element_1_field_N"
    },
    ...
    {
        "field_name_0": "element_N_field_0",
        "field_name_1": "element_N_field_1",
        ...
        "field_name_N": "element_N_field_N"
    }
]
```

Where `field_name_*` is the name of the field and `element_*_field_*` is the value of the field for this element.
Other examples of rules can be found in `tests/entries/`.

##### Important
PHP, JavaScript and Python (especially the last) uses different sorting methods, so the results may vary mainly according to sort stability ([Python sort is stable](https://docs.python.org/2/library/functions.html#sorted), [PHP sort is not](https://secure.php.net/manual/en/function.uasort.php), [JavaScript leaves undefined](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort)).

### Output
JSON file containing the indexes of the entries after sort.

#### Example
```
[
    2,
    5,
    1,
    0,
    4,
    3
]
```

Where every index references an entry. In that case `2` should be the first element after sort, `5` should be next and so on.
Other examples of outputs can be found in `tests/outputs/`.

## 3rd Party Packages
There are no extra 3rd party packages except those shipped with the language (for example, php5-json is installed with php5). If there is any problem with package requirements you can always use the `test.sh` script with `--install-deps` and the packages you want to install (`-php`, `-js` or `-python`)

## Run commands
### PHP
```bash
php php/main.php rules_file entries_file
```
### Python
```bash
python3 python/main.py rules_file entries_file
```
### JavaScript
```bash
node javascript/main.js rules_file entries_file
```

In all the commands the output is printed to the screen. You can always redirect the output using `>`.

## Other
### Tests
There is a shell script `test.sh` that tests inputs and compare with another *valid* output. It does so by running the code and comparing the output as a dictonary to the *valid* output.
It will find all `tests/rules/test_N_rules.json` matching `tests/entries/test_N_entries.json` and `tests/outputs/output_N.json` (where N is an incremental number from 0 without leading zeros) and execute this test case for the selected languages.
As stated before, outputs could be different as the stability of the sort function is not the same for the languages.
#### Command
```bash
bash test.sh [-php] [-js] [-python] [--install-deps]
```
#### Parameters
* `-php`: test php implementation
* `-js`: test javascript implementation
* `-python`: test python implementation
* `--install-deps`: auto install dependencies on Ubuntu for the required languages (and test)

The flags can be used in any order.

The `tests/` folder is supplied with 50 inputs (rules and entries) and 50 outputs (results of the python build) and an input generator `maketest.py`. It generates random inputs and saves these on their respective folders to be be tested with `test.sh`.
#### Command
```bash
python3 maketest.py NUM
```
#### Parameters
* `NUM`: number of inputs to generate

#### Naming
##### Rules
Rules are placed on `tests/rules` folder with the name `test_N_rules.json` where N is the number of the test (matches entry and output)
##### Entries
Entries are placed on `tests/entries` folder with the name `test_N_entries.json` where N is the number of the test (matches rule and output)
##### Outputs
Outputs are placed on `tests/outputs` folder with the name `output_N.json` where N is the number of the test (matches entry and rule)

#### Important
`maketest.py` only generates inputs, the outputs should be computed and stored on their respective path.

### Travis CI
This build has a `.travis.yml` and is linked to Travis CI, who tests it automatically using the default tests supplied. 
