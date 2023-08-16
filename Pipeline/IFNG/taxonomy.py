def extract_taxonomic_info_from_fasta_updated(fasta_file):
    """
    Extrai os códigos de identificação e classificações taxonômicas das descrições das sequências do arquivo FASTA.
    Esta função usa manipulação de strings padrão e está ajustada para extrair a classificação taxonômica entre [].
    """
    identifiers = []
    taxonomies = []

    # Lendo o arquivo FASTA
    with open(fasta_file, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith('>'):
                # Usando regex para extrair o código de identificação e a classificação taxonômica entre []
                match = re.match(r'>(\S+) .+? \[(.+?)\]', line)
                if match:
                    identifiers.append(match.group(1))
                    taxonomies.append(match.group(2))

    # Convertendo as listas em DataFrame
    df = pd.DataFrame({
        'SpeciesID': identifiers,
        'Taxonomy': taxonomies
    })
    
    return df

# Testando a função atualizada
taxonomic_df_updated = extract_taxonomic_info_from_fasta_updated(fasta_file_path_corrected)
taxonomic_df_updated.head()
