#!/bin/bash

# Diretório onde estão as sequências
INPUT_DIR="$1"
# Diretório de saída
OUTPUT_DIR="$2"

# Arquivo temporário
TEMP_FILE="$INPUT_DIR/temp.fasta"

# Loop através de todos os arquivos FASTA no diretório de entrada
for FILE in $INPUT_DIR/*.fasta; do
    # Nome base do arquivo sem extensão
    BASENAME=$(basename -- "$FILE" .fasta)
    
    # Arquivo de saída do MAFFT
    MAFFT_OUTPUT="$OUTPUT_DIR/$BASENAME-aligned.fasta"
    
    # Arquivo de saída do GBLOCKS
    GBLOCKS_OUTPUT="$OUTPUT_DIR/$BASENAME-aligned-gblocks.fasta"

    # Se os arquivos de saída já existem, pule o processamento para este arquivo
    if [ -f $MAFFT_OUTPUT ] && [ -f $GBLOCKS_OUTPUT ]; then
        echo "Os arquivos de saída para $BASENAME já existem. Pulando..."
        continue
    fi

    # Encurtar os nomes das sequências para o requerimento do gblocks (em arquivo temporário)
    awk '/^>/ {print ">" substr($1, 2); next} {print}' $FILE > $TEMP_FILE
    
    # Executar MAFFT no arquivo temporário
    mafft --auto $TEMP_FILE > $MAFFT_OUTPUT
    
    # Executar GBLOCKS + parâmetros de ajustes 
    Gblocks $MAFFT_OUTPUT -t=p -b5=h

    # Verificar se Gblocks foi bem-sucedido
    if [ ! -f "${MAFFT_OUTPUT}-gb" ]; then
        echo "Erro ao ajustar alinhamento de $MAFFT_OUTPUT com Gblocks!"
        exit 1
    fi

    # Mover a saída do GBLOCKS para o diretório de saída
    mv "${MAFFT_OUTPUT}-gb" $GBLOCKS_OUTPUT

    # Remover o arquivo temporário
    rm $TEMP_FILE
    
done

