import argparse
import csv
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a mapping from sequence identifiers to species names using a FASTA file.")
    parser.add_argument('fasta_file', type=str, help="Path to the FASTA file.")
    args = parser.parse_args()

    gene_name = args.fasta_file.split('.')[0]
    output_csv = f"{gene_name}_species.csv"

    mapping = create_species_mapping(args.fasta_file)
    save_mapping_to_csv(mapping, output_csv)
    print(f"Mapping saved to {output_csv}")

