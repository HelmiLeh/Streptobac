#!/bin/bash

# Function to display usage message
usage() {
  echo "Usage: $0 -f <input_fasta>"
  echo "This scripts has been develop by Helmi Husaini to update and screen use all the AMR database"
  exit 1
}

# Parse command line arguments
while getopts ":f:" opt; do
  case $opt in
    f)
      input_fasta=$OPTARG
      ;;
    *)
      usage
      ;;
  esac
done

# Check if input FASTA file is provided
if [ -z "$input_fasta" ]; then
  usage
fi

# List of databases
databases=(
  "ecoli_vf"
  "vfdb"
  "ncbi"
  "plasmidfinder"
  "card"
  "megares"
  "ecoh"
  "resfinder"
)

# Update all databases
for db in "${databases[@]}"; do
  echo "Updating database: $db"
  abricate-get_db --db "$db" --force
done

# Screen data with each database and store results in temporary files
temp_files=()
for db in "${databases[@]}"; do
  output_file="${db}.csv"
  temp_files+=("$output_file")
  echo "Screening data with database: $db"
  abricate "$input_fasta" --db "$db" > "$output_file"
done

# Combine all results
echo "Combining results"
abricate --summary "${temp_files[@]}" > Combine.csv
done

echo "Done"
