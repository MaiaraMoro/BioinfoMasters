#!/bin/bash

# Função para realizar o alinhamento
align_sequences() {
    local INPUT_DIR=$1
    local OUTPUT_DIR=$2

    # Verificar se o diretório de entrada existe
    if [ ! -d "$INPUT_DIR" ]; then
        echo "Erro: diretório de entrada $INPUT_DIR não encontrado!"
        exit 1
    fi

    # Arquivo temporário
    local TEMP_FILE="$INPUT_DIR/temp.fasta"

    # Loop através de todos os arquivos FASTA no diretório de entrada
    for FILE in $INPUT_DIR/*.fasta; do
    
        # Verifica se o arquivo é um arquivo fasta válido
        if [[ $FILE =~ \.fasta$ ]] && ! [[ $FILE =~ ^\./\. ]]; then
        
            # Nome base do arquivo sem extensão
            local BASENAME=$(basename -- "$FILE" .fasta)
            
            # Pular arquivos que começam com um ponto
            if [[ $BASENAME == .* ]]; then
                continue
            fi
        
            # Arquivo de saída do MAFFT
            local MAFFT_OUTPUT="$OUTPUT_DIR/$BASENAME-aligned.fasta"
            
            # Arquivo de saída do GBLOCKS
            local GBLOCKS_OUTPUT="$OUTPUT_DIR/$BASENAME-aligned-gblocks.fasta"

            # Encurtar os nomes das sequências para o requerimento do gblocks (em arquivo temporário)
            awk '/^>/ {print ">" substr($1, 2); next} {print}' $FILE > $TEMP_FILE
        
            # Executar MAFFT no arquivo temporário
            mafft --auto $TEMP_FILE > $MAFFT_OUTPUT
        
            # Executar GBLOCKS + parâmetros de ajustes 
            Gblocks $MAFFT_OUTPUT -t=p -b5=h
        
            # Verifica se o Gblocks foi bem-sucedido
            if [ ! -f "${MAFFT_OUTPUT}-gb" ]; then
                echo "Erro ao ajustar alinhamento de $MAFFT_OUTPUT com Gblocks!"
                exit 1
            fi

            # Mover a saída do GBLOCKS para o diretório de saída
            mv "${MAFFT_OUTPUT}-gb" $GBLOCKS_OUTPUT

            # Remover o arquivo temporário
            rm $TEMP_FILE
            
            # Chamar a função calculate_distances para este arquivo específico
            calculate_distances $GBLOCKS_OUTPUT $BASENAME
        fi
    done 
}

# Função para realizar seleção do modelo e cálculo de distância
calculate_distances() {
    local INPUT=$1
    local BASENAME=$2

    # Verificar se o arquivo existe
    if [ ! -f "$INPUT" ]; then
        echo "Erro: O arquivo $INPUT não foi encontrado!"
        exit 1
    fi

    # Passo 1: Executar o ModelFinder para seleção do modelo, restringindo aos modelos suportados pelo RAxML
    iqtree2 -s $INPUT -m MF --mset raxml

    # Encontrar o modelo ótimo no arquivo de log do IQ-TREE
    local MODEL=$(grep "Best-fit model:" $INPUT.log | awk '{print $3}' | sed 's/+.*//')

    # Verifica se o modelo é "HIVb" e, em caso afirmativo, substitui por "HIVB" forma reconhecida pelo RAxML. 
    [ "$MODEL" == "HIVb" ] && MODEL="HIVB"

    # Verificar se o modelo está na lista de modelos do RAxML
    case $MODEL in
        DAYHOFF|DCMUT|JTT|MTREV|WAG|RTREV|CPREV|VT|BLOSUM62|MTMAM|LG|MTART|MTZOA|PMB|HIVB|HIVW|JTTDCMUT|FLU|STMTREV|DUMMY|DUMMY2|AUTO|LG4M|LG4X|PROT_FILE|GTR_UNLINKED|GTR)
            # Passo 2: Executar o RAxML com o modelo selecionado
            raxmlHPC -p 12345 -s $INPUT -m PROTGAMMA${MODEL} -f x -n ${BASENAME}_matrix
            ;;
        *)
            echo "Erro: O modelo $MODEL não é reconhecido pelo RAxML."
            exit 1
            ;;
    esac
}

# Chamar as funções
align_sequences "$1" "$2"
echo "Processo concluído."

