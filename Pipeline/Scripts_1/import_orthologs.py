import requests
import json
import csv

#function to fetch mammalian orthologs sequences using Ensembl API REST 
def fetch_orthologs (ensembl_id):
    server = "https://rest.ensembl.org"
    ext = f"/homology/id/{ensembl_id}?type=orthologues"
    headers = {"Content-Type": "application/json"}

    response = requests.get(server + ext, headers=headers)

    if not response.ok:
        response.raise_for_status()
        return
    
    decoded = response.json()
    mammalian_orthologs = []

    for homology in decoded.get("data", [])[0].get("homologies", []):
        target = homology.get("target", {})
        species = target.get("species", "")

        #filter to search for only mammalian species 
        if "mammalia" in species.lower():
            mammalian_orthologs.append({
                "Gene_ensembl_ID": ensembl_id,
                "Ortholog_Species": species,
                "Ortholog_Protein_ID": target.get("protein_id"),
                "Percentage_ID": homology.get("perc_id"),
                "Percentage_Pos": homology.get("perc_pos")
            })
    return mammalian_orthologs

#Load the list of genes from the csv file - obs the column with ensembl IDs must be called `ensembl`
gene_list = [] 
with open("/home/mra/Downloads/Analises-masters/Pipeline/Scripts_1/InnateDB_TNFA.csv", "r") as readfile:
    reader = csv.DictReader(readfile)
    gene_list = [row['ensembl'] for row in reader]

# writing in the new csv file
with open('/home/mra/Downloads/Analises-masters/Pipeline/Scripts_1/genes.csv', 'w', newline='') as write_file:
    fieldnames = ['Gene_Ensembl_ID', 'Ortholog_Species', 'Ortholog_Protein_ID', 'Percentage_ID', 'Percentage_Pos']
    writer = csv.DictWriter(write_file, fieldnames=fieldnames)
    writer.writeheader()

    for ensembl_id in gene_list:
        orthologs = fetch_orthologs(ensembl_id) #function to call orthologs
        if orthologs: #verify if the list is empty
            writer.writerows(orthologs)
                         