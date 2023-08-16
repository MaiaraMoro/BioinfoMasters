# distance_processing.py

import pandas as pd

def transform_distance_file_with_mapping(file_path, gene_name, mapping_df):
    """
    Transform the distance file using the mapping from sequence ID to species name.
    """
    df = pd.read_csv(file_path, sep='\s+', header=None, names=["Seq1", "Seq2", "Distance"])
    
    df = pd.merge(df, mapping_df, left_on='Seq1', right_on='SpeciesID', how='left').drop(['Seq1', 'SpeciesID'], axis=1)
    df['Taxonomy'] = df['Taxonomy'].fillna("Desconhecido")
    df.rename(columns={'Taxonomy': 'Species1'}, inplace=True)

    df = pd.merge(df, mapping_df, left_on='Seq2', right_on='SpeciesID', how='left').drop(['Seq2', 'SpeciesID'], axis=1)
    df['Taxonomy'] = df['Taxonomy'].fillna("Desconhecido")
    df.rename(columns={'Taxonomy': 'Species2'}, inplace=True)

    df['Pairs'] = df['Species1'] + ' ' + df['Species2']
    df.rename(columns={'Distance': gene_name}, inplace=True)
    df = df[['Pairs', gene_name]]

    return df
