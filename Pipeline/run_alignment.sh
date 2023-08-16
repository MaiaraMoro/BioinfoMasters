#!/bin/bash

# Diretório onde estão as sequências
INPUT_DIR="~/Downloads/Pipeline/IFNG"

# Diretório de saída
OUTPUT_DIR="~/Downloads/Pipeline/IFNG"

# Loop através de todos os arquivos FASTA no diretório de entrada
for FILE in $INPUT_DIR/*.fasta; do
    # Nome base do arquivo sem extensão
    BASENAME=$(basename -- "$FILE" .fasta)
    
    # Arquivo de saída do MAFFT
    MAFFT_OUTPUT="$OUTPUT_DIR/$BASENAME-aligned.fasta"
    
    # Arquivo de saída do GBLOCKS
    GBLOCKS_OUTPUT="$OUTPUT_DIR/$BASENAME-aligned-gblocks.fasta"
    
    # Executar MAFFT
    mafft --auto $FILE > $MAFFT_OUTPUT
    
    # Executar GBLOCKS
    Gblocks $MAFFT_OUTPUT -t=p -b5=h -e=-gblocks.fasta
    
    # Mover a saída do GBLOCKS para o diretório de saída
    mv "$MAFFT_OUTPUT-gblocks.fasta" $GBLOCKS_OUTPUT
done
