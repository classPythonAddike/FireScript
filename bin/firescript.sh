#!/bin/bash

COMMAND=$1
FILE=$2

case $COMMAND in
    build)
        python -m bin.parse $FILE
    ;;
    *)
        echo "Invalid command!"
        echo "Valid commands are -"
        echo "   1) build <file>"
    ;;
esac
