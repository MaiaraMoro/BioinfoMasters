import os
import pandas as pd
import csv
import sys

def create_species_mapping_from_fasta(fasta_file, gene_name):
    os.system(f"python3 create_species_mapping.py {fasta_file}")

def read_species_mapping(gene_name):
    csv_file = f"{gene_name}_species.csv"
    species_mapping = {}
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            identifier, species = row
            species_mapping[identifier] = species
    return species_mapping

def construct_distance_table(matrix_file, species_mapping, gene_name):
    distances = {}
    with open(matrix_file, 'r') as f:
        for line in f.readlines()[1:]:
            parts = line.strip().split()
            identifier_a, identifier_b = parts[0], parts[1]
            species_a, species_b = species_mapping.get(identifier_a, identifier_a), species_mapping.get(identifier_b, identifier_b)
            distance = float(parts[2])
            key = f"{species_a} - {species_b}"  # use a string as the key
            distances[key] = distance
    df = pd.DataFrame.from_dict(distances, orient='index', columns=[gene_name])
    return df

def update_csv_with_new_data(df, gene_name):
    if os.path.exists('distances_table.csv'):
        existing_df = pd.read_csv('distances_table.csv', index_col='Species pair')

        # If the column for the specific gene exists, update its values
        if gene_name in existing_df.columns:
            existing_df[gene_name] = df[gene_name]
        # Otherwise, add the new column
        else:
            existing_df = pd.concat([existing_df, df], axis=1)
            
        existing_df.to_csv('distances_table.csv')
    else:
        df.index.name = 'Species pair'
        df.to_csv('distances_table.csv')

def main(input_fasta):
    gene_name = os.path.basename(input_fasta).split('.')[0]
    matrix_file = f"RAxML_distances.{gene_name}_matrix"

    create_species_mapping_from_fasta(input_fasta, gene_name)
    species_mapping = read_species_mapping(gene_name)

    if not os.path.exists(matrix_file):
        print(f"RAxML matrix file {matrix_file} does not exist. Exiting.")
        sys.exit()

    df = construct_distance_table(matrix_file, species_mapping, gene_name)
    update_csv_with_new_data(df, gene_name)

if __name__ == "__main__":
    main(sys.argv[1])

