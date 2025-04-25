# Erdem Dünyası - Asset Kurulum Rehberi

Bu rehber Erdem Dünyası oyununun asset (görsel, ses ve harita) dosyalarını yapılandırmak için gerekli adımları açıklar.

## Gereksinimleri

- Python 3.7 veya daha yeni sürüm
- Pygame kütüphanesi

## Hazır Asset Paketini Kurma

Erdem Dünyası için asset'leri iki şekilde kurabilirsiniz:

### 1. Hazır Asset Paketi Kullanarak

Eğer bir asset paketi (.zip) indirdiyseniz:

1. `setup_assets.bat` dosyasını çalıştırın ve asset paketinin yolunu parametre olarak verin:
   ```
   setup_assets.bat "C:\indirilen_assetler\erdem_dunyasi_assetler.zip"
   ```

2. Asset'ler otomatik olarak doğru klasörlere kopyalanacak ve kayıt dosyası güncellenecektir.

### 2. Mevcut Asset'leri Yapılandırarak

Eğer roguelike sprite sheet'leri (roguelikeChar_transparent.png, roguelikeSheet_transparent.png) zaten mevcutsa:

1. `configure_assets.bat` dosyasını çalıştırın:
   ```
   configure_assets.bat
   ```

2. Bu betik mevcut sprite sheet'lerden karakterleri, düşmanları, eşyaları ve efektleri otomatik olarak oluşturacaktır.

## Asset Yapısı

Oyun aşağıdaki asset türlerini kullanır:

- **Karakterler**: `assets/sprites/player/` dizininde kahramanlar
- **NPC'ler**: `assets/sprites/npcs/` dizininde köylüler, tüccarlar, vb.
- **Düşmanlar**: `assets/sprites/enemies/` dizininde yaratıklar
- **Ruh Hayvanları**: `assets/sprites/spirit_animals/` dizininde kurt, ayı, kartal, tilki
- **Eşyalar**: `assets/sprites/items/` dizininde çeşitli eşyalar
- **Silahlar**: `assets/sprites/items/weapons/` dizininde silahlar
- **Zırhlar**: `assets/sprites/items/armor/` dizininde zırhlar
- **Haritalar**: `assets/maps/` dizininde Tiled harita dosyaları (.tmx)
- **Tile Setleri**: `assets/tilesets/` dizininde harita parçaları
- **UI**: `assets/images/ui/` dizininde arayüz elemanları
- **Sesler**: `assets/sounds/effects/` dizininde efekt sesleri
- **Müzikler**: `assets/sounds/music/` dizininde müzikler

## Mevcut Asset'ler

Şu anda oyunda bulunan hazır asset'ler:

### Karakterler
- Erkek Kahraman
- Kadın Kahraman

### Ruh Hayvanları
- Kurt (Toprak Elementi)
- Ayı (Ateş Elementi)
- Kartal (Hava Elementi)
- Tilki (Su Elementi)

### NPC'ler
- Köy Lideri (Elder)
- Muhafız (Guard)
- Tüccar (Merchant)
- Köylü (Villager)

### Düşmanlar
- Kurt (Wolf)
- Haydut (Bandit)
- Glitch (Dijital Hata Yaratığı)
- Drone (Mekanik Yaratık)

### Silahlar ve Zırhlar
- Kılıç, Balta, Yay, Asa
- Kalkan, Miğfer, Zırh, Botlar

### Efektler
- Elemental efektler (Ateş, Su, Toprak, Hava)
- Teknoloji efektleri (Teknoloji, Ruh)
- Ruh hayvanı yetenekleri (Kurt Uluması, Ayı Kükremesi, Kartal Dalışı, Tilki Hileleri)

## Kendi Asset'lerinizi Eklemek

Kendi özel asset'lerinizi eklemek için:

1. Dosyalarınızı ilgili klasörlere kopyalayın
2. Asset kaydını güncellemek için:
   ```
   python -m src.asset_importer --update
   ```

## Sorun Giderme

Eğer asset'lerin doğru görüntülenmediğini fark ederseniz:

1. `assets/asset_registry.json` dosyasının doğru şekilde güncellendiğinden emin olun
2. Tüm dosya yollarının Windows formatında olduğundan emin olun (ters eğik çizgi `\` kullanılmalı)
3. Asset yapılandırıcıyı tekrar çalıştırın:
   ```
   configure_assets.bat
   ```

## Daha Fazla Yardım

Daha fazla yardım için projede bulunan `src/asset_importer.py` ve `src/asset_configurator.py` dosyalarını inceleyebilirsiniz. 