import pandas as pd
import sys
import os

def transform_distance_file(file_path, gene_name):
    # Lendo o arquivo de saída do RAxML com espaços em branco como delimitador
    df = pd.read_csv(file_path, delim_whitespace=True, header=None, names=["Species1", "Species2", "Distance"])

    # Convertendo explicitamente as colunas para strings
    df['Species1'] = df['Species1'].astype(str)
    df['Species2'] = df['Species2'].astype(str)

    # Renomeando a coluna de "Distance" para o nome do gene
    df[gene_name] = df["Distance"]
    df.drop(['Distance'], axis=1, inplace=True)

    return df

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Por favor, forneça o nome do arquivo e o nome do gene como argumentos.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    gene_name = sys.argv[2]

    # Processa o arquivo de entrada
    result = transform_distance_file(input_file, gene_name)
    print("Primeiros registros do DataFrame 'result':")
    print(result.head())

    # Se o arquivo de saída já existe, leia-o e combine-o com o novo resultado
    if os.path.exists('aggregated_distances.csv'):
        aggregated_df = pd.read_csv('aggregated_distances.csv')
        print("\nPrimeiros registros do DataFrame 'aggregated_df':")
        print(aggregated_df.head())

        # Merge com base nas colunas 'Species1' e 'Species2'
        merged_df = pd.merge(aggregated_df, result, on=['Species1', 'Species2'], how='outer')
        # Ordena pelo par de espécies para garantir uma ordem consistente
        merged_df = merged_df.sort_values(by=['Species1', 'Species2'])
        merged_df.to_csv('aggregated_distances.csv', index=False)
    else:
        # Se o arquivo não existe, simplesmente salve o resultado
        result.to_csv('aggregated_distances.csv', index=False)

    print(f"\nArquivo transformado e agregado salvo como: aggregated_distances.csv")

