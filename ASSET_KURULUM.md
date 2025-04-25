# Erdem Dünyası - Asset Kurulum Rehberi

Bu rehber, Erdem Dünyası oyununa yeni görsel elemanlar (asset) ekleme sürecini anlatır.

## Gereken Araçlar

- Python 3.7 veya daha yeni bir sürümü
- Pygame kütüphanesi
- Eklemek istediğiniz asset paketleri

## Kurulum Adımları

### 1. Asset Klasör Yapısını Oluşturma

Asset klasör yapısını oluşturmak için aşağıdaki komutu çalıştırın:

**Windows:**
```
python -m src.asset_importer --setup
```

**Linux/macOS:**
```
python3 -m src.asset_importer --setup
```

Bu komut, oyunda kullanılacak tüm asset türleri için gerekli klasörleri oluşturacaktır.

### 2. Asset Paketlerini İçe Aktarma

Asset paketlerini içe aktarmak için aşağıdaki komutu kullanın:

**Windows:**
```
python -m src.asset_importer --source "C:\path\to\asset_pack" --recursive
```

**Linux/macOS:**
```
python3 -m src.asset_importer --source "/path/to/asset_pack" --recursive
```

`--recursive` parametresi, belirtilen klasörü ve tüm alt klasörlerini tarayarak uygun dosyaları otomatik olarak içe aktarır.

Belirli bir asset türü için içe aktarma yapmak isterseniz:

```
python -m src.asset_importer --source "path/to/tileset_folder" --type tileset
```

Desteklenen asset türleri:
- `character`: Oyuncu karakterleri
- `npc`: NPC karakterleri
- `enemy`: Düşmanlar
- `spirit_animal`: Ruh hayvanları
- `tileset`: Harita karoları
- `map`: Harita dosyaları
- `item`: Genel eşyalar
- `weapon`: Silahlar
- `armor`: Zırhlar
- `ui`: Arayüz elemanları
- `effect`: Görsel efektler
- `sound`: Ses efektleri
- `music`: Müzik dosyaları

### 3. Asset Kaydını Güncelleme

Tüm assetleri içe aktardıktan sonra, oyunun bunları tanıması için kayıtları güncelleyin:

**Windows:**
```
python -m src.asset_importer --update
```

**Linux/macOS:**
```
python3 -m src.asset_importer --update
```

Bu komut, tüm assetleri tarayacak ve `assets/asset_registry.json` dosyasını oluşturacak veya güncelleyecektir.

## Tek Adımda Kurulum

Batch dosyasını kullanarak tek bir komutla tüm süreci otomatikleştirebilirsiniz:

**Windows:**
```
setup_assets.bat "C:\path\to\asset_pack"
```

**Linux/macOS:**
```
./setup_assets.sh "/path/to/asset_pack"
```

## Örnek Dosya Yerleşimi

Tipik bir asset paketi yapısı şöyle olabilir:

```
assets/
  ├── sprites/
  │   ├── player/
  │   │   └── character.png
  │   ├── npcs/
  │   │   ├── villager.png
  │   │   └── merchant.png
  │   ├── enemies/
  │   │   ├── wolf.png
  │   │   └── bandit.png
  │   ├── spirit_animals/
  │   │   ├── wolf.png
  │   │   ├── eagle.png
  │   │   ├── bear.png
  │   │   └── fox.png
  │   └── items/
  │       ├── potion.png
  │       ├── weapons/
  │       │   ├── sword.png
  │       │   └── bow.png
  │       └── armor/
  │           ├── helmet.png
  │           └── shield.png
  ├── tilesets/
  │   ├── grass.png
  │   ├── water.png
  │   └── village.tsx
  ├── maps/
  │   ├── starter_village.tmx
  │   └── forest.tmx
  ├── images/
  │   └── ui/
  │       ├── button.png
  │       ├── panel.png
  │       └── inventory_slot.png
  └── sounds/
      ├── attack.wav
      ├── item_pickup.wav
      └── music/
          ├── village_theme.mp3
          └── battle_theme.mp3
```

## Önerilen Asset Paketleri

Oyunda kullanabileceğiniz bazı ücretsiz asset paketleri:

1. **RPG Maker Tileset**: RPG Maker VX/MV/MZ için tilesetler
2. **Kenney Game Assets**: https://kenney.nl/assets adresinde birçok ücretsiz asset bulabilirsiniz
3. **OpenGameArt.org**: https://opengameart.org/ üzerinde birçok ücretsiz sprite ve tileset mevcut
4. **itch.io Ücretsiz Assetleri**: https://itch.io/game-assets/free adresinden birçok ücretsiz asset bulabilirsiniz

## Not

Eklediğiniz assetleri kullanırken, orijinal lisanslarına dikkat etmeyi unutmayın. Bazı assetleri oyununuzda kullanmak için belirli bir atıf veya lisans anlaşması gerekebilir. 