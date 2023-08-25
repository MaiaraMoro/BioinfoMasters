import csv
import requests
import time

#function to fetch mammalian orthologs sequences using Ensembl API REST 
def fetch_orthologs (ensembl_id):
    server = "https://rest.ensembl.org"
    mammalian_target_taxon = "40674"
    ext = f"/homology/id/{ensembl_id}?type=orthologues;target_taxon={mammalian_target_taxon};"
    headers = {"Content-Type": "application/json"}

    response = requests.get(server + ext, headers=headers)

    if not response.ok:
        print("Request gone wrong!!!")
        response.raise_for_status()
        return
    
    decoded = response.json()
    mammalian_orthologs = []

    for homology in decoded.get("data", [])[0].get("homologies", []):
        target = homology.get("target", {})
        species = target.get("species", "")

    mammalian_orthologs.append({
        "Gene_Ensembl_ID": ensembl_id,
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
    reqs_per_sec = 15
    req_count = 0
    last_req = 0

    for ensembl_id in gene_list:        # check if we need to rate limit ourselves
        print(ensembl_id)

        if req_count >= reqs_per_sec:
            delta = time.time() - last_req
            if delta < 1:
                print("Maximum request limit reached!\n")
                time.sleep(1 - delta)
            last_req = time.time()
            req_count = 0
   
        try:
            orthologs = fetch_orthologs(ensembl_id) #function to call orthologs
            print(orthologs)
            if orthologs: #verify if the list is empty
                writer.writerows(orthologs)
                exit()
            
            req_count += 1
            print(f"Finish processing :{ensembl_id}\n")
        
        except requests.exceptions.HTTPError as e:
            print(f"Erro ao fazer solicitacao para {ensembl_id}:{e}")
            time.sleep(10) #wait 10s until try again
                         