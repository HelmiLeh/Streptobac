#!/bin/bash

# Use all available CPU cores
cpus=$(nproc)

# Create a directory for GFFs if it doesn't exist
mkdir -p gffs

# Create a directory for Prokka output
mkdir -p out_prokka

# Loop through all files in the genomes directory
for genome_path in genomes/*.fasta; do
    # Extract filename without extension
    genome=$(basename "$genome_path" .fasta)
    
    # Run Prokka
    prokka --cpus $cpus --kingdom Bacteria --locustag "$genome" --addgenes --prefix "$genome" "$genome_path"
    
    # Move GFF to gffs directory
    cp "$genome/$genome.gff" gffs/
    
    # Move Prokka output to out_prokka directory
    mv "$genome" out_prokka/
done

# List files in the gffs directory
ls gffs
