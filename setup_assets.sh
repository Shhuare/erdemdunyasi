#!/bin/bash

echo "Erdem Dunyasi - Asset Kurulum Araci"
echo "====================================="

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo "Python bulunamadi! Lutfen Python 3.7 veya daha yeni bir surumu yukleyin."
    exit 1
fi

# Assets klasörü oluştur
echo "Asset klasor yapisini kuruyorum..."
python3 -m src.asset_importer --setup

# Eğer asset paketi belirtilmişse
if [ ! -z "$1" ]; then
    echo "$1 paketini isliyorum..."
    python3 -m src.asset_importer --source "$1" --recursive
else
    echo "Lutfen ice aktarilacak klasoru belirtin."
    echo "Ornek: ./setup_assets.sh ~/Downloads/fantasy_rpg_asset_pack"
fi

# Asset kaydını güncelle
echo "Asset kayitlarini guncelliyorum..."
python3 -m src.asset_importer --update

echo "Islem tamamlandi!" 