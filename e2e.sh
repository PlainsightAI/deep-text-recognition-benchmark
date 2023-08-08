#!/bin/bash

# Check if at least one argument is given
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <DATASET_PATH>"
    exit 1
fi

DATASET_PATH="$1"
BASE_NAME=$(basename "$DATASET_PATH" .zip)  # Assuming the DATASET_PATH ends in .zip
SENSE_CONVERTED=./dataset/$BASE_NAME

# Call the first Python script with the provided DATASET_PATH
python3 sense_to_intermediate_format.py "$DATASET_PATH" 2>&1 | tee log.txt

# Check if the first script ran successfully
if [ $? -ne 0 ]; then
    echo "Error occurred during the execution of sense_to_intermediate_format.py!"
    exit 2
fi

# Call the second Python script with the derived paths
python3 create_lmdb_dataset.py --inputPath "$SENSE_CONVERTED" --gtFile "$SENSE_CONVERTED/gt.txt" --outputPath result/

# Check if the second script ran successfully
if [ $? -ne 0 ]; then
    echo "Error occurred during the execution of create_lmdb_dataset.py!"
    exit 3
fi

echo "Both scripts executed successfully!"

