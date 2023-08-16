# fasta_processing.py

import pandas as pd

def extract_mapping_from_fasta(fasta_path):
    """
    Extract the mapping between sequence IDs and species names from a FASTA file.
    """
    with open(fasta_path, 'r') as f:
        lines = f.readlines()

    mapping = {}
    for line in lines:
        if line.startswith('>'):
            parts = line.split()
            seq_id = parts[0][1:]  # Remove '>'
            species_name = parts[-1][1:-1]  # Remove '[' and ']'
            mapping[seq_id] = species_name

    return mapping
