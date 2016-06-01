#!/bin/bash

if [ "${1}" = '--install-deps' ]; then
    sudo apt-get install php5 php5-json npm -y
    sudo npm cache clean -f
    sudo npm install -g n
    sudo n stable
fi

# Output file
TMP_OUT=$(mktemp)
# Number of available tests
NUM_TESTS=1

# Turns the output red
RED=$(tput setaf 1)
# Turns the output green
GREEN=$(tput setaf 2)
# Reset output
RESET=$(tput sgr0)

for i in $(seq 1 ${NUM_TESTS}); do

    # JavaScript test
    node javascript/main.js tests/test_${i}_rules.json \
        tests/test_${i}_entries.json > ${TMP_OUT}

    if ! ./jsondiff.py tests/output_${i}.txt ${TMP_OUT}; then
        echo ${RED} JavaScript errored at test ${i} ${RESET}
        rm -f ${TMP_OUT}
        exit -1
    else
        echo ${GREEN} JavaScript passed test ${i} ${RESET}
    fi

    # PHP test
    php php/main.php tests/test_${i}_rules.json tests/test_${i}_entries.json > \
        ${TMP_OUT}

    if ! ./jsondiff.py tests/output_${i}.txt ${TMP_OUT}; then
        echo ${RED} PHP errored at test ${i} ${RESET}
        rm -f ${TMP_OUT}
        exit -1
    else
        echo ${GREEN} PHP passed test ${i} ${RESET}
    fi

    # Python test
    python3 python/main.py tests/test_${i}_rules.json \
        tests/test_${i}_entries.json > ${TMP_OUT}

    if ! ./jsondiff.py tests/output_${i}.txt ${TMP_OUT}; then
        echo ${RED} Python errored at test ${i} ${RESET}
        rm -f ${TMP_OUT}
        exit -1
    else
        echo ${GREEN} Python passed test ${i} ${RESET}
    fi
done

rm -f ${TMP_OUT}
echo ${GREEN} All tests passed ${RESET}
