#!/usr/bin/env bash

set -ve

download_ncbi() {
    wget https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/latest/AMRProt > download.sh
    mv AMRProt data/AMRProt.faa
}

download_aro() {
    wget http://purl.obolibrary.org/obo/aro.owl
}

mkdir -p data

download_ncbi
download_aro
