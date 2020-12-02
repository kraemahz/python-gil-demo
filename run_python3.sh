#!/bin/bash -e
echo "Running python3... should not fail"
echo "with key error mutex"
for i in {0..100}; do
    python3 key_error.py
done
echo "passed"
echo "if check only"
for i in {0..100}; do
    python3 if_check.py
done
echo "passed"
