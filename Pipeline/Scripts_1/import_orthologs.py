import csv
import requests
import time

# function to fetch mammalian orthologs sequences using Ensembl API REST


def fetch_orthologs(ensembl_id):
    server = "https://rest.ensembl.org"
    mammalian_target_taxon = "40674"
    type_of_homology = "orthologues"
    ext = f"/homology/id/{ensembl_id}?target_taxon={mammalian_target_taxon};type={type_of_homology}"
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
        mammalian_orthologs.append({
            "Gene_Ensembl_ID": ensembl_id,
            "Ortholog_Species": target.get("species", ""),
            "Ortholog_Protein_ID": target.get("protein_id"),
            "Percentage_ID": target.get("perc_id"),
            "Percentage_Pos": target.get("perc_pos")
        })

    return mammalian_orthologs


# Load the list of genes from the csv file - obs the column with ensembl IDs must be called `ensembl`
gene_list = []
with open("/home/mra/Downloads/Analises-masters/Pipeline/Scripts_1/InnateDB_TNFA.csv", "r") as readfile:
    reader = csv.DictReader(readfile)
    gene_list = [(row['ensembl'], row['name']) for row in reader]

# writing in the new csv file
for ensembl_id, name in gene_list:
    print(f"Ensembl ID: {ensembl_id}, Name: {name}")

    with open(f"/home/mra/Downloads/Analises-masters/Pipeline/Scripts_1/{name}.csv", 'w', newline='') as write_file:
        fieldnames = ['Gene_Ensembl_ID', 'Ortholog_Species',
                      'Ortholog_Protein_ID', 'Percentage_ID', 'Percentage_Pos']
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        writer.writeheader()
        reqs_per_sec = 15
        req_count = 0
        last_req = 0

        print(f"Starting \033[31m{ensembl_id}\033[0m fetching...")

        finished_with_success = False
        while not finished_with_success:
            if req_count >= reqs_per_sec:
                delta = time.time() - last_req
                if delta < 1:
                    print("Maximum request limit reached!\n")
                    time.sleep(1 - delta)
                last_req = time.time()
                req_count = 0

            try:
                # function to call orthologs
                orthologs = fetch_orthologs(ensembl_id)
                print(orthologs)
                if orthologs:  # verify if the list is empty
                    writer.writerows(orthologs)

                req_count += 1
                finished_with_success = True
                print(f"Finish processing :{ensembl_id}\n")

            except requests.exceptions.HTTPError as e:
                print(f"Erro ao fazer solicitacao para {ensembl_id}:{e}")
                time.sleep(2)  # wait 10s until try again
