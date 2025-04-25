# Erdem Dünyası Ses Varlıkları

Bu klasörde, Erdem Dünyası oyunu için oluşturulan ses efektleri ve müzikler bulunmaktadır. Tüm ses dosyaları WAV formatındadır.

## Klasör Yapısı

```
assets/sounds/
├── effects/     # Ses efektleri
│   ├── menu_select.wav      # Menü seçim sesi
│   ├── level_up.wav         # Seviye atlama sesi
│   ├── attack.wav           # Saldırı sesi
│   ├── damage.wav           # Hasar alma sesi
│   ├── item_pickup.wav      # Eşya toplama sesi
│   ├── quest_complete.wav   # Görev tamamlama sesi
│   ├── spirit_transform.wav # Ruh hayvanı dönüşüm sesi
│   └── door_open.wav        # Kapı açılma sesi
│
└── music/       # Müzik parçaları
    ├── menu_music.wav       # Menü müziği
    ├── valley_music.wav     # Vadi (Uyum Vadisi) müziği
    ├── forest_music.wav     # Orman bölgesi müziği
    ├── combat_music.wav     # Savaş müziği
    └── cave_music.wav       # Mağara müziği
```

## Ses Efektleri

Tüm ses efektleri, oyun içindeki çeşitli olaylara tepki olarak çalınması için tasarlanmıştır:

- **menu_select.wav**: Menüde bir öğe seçildiğinde çalınan ses
- **level_up.wav**: Oyuncu seviye atladığında çalınan ses
- **attack.wav**: Saldırı yapıldığında çalınan ses
- **damage.wav**: Oyuncu hasar aldığında çalınan ses
- **item_pickup.wav**: Oyuncu bir eşya topladığında çalınan ses
- **quest_complete.wav**: Bir görev tamamlandığında çalınan ses
- **spirit_transform.wav**: Ruh hayvanı dönüşümü sırasında çalınan ses
- **door_open.wav**: Kapı açıldığında çalınan ses

## Müzik Parçaları

Müzik parçaları, oyunun farklı bölümlerinde arka planda çalması için tasarlanmıştır:

- **menu_music.wav**: Ana menüde çalan sakin müzik
- **valley_music.wav**: Uyum Vadisi'nde çalan huzurlu müzik
- **forest_music.wav**: Orman bölgesinde çalan gizemli müzik
- **combat_music.wav**: Düşmanlarla savaşırken çalan heyecanlı müzik
- **cave_music.wav**: Mağara ve yeraltı bölgelerinde çalan ürpertici müzik

## Nasıl Üretildi?

Bu ses dosyaları iki yöntemle oluşturulabilir:

1. **CSound**: Bu dosyalar öncelikle CSound kullanılarak oluşturulmak üzere tasarlanmıştır. `create_sounds.py` betiği, CSound kurulu olduğunda, çeşitli orkestra (orc) ve partitur (sco) dosyaları kullanarak bu sesleri sentezler.

2. **Alternatif Metod**: CSound kurulu değilse, betik otomatik olarak NumPy ve SciPy kütüphanelerini kullanarak basit sinüs dalgaları ve gürültü bazlı ses efektleri oluşturur.

## AudioManager Kullanımı

Bu ses dosyalarını oyunda kullanmak için, `src/audio_manager.py` dosyasındaki `AudioManager` sınıfı kullanılabilir. Örnek kullanım:

```python
from audio_manager import AudioManager

# Ses yöneticisini başlat
audio_manager = AudioManager()
audio_manager.initialize()

# Ses efekti çal
audio_manager.play_sound("menu_select")

# Müzik çal
audio_manager.play_music("valley_music")

# Ses seviyesini ayarla
audio_manager.set_sound_volume(0.5)  # 0.0 ile 1.0 arasında
audio_manager.set_music_volume(0.3)  # 0.0 ile 1.0 arasında

# Müziği duraklat/devam ettir
audio_manager.pause_music()
audio_manager.resume_music()

# Müziği durdur
audio_manager.stop_music()
```

## Özelleştirme

Daha fazla ses efekti veya müzik parçası eklemek isterseniz:

1. Özel ses dosyalarınızı ilgili klasörlere (effects/ veya music/) ekleyin
2. `src/constants.py` dosyasındaki SOUNDS ve MUSIC sözlüklerini güncelleyin
3. AudioManager sınıfını ilgili metodları kullanarak çağırın

## Lisans

Bu ses dosyaları MIT lisansı altında lisanslanmıştır ve Erdem Dünyası projesine özeldir. 