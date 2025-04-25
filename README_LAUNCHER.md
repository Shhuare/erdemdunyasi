# Erdem Dünyası Oyun Başlatıcısı

Bu başlatıcı, Erdem Dünyası oyununu çalıştırmak için geliştirilmiş kullanıcı dostu bir arayüzdür.

## Özellikler

- **Bağımlılık Kontrolü**: Oyun için gerekli Python modüllerinin kontrol edilmesi
- **Otomatik Kurulum**: Eksik Python kütüphanelerinin otomatik olarak yüklenmesi
- **Ayarlar Menüsü**: Oyun ayarlarını yapılandırma seçenekleri
  - Ses Seviyesi
  - Müzik Seviyesi
  - Grafik Kalitesi
  - Tam Ekran Modu
  - Dil Seçimi
- **İşlem Günlüğü**: Uygulama tarafından gerçekleştirilen işlemlerin günlük ekranında gösterilmesi
- **Yardım Sayfası**: Oyun kontrolleri ve özellikleri hakkında bilgiler

## Kullanım

Başlatıcıyı aşağıdaki yöntemlerle çalıştırabilirsiniz:

### Windows'ta:
```
run_game.bat
```
veya
```
python launcher.py
```

### Linux/macOS'ta:
```
./run_game.sh
```
veya
```
python3 launcher.py
```

## Gereksinimler

- Python 3.7 veya üzeri
- Tkinter (Python'un grafik arayüz kütüphanesi)
- Oyun için gerekli kütüphaneler (pygame, numpy, pillow, pytmx, pyyaml, pathlib)

## Sorun Giderme

1. **"Python bulunamadı" hatası**:
   - Python'un doğru bir şekilde kurulu olduğundan emin olun
   - Python'un PATH değişkeninde olduğundan emin olun

2. **"Tkinter bulunamadı" hatası**:
   - Linux kullanıcıları için: `sudo apt-get install python3-tk` (Debian/Ubuntu)
   - macOS kullanıcıları için: `brew install python-tk` (Homebrew kullanıyorsanız)

3. **Bağımlılık Yükleme Hatası**:
   - Başlatıcı arayüzünde "Bağımlılıkları Yükle" düğmesini kullanın
   - Veya manuel olarak: `pip install -r requirements.txt`

4. **Oyun Başlatma Hatası**:
   - İşlem günlüğündeki hata mesajlarını kontrol edin
   - Ana oyun dosyaları (main.py veya src/main.py) mevcut olduğundan emin olun

## Dizin Yapısı

```
erdem_dunyasi/
├── launcher.py          # Başlatıcı uygulaması
├── run_game.bat         # Windows başlatma betiği
├── run_game.sh          # Linux/macOS başlatma betiği
├── main.py              # Ana oyun dosyası
├── src/                 # Kaynak kodları
├── assets/              # Oyun varlıkları (görseller, sesler, vb.)
│   └── images/          # Logoları ve simgeleri içerir
├── requirements.txt     # Gerekli kütüphaneler
└── settings.json        # Kullanıcı ayarları
```

## Katkıda Bulunma

Sorunları bildirmek veya özellik önerileri için lütfen bir Issue açın veya Pull Request gönderin.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 