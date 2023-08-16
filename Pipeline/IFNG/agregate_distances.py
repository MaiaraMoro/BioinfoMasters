# aggregate_distances.py

import os
import pandas as pd
from fasta_processing import extract_mapping_from_fasta
from distance_processing import transform_distance_file_with_mapping

# Path to the directory containing gene subdirectories
dir_path = "~/Downloads/Analises-masters/Pipeline/"

# Check if the aggregated_distances.csv file already exists
if os.path.exists('aggregated_distances.csv'):
    aggregated_df = pd.read_csv('aggregated_distances.csv')
else:
    aggregated_df = pd.DataFrame(columns=['Pairs'])

# Loop through each gene's directory
for gene_dir in os.listdir(dir_path):
    gene_dir_path = os.path.join(dir_path, gene_dir)
    
    fasta_path = os.path.join(gene_dir_path, gene_dir + ".fasta")
    txt_path = os.path.join(gene_dir_path, "RAxML_distances.txt")
    
    # Extract the mapping for this gene
    mapping_dict = extract_mapping_from_fasta(fasta_path)
    mapping_df = pd.DataFrame(list(mapping_dict.items()), columns=['SpeciesID', 'Taxonomy'])

    # Transform the .txt file using the specific mapping
    transformed_df = transform_distance_file_with_mapping(txt_path, gene_dir, mapping_df)
    
    # Merge with the aggregated DataFrame
    aggregated_df = pd.merge(aggregated_df, transformed_df, on='Pairs', how='outer')

# Save the aggregated DataFrame
aggregated_df.to_csv('aggregated_distances.csv', index=False)
