#!/bin/bash

# Enable php test
ENABLE_PHP=0
# Enable javascript test
ENABLE_JAVASCRIPT=0
# Enable python test
ENABLE_PYTHON=0

# Install dependencies
INSTALL_DEPS=0

# Output file
TMP_OUT=$(mktemp)
# Number of available tests
NUM_TESTS=50

# Turns the output red
RED=$(tput setaf 1)
# Turns the output green
GREEN=$(tput setaf 2)
# Reset output
RESET=$(tput sgr0)

# Detect arguments
for arg in "${@}"; do
    case "${arg}" in
        "-php") ENABLE_PHP=1 ;;
        "-js") ENABLE_JAVASCRIPT=1 ;;
        "-python") ENABLE_PYTHON=1 ;;
        "--install-deps") INSTALL_DEPS=1 ;;
    esac
done

if [ "${INSTALL_DEPS}" = "1" ]; then
    # Install php deps
    if [ "${ENABLE_PHP}" = "1" ]; then
        sudo apt-get install php5 php5-json
    fi

    # Install javascript deps
    if [ "${ENABLE_JAVASCRIPT}" = "1" ]; then
        sudo apt-get install npm -y
        sudo npm cache clean -f
        sudo npm install -g n
        sudo n stable
    fi
fi

# Test in range [ 0, NUM_TESTS )
for i in $(seq 0 $((${NUM_TESTS} - 1))); do

    # JavaScript test
    if [ "${ENABLE_JAVASCRIPT}" = "1" ]; then
        node javascript/main.js tests/rules/test_${i}_rules.json \
            tests/entries/test_${i}_entries.json > ${TMP_OUT}

        if ! python3 jsondiff.py tests/outputs/output_${i}.json ${TMP_OUT}; then
            echo ${RED} JavaScript errored at test ${i} ${RESET}
            rm -f ${TMP_OUT}
            exit -1
        else
            echo ${GREEN} JavaScript passed test ${i} ${RESET}
        fi
    fi

    # PHP test
    if [ "${ENABLE_PHP}" = "1" ]; then
        php php/main.php tests/rules/test_${i}_rules.json \
            tests/entries/test_${i}_entries.json > ${TMP_OUT}

        if ! python3 jsondiff.py tests/outputs/output_${i}.json ${TMP_OUT}; then
            echo ${RED} PHP errored at test ${i} ${RESET}
            rm -f ${TMP_OUT}
            exit -1
        else
            echo ${GREEN} PHP passed test ${i} ${RESET}
        fi
    fi

    # Python test
    if [ "${ENABLE_PYTHON}" = "1" ]; then
        python3 python/main.py tests/rules/test_${i}_rules.json \
            tests/entries/test_${i}_entries.json > ${TMP_OUT}

        if ! python3 jsondiff.py tests/outputs/output_${i}.json ${TMP_OUT}; then
            echo ${RED} Python errored at test ${i} ${RESET}
            rm -f ${TMP_OUT}
            exit -1
        else
            echo ${GREEN} Python passed test ${i} ${RESET}
        fi
    fi
done

rm -f ${TMP_OUT}
echo ${GREEN} All tests passed ${RESET}
