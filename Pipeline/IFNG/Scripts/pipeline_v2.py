import os
import csv
import pandas as pd
from Bio import SeqIO

def create_species_mapping(fasta_file):
    species_mapping = {}
    records = list(SeqIO.parse(fasta_file, "fasta"))
    for record in records:
        identifier = record.id
        species = record.description.split("[")[-1].split("]")[0]
        species_mapping[identifier] = species
    return species_mapping

def save_mapping_to_csv(mapping, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Identifier", "Species"])
        for identifier, species in mapping.items():
            writer.writerow([identifier, species])

def read_distance_matrix(filename, species_mapping):
    distances = {}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            identifier_a, identifier_b = parts[0], parts[1]
            species_a, species_b = species_mapping[identifier_a], species_mapping[identifier_b]
            key = (species_a, species_b) if species_a < species_b else (species_b, species_a)
            distances[key] = float(parts[2])
    return distances

def main():
    input_folder = './'  # pasta onde os arquivos fasta e as saídas do RAxML estão localizados
    global_df = pd.DataFrame()

    for fasta_file in os.listdir(input_folder):
        if fasta_file.endswith('.fasta'):
            gene_name = fasta_file.split('.')[0]
            raxml_output = f'RAxML_distances.{gene_name}_matrix'
            mapping_file = f'{gene_name}_species.csv'
            
            species_mapping = create_species_mapping(fasta_file)
            save_mapping_to_csv(species_mapping, mapping_file)
            
            distances = read_distance_matrix(raxml_output, species_mapping)
            df = pd.DataFrame(list(distances.items()), columns=['Species Pair', gene_name])
            df.set_index('Species Pair', inplace=True)
            global_df = pd.merge(global_df, df, left_index=True, right_index=True, how='outer')
    
    global_df.to_csv('combined_distances.csv')

if __name__ == "__main__":
    main()
