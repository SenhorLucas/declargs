#!/bin/bash
main() {
    tmp=$(mktemp -dt simple_app.XXXXXX)
    (
        cd "$tmp" || exit
        local -r expected=$'arg\nTrue'
        local -ar cmd1=(simple_app arg --some-kwarg)
        local -ar cmd2=(python3 -m simple_app arg --some-kwarg)

        run_test "$expected" "${cmd1[@]}"
        run_test "$expected" "${cmd2[@]}"
    )
}

run_test() {
    local -r expected=$1
    shift
    local -ar command=("$@")
    local -r output=$("${command[@]}")

    echo "Running: ${command[*]}"
    if [[ "$output" != "$expected" ]]; then
        echo "Test failed"
        echo "Expected: $expected"
        echo "Got: $output"
        exit 1
    fi
}

main
