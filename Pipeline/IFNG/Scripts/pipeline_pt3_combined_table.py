import pandas as pd
from Bio import SeqIO

def load_mapping(csv_file):
    """Load the mapping from sequence identifier to species name."""
    df = pd.read_csv(csv_file)
    return dict(zip(df['Identifier'], df['Species']))

def construct_distance_table(matrix_file, species_mapping, gene_name):
    """Construct a DataFrame with species pairs and genetic distances."""
    distances = {}
    with open(matrix_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            identifier_a, identifier_b, distance = parts[0], parts[1], float(parts[2])
            species_a = species_mapping.get(identifier_a, identifier_a)
            species_b = species_mapping.get(identifier_b, identifier_b)
            key = (species_a, species_b)
            distances[key] = distance

    df = pd.DataFrame.from_dict(distances, orient='index', columns=[gene_name])
    return df

def main():
    # Load the species mapping
    species_mapping = load_mapping('IFNG_species.csv')

    # Construct the distance table
    matrix_file = 'RAxML_distances.IFNG_matrix'  # This should be the path to your RAxML matrix file
    gene_name = 'IFNG'  # Name of the gene
    df = construct_distance_table(matrix_file, species_mapping, gene_name)

    # Save the resulting table
    df.to_csv('distances_table.csv')

if __name__ == "__main__":
    main()

