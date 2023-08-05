#!/bin/bash

# Uses scripts from MGKit to make te required HDF5 file that is used to extract
# the taxonomic mappings from NCBI/Uniprot

# First checks if any option was passed. Assumes NCBI nt as default
if [ -z "$1" ];
    then
        TYPE=nucl
    else
        TYPE=$1
fi

if [ -z "$2" ];
    then
       OUT_FILE=taxa-tables.hdf
   else
       OUT_FILE=$2
fi

# Dowload the correct DB with MGKit and set the relevant variables
if [ `echo "$TYPE" | tr '[:lower:]' '[:upper:]'` = "PROT" ];
then
    download-ncbi-taxa.sh prot
    TAXA_IDS="ncbi-prot-taxa.gz"
    TABLE_NAME="ncbi-prot"

elif [ `echo "$TYPE" | tr '[:lower:]' '[:upper:]'` = "NUCL" ];
then
    download-ncbi-taxa.sh nucl
    TAXA_IDS="ncbi-nucl-taxa.gz"
    TABLE_NAME="ncbi-nucl"

else
    download-uniprot-taxa.sh
    TAXA_IDS="uniprot-taxa.gz"
    TABLE_NAME=uniprot
fi

echo "Finding the maximum length of the database IDs (takes a while)"
MAX_LENGTH=`gunzip -c $TAXA_IDS  | awk '{ if (length($1) > max) max = length($1) } END {print max}'`

echo "Table name $TABLE_NAME, with a maximum ID length of $MAX_LENGTH"

# Uses gunzip to avoid problems on macOS, where zcat is for .Z files
echo "Creating HDF5 file"
gunzip -c $TAXA_IDS | taxon-utils to_hdf -v -n $TABLE_NAME -s $MAX_LENGTH - $OUT_FILE

echo "The file should be recompressed (using ptrepack) before usage to improve performance"
