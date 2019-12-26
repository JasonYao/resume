#!/usr/bin/env bash

set -e # Fails on the first error

###
# Helper functions
##

function info() {
    printf "\\t  [\\033[00;34mINFO\\033[0m] %s\\n" "${1}"
}

function user() {
    printf "\\t  [ \\033[0;33m??\\033[0m ] %s\\n" "${1}"
}

function success() {
    printf "\\t\\033[2K  [ \\033[00;32mOK\\033[0m ] %s\\n" "${1}"
}

function warn() {
    printf "\\t\\033[2K  [\\033[38:2:255:165:0mWARN\\033[0m] %s\\n" "${1}"
}

function fail() {
    printf "\\t\\033[2K  [\\033[0;31mFAIL\\033[0m] %s\\n" "${1}"
    exit 1
}
