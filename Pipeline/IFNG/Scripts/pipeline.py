import os
import pandas as pd
import csv


def create_species_mapping_from_fasta(fasta_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f"python3 {script_dir}/create_species_mapping.py {fasta_file}")


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


def read_distance_matrix(raxml_output, species_mapping):
    distances = {}
    with open(raxml_output, 'r') as f:
        for line in f.readlines()[1:]:
            parts = line.strip().split()
            identifier_a, identifier_b = parts[0], parts[1]
            species_a, species_b = species_mapping[identifier_a], species_mapping[identifier_b]
            distance = float(parts[2])
            key = (species_a, species_b)  # use a tuple as the key
            distances[key] = distance
    return distances


def main():
    fasta_files = [f for f in os.listdir() if f.endswith('.fasta')]

    for fasta_file in fasta_files:
        gene_name = fasta_file.split('.')[0]

        # Generate species mapping for this gene
        create_species_mapping_from_fasta(fasta_file)

        species_mapping = read_species_mapping(gene_name)
        raxml_output = f"RAxML_distances.{gene_name}_matrix"

        if not os.path.exists(raxml_output):
            continue

        distances = read_distance_matrix(raxml_output, species_mapping)

        df = pd.DataFrame.from_dict(
            distances, orient='index', columns=[gene_name])
        df.index.names = ['Species pair']

        if not os.path.exists('distances_table.csv'):
            df.to_csv('distances_table.csv')
        else:
            try:
                existing_df = pd.read_csv('distances_table.csv', index_col=0)

                # Identifique os índices problemáticos
                problematic_indices = [
                    idx for idx in existing_df.index if len(idx.split('-')) != 2
                ]

                # Imprima os índices problemáticos para verificar
                print(f"Problematic indices: {problematic_indices}")

                # Se não houver índices problemáticos, prossiga com a criação do MultiIndex
                if not problematic_indices:
                    existing_df.index = pd.MultiIndex.from_tuples(
                        [tuple(idx.split('-')) for idx in existing_df.index], 
                        names=['Species A', 'Species B']
                    )
            except FileNotFoundError:
                existing_df = pd.DataFrame()

        merged_df = existing_df.merge(
            df, left_index=True, right_index=True, how='outer')
        merged_df.to_csv('distances_table.csv')


if __name__ == "__main__":
    main()

