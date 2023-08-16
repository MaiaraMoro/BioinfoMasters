#!/bin/bash

# Solicitar ao usuário o nome do arquivo de alinhamento
echo "Por favor, insira o nome do arquivo de alinhamento:"
read INPUT

# Verificar se o arquivo existe
if [ ! -f "$INPUT" ]; then
    echo "Erro: O arquivo $INPUT não foi encontrado!"
    exit 1
fi

# Passo 1: Executar o ModelFinder para seleção do modelo, restringindo aos modelos suportados pelo RAxML
iqtree2 -s $INPUT -m MF --mset raxml

# Encontrar o modelo ótimo no arquivo de log do IQ-TREE
MODEL=$(grep "Best-fit model:" $INPUT.log | awk '{print $3}' | sed 's/+.*//')

echo "O modelo recomendado pelo IQ-TREE é: $MODEL"

# Verifica se o modelo é "HIVb" e, em caso afirmativo, substitui por "HIVB". 
if [ "$MODEL" == "HIVb" ]; then
    MODEL="HIVB"
fi

echo "Usando o modelo: $MODEL"

# Verificar se o modelo está na lista de modelos do RAxML
case $MODEL in
    DAYHOFF|DCMUT|JTT|MTREV|WAG|RTREV|CPREV|VT|BLOSUM62|MTMAM|LG|MTART|MTZOA|PMB|HIVB|HIVW|JTTDCMUT|FLU|STMTREV|DUMMY|DUMMY2|AUTO|LG4M|LG4X|PROT_FILE|GTR_UNLINKED|GTR)
        # Passo 2: Executar o RAxML com o modelo selecionado
        raxmlHPC -p 12345 -s $INPUT -m PROTGAMMA${MODEL} -f x -n matrix
        ;;
    *)
        echo "Erro: O modelo $MODEL não é reconhecido pelo RAxML."
        exit 1
        ;;
esac

echo "Processo concluído."

