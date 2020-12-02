#!/bin/bash -e
echo "Running python2... should fail"
echo "with key error mutex"
for i in {0..100}; do
    python2 key_error.py
done
echo "passed"
echo "if check only"
for i in {0..100}; do
    python2 if_check.py
done
echo "passed"
