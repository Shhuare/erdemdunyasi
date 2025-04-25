#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Erdem Dünyası için CSound kullanarak ses efektleri ve müzik oluşturan betik.
Bu betik, oyun için gereken temel sesleri CSound kullanarak sentezler ve wav formatında kaydeder.
"""

import os
import subprocess
import tempfile
import time
import random
from pathlib import Path

# Ses dosyalarının kaydedileceği dizinler
EFFECTS_DIR = Path("assets/sounds/effects")
MUSIC_DIR = Path("assets/sounds/music")

# CSound'un yüklü olup olmadığını kontrol et
def check_csound():
    """CSound'un yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(['csound', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

# CSound orc dosyasını oluştur
def create_orc_file(temp_dir):
    """CSound için orkestra (orc) dosyası oluşturur"""
    orc_path = os.path.join(temp_dir, "erdem_dunyasi.orc")
    
    orc_content = """
    sr = 44100
    ksmps = 32
    nchnls = 2
    0dbfs = 1
    
    ; Temel enstrümanlar
    
    ; Basit bir zil/çan sesi (menu_select, level_up)
    instr 1
        ; p4 = frekans
        ; p5 = süre çarpanı
        ifreq = p4
        ifdbgain = 0.9
        aenv expseg 0.01, 0.1, 1, p3 * p5, 0.01
        asig pluck aenv, ifreq, ifreq, 0, 1
        aflt resonz asig, ifreq, ifreq/5
        outs aflt*0.7, aflt*0.7
    endin
    
    ; Saldırı/vuruş sesi (attack)
    instr 2
        ; p4 = frekans
        ; p5 = süre
        ifreq = p4
        aenv expseg 0.01, 0.01, 1, 0.05, 0.5, p5, 0.01
        anoise noise 0.5, 0
        afilt resonz anoise, ifreq, ifreq/2
        asig = afilt * aenv
        outs asig, asig
    endin
    
    ; Hasar alma/acı sesi (damage)
    instr 3
        ; p4 = frekans
        ifreq = p4
        aenv linseg 0, 0.05, 1, 0.1, 0.3, 0.2, 0
        aosc oscili aenv, ifreq, 1
        anoise noise 0.3, 0
        afilt resonz anoise, ifreq*2, 100
        asig = aenv * (aosc*0.5 + afilt*0.5)
        outs asig, asig
    endin
    
    ; Eşya alma sesi (item_pickup)
    instr 4
        ; p4 = frekans
        ifreq = p4
        aenv linseg 0, 0.05, 1, 0.2, 0
        aosc oscili aenv, ifreq, 1
        aosc2 oscili aenv, ifreq*1.5, 1
        asig = aosc*0.6 + aosc2*0.4
        outs asig, asig
    endin
    
    ; Görev tamamlama sesi (quest_complete)
    instr 5
        ; p4 = frekans
        ifreq = p4
        aenv1 linseg 0, 0.05, 1, 0.2, 0
        aenv2 linseg 0, 0.15, 1, 0.3, 0
        aenv3 linseg 0, 0.3, 1, 0.3, 0
        aosc1 oscili aenv1, ifreq, 1
        aosc2 oscili aenv2, ifreq*1.5, 1
        aosc3 oscili aenv3, ifreq*2, 1
        asig = aosc1*0.4 + aosc2*0.3 + aosc3*0.3
        outs asig, asig
    endin
    
    ; Ruh hayvanı dönüşüm sesi (spirit_transform)
    instr 6
        ; p4 = frekans
        ifreq = p4
        kfreq expseg ifreq*0.8, 0.3, ifreq*2, 0.7, ifreq
        kenv linseg 0, 0.1, 0.8, 0.8, 0.5, 0.3, 0
        anoise noise 0.3, 0
        afilt resonz anoise, kfreq, kfreq/4
        aosc oscili kenv, kfreq, 1
        asig = kenv * (aosc*0.6 + afilt*0.4)
        outs asig, asig
    endin
    
    ; Kapı açılma sesi (door_open)
    instr 7
        kenv linseg 0, 0.01, 1, 0.3, 0.5, 0.2, 0
        anoise noise 0.4, 0
        kfreq expseg 800, 0.5, 300, 0.5, 80
        afilt resonz anoise, kfreq, kfreq/2
        asig = afilt * kenv
        outs asig, asig
    endin
    
    ; Basit melodi aleti (ambient müzik için)
    instr 10
        ; p4 = frekans
        ; p5 = amplitude (0-1)
        ifreq = p4
        iamp = p5
        kenv linseg 0, 0.1, iamp, p3-0.2, iamp, 0.1, 0
        asig oscili kenv, ifreq, 1
        aenv2 linseg 1, p3, 0.8
        asig2 oscili kenv*0.5, ifreq*2*aenv2, 1
        aout = asig + asig2*0.3
        afilt tone aout, 3000
        outs afilt, afilt
    endin
    
    ; Pad sesi (ambient müzik için)
    instr 11
        ; p4 = frekans
        ; p5 = amplitude (0-1)
        ifreq = p4
        iamp = p5
        kenv linseg 0, 1, iamp, p3-2, iamp, 1, 0
        kosc1 oscili 1, 5.5, 1
        kosc2 oscili 1, 4.7, 1
        kfmod = 1 + ((kosc1 + kosc2) * 0.01)
        asig1 oscili kenv, ifreq, 1
        asig2 oscili kenv*0.5, ifreq*kfmod, 1
        asig3 oscili kenv*0.3, ifreq*2.01, 1
        aout = asig1 + asig2 + asig3
        afilt tone aout, 2000
        outs afilt, afilt
    endin
    
    ; Bas sesi (müzik için)
    instr 12
        ; p4 = frekans
        ; p5 = amplitude (0-1)
        ifreq = p4
        iamp = p5
        kenv linseg 0, 0.1, iamp, p3-0.2, iamp, 0.1, 0
        asig oscili kenv, ifreq, 1
        asig2 oscili kenv*0.2, ifreq*2, 1
        aout = asig + asig2
        afilt tone aout, 1000
        outs afilt, afilt
    endin
    """
    
    with open(orc_path, "w") as f:
        f.write(orc_content)
    
    return orc_path

# Ses efektleri için sco dosyaları oluştur
def create_effect_sco(temp_dir, effect_name):
    """Belirli bir ses efekti için CSound sco dosyası oluşturur"""
    sco_path = os.path.join(temp_dir, f"{effect_name}.sco")
    
    sco_content = ""
    # Farklı ses efektleri için sco içeriği
    if effect_name == "menu_select":
        sco_content = """
        ; Menü seçim sesi
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        ; Yükselen iki nota
        i 1 0 0.3 700 1
        i 1 0.15 0.3 1000 1
        
        e
        """
    elif effect_name == "level_up":
        sco_content = """
        ; Seviye atlama sesi
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        ; Üç nota artarak
        i 1 0 0.4 500 1
        i 1 0.2 0.5 750 1
        i 1 0.5 0.6 1000 1
        i 1 0.8 0.7 1200 1
        
        e
        """
    elif effect_name == "attack":
        sco_content = """
        ; Saldırı sesi
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        i 2 0 0.3 300 0.3
        
        e
        """
    elif effect_name == "damage":
        sco_content = """
        ; Hasar alma sesi
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        i 3 0 0.4 200
        
        e
        """
    elif effect_name == "item_pickup":
        sco_content = """
        ; Eşya alma sesi
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        i 4 0 0.3 800
        
        e
        """
    elif effect_name == "quest_complete":
        sco_content = """
        ; Görev tamamlama sesi
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        i 5 0 0.8 400
        
        e
        """
    elif effect_name == "spirit_transform":
        sco_content = """
        ; Ruh hayvanı dönüşüm sesi
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        i 6 0 1.2 300
        
        e
        """
    elif effect_name == "door_open":
        sco_content = """
        ; Kapı açılma sesi
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        i 7 0 0.6
        
        e
        """
    
    with open(sco_path, "w") as f:
        f.write(sco_content)
    
    return sco_path

# Melodi oluşturucu fonksiyon (Pentatonik dizide)
def generate_pentatonic_melody(temp_dir, length=16, base_note=60):
    """Pentatonik dizide basit bir melodi oluşturur"""
    notes = []
    pentatonic = [0, 2, 4, 7, 9]  # Pentatonik dizi aralıkları
    current_note = base_note
    
    for i in range(length):
        interval = random.choice(pentatonic)
        octave_shift = random.choice([-12, 0, 0, 0, 12]) if i % 4 == 0 else 0
        current_note = base_note + interval + octave_shift
        duration = random.choice([0.5, 1.0, 1.5])
        notes.append((current_note, duration))
    
    return notes

# Frekans hesaplama (MIDI nota numarasından)
def midi_to_freq(midi_note):
    """MIDI nota numarasından frekans hesaplar"""
    return 440 * (2 ** ((midi_note - 69) / 12))

# Müzik parçaları için sco dosyaları oluştur
def create_music_sco(temp_dir, music_name):
    """Belirli bir müzik parçası için CSound sco dosyası oluşturur"""
    sco_path = os.path.join(temp_dir, f"{music_name}.sco")
    
    sco_content = ""
    # Farklı müzik tipleri için sco içeriği
    if music_name == "menu_music":
        sco_content = """
        ; Menü müziği
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        """
        
        # Sakin, ambiyans tarzı müzik
        # Pad sesleri
        pad_notes = [60, 64, 67, 72]  # C, E, G, C - C major akordu
        for i, note in enumerate(pad_notes):
            freq = midi_to_freq(note)
            start_time = i * 0.5  # Notalar arasında yarım saniye
            sco_content += f"i 11 {start_time} 10 {freq} 0.2\n"
        
        # 10 saniye ara verip tekrarla
        for i, note in enumerate(pad_notes):
            freq = midi_to_freq(note)
            start_time = 10 + i * 0.5  # Notalar arasında yarım saniye
            sco_content += f"i 11 {start_time} 10 {freq} 0.2\n"
        
        sco_content += "\ne\n"
        
    elif music_name == "valley_music":
        sco_content = """
        ; Vadi müziği (sakin ve huzurlu)
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        """
        
        # Pad sesleri (uzun süren arka plan)
        pad_notes = [(55, 0.15), (59, 0.15), (62, 0.15)]  # G, B, D - G major akordu
        current_time = 0
        for _ in range(2):  # İki kez tekrarla
            for note, amp in pad_notes:
                freq = midi_to_freq(note)
                sco_content += f"i 11 {current_time} 15 {freq} {amp}\n"
                current_time += 5  # 5 saniye sonra sonraki nota
        
        # Melodi
        melody_notes = generate_pentatonic_melody(temp_dir, length=12, base_note=67)
        current_time = 3  # Melodiyi 3 saniye gecikmeli başlat
        for note, duration in melody_notes:
            freq = midi_to_freq(note)
            sco_content += f"i 10 {current_time} {duration} {freq} 0.3\n"
            current_time += duration
        
        sco_content += "\ne\n"
        
    elif music_name == "forest_music":
        sco_content = """
        ; Orman müziği (gizemli)
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        """
        
        # Bas notaları (yavaş ritimli)
        bass_notes = [48, 47, 45, 43]  # C, B, A, G - inici bas hattı
        current_time = 0
        for _ in range(4):  # 4 kez tekrarla
            for note in bass_notes:
                freq = midi_to_freq(note)
                sco_content += f"i 12 {current_time} 1.8 {freq} 0.4\n"
                current_time += 2
        
        # Pad sesleri (atmosferik)
        pad_notes = [(52, 0.1), (56, 0.1), (59, 0.1)]  # E, G#, B - E minör akordu
        current_time = 2  # Padleri 2 saniye gecikmeli başlat
        for note, amp in pad_notes:
            freq = midi_to_freq(note)
            sco_content += f"i 11 {current_time} 30 {freq} {amp}\n"
            current_time += 10
        
        sco_content += "\ne\n"
        
    elif music_name == "combat_music":
        sco_content = """
        ; Savaş müziği (heyecan verici, hızlı)
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        """
        
        # Bas ritmik desenler
        bass_pattern = [48, 48, 52, 55, 53, 52, 50, 48]  # Ritmik bas dizisi
        current_time = 0
        for _ in range(4):  # 4 kez tekrarla
            for note in bass_pattern:
                freq = midi_to_freq(note)
                sco_content += f"i 12 {current_time} 0.4 {freq} 0.5\n"
                current_time += 0.5
        
        # "Tehllike" hissi veren notalar
        tension_notes = [(55, 0.3), (56, 0.2), (62, 0.3)]
        current_time = 0.25  # Çeyrek saniye gecikmeli başla
        for _ in range(2):  # 2 kez tekrarla
            for note, amp in tension_notes:
                freq = midi_to_freq(note)
                sco_content += f"i 11 {current_time} 4 {freq} {amp}\n"
                current_time += 4
        
        sco_content += "\ne\n"
    
    elif music_name == "cave_music":
        sco_content = """
        ; Mağara müziği (yankılı, ürpertici)
        f 1 0 8192 10 1 0.5 0.3 0.2 0.1
        
        """
        
        # Derin bas notalar
        bass_notes = [36, 35, 39, 38]  # Derin bas notalar
        current_time = 0
        for _ in range(3):  # 3 kez tekrarla
            for note in bass_notes:
                freq = midi_to_freq(note)
                sco_content += f"i 12 {current_time} 3 {freq} 0.4\n"
                current_time += 3.5  # 3.5 saniye sonra sonraki nota
        
        # Atmosferik sesler
        atmos_notes = [(47, 0.1), (50, 0.05), (54, 0.08)]
        current_time = 0.5  # Yarım saniye gecikmeli başla
        for _ in range(2):  # 2 kez tekrarla
            for note, amp in atmos_notes:
                freq = midi_to_freq(note)
                sco_content += f"i 11 {current_time} 8 {freq} {amp}\n"
                current_time += 8.5
        
        sco_content += "\ne\n"
    
    with open(sco_path, "w") as f:
        f.write(sco_content)
    
    return sco_path

# CSound ile ses oluştur
def generate_sound(orc_path, sco_path, output_path):
    """CSound kullanarak ses dosyası oluşturur"""
    try:
        subprocess.run([
            'csound', 
            '-o', output_path, 
            '-W', 
            '-d', 
            orc_path, 
            sco_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return os.path.exists(output_path)
    except Exception as e:
        print(f"Ses oluşturma hatası: {e}")
        return False

# Tüm ses efektlerini oluştur
def create_all_sound_effects(orc_path, temp_dir):
    """Tüm ses efektlerini oluşturur"""
    # Ses efektleri listesi
    effects = [
        "menu_select", 
        "level_up", 
        "attack", 
        "damage", 
        "item_pickup", 
        "quest_complete", 
        "spirit_transform", 
        "door_open"
    ]
    
    for effect in effects:
        print(f"{effect} ses efekti oluşturuluyor...")
        sco_path = create_effect_sco(temp_dir, effect)
        output_path = os.path.join(EFFECTS_DIR, f"{effect}.wav")
        
        if generate_sound(orc_path, sco_path, output_path):
            print(f"{effect}.wav başarıyla oluşturuldu.")
        else:
            print(f"{effect}.wav oluşturulurken hata.")

# Tüm müzik parçalarını oluştur
def create_all_music(orc_path, temp_dir):
    """Tüm müzik parçalarını oluşturur"""
    # Müzik parçaları listesi
    music_tracks = [
        "menu_music", 
        "valley_music", 
        "forest_music", 
        "combat_music", 
        "cave_music"
    ]
    
    for track in music_tracks:
        print(f"{track} müziği oluşturuluyor...")
        sco_path = create_music_sco(temp_dir, track)
        output_path = os.path.join(MUSIC_DIR, f"{track}.wav")
        
        if generate_sound(orc_path, sco_path, output_path):
            print(f"{track}.wav başarıyla oluşturuldu.")
        else:
            print(f"{track}.wav oluşturulurken hata.")

# CSound mevcut değilse alternatif olarak kullanılacak ses dosyalarını oluştur
def create_dummy_sounds():
    """CSound yoksa basit ses dosyaları oluşturur (sessiz veya beyaz gürültü)"""
    import numpy as np
    from scipy.io import wavfile
    
    print("CSound bulunamadı, basit ses dosyaları oluşturuluyor...")
    
    # Ses efektleri listesi
    effects = [
        "menu_select", 
        "level_up", 
        "attack", 
        "damage", 
        "item_pickup", 
        "quest_complete", 
        "spirit_transform", 
        "door_open"
    ]
    
    # Müzik parçaları listesi
    music_tracks = [
        "menu_music", 
        "valley_music", 
        "forest_music", 
        "combat_music", 
        "cave_music"
    ]
    
    # Ses efektleri oluştur
    for effect in effects:
        output_path = os.path.join(EFFECTS_DIR, f"{effect}.wav")
        
        # Kısa bir ses efekti (0.5 saniye)
        duration = 0.5  # saniye
        sample_rate = 44100  # örnekleme hızı (Hz)
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Basit bir zil sesi
        if effect in ["menu_select", "level_up", "item_pickup", "quest_complete"]:
            freq = 440 if effect == "menu_select" else 880  # A4 veya A5
            signal = 0.5 * np.sin(2 * np.pi * freq * t) * np.exp(-5 * t)
        else:  # Gürültü bazlı efektler
            signal = np.random.normal(0, 0.1, int(sample_rate * duration))
            signal = signal * np.exp(-5 * t)
        
        # Stereo ses için çift kanal
        stereo_signal = np.column_stack((signal, signal))
        
        # WAV olarak kaydet
        wavfile.write(output_path, sample_rate, stereo_signal.astype(np.float32))
        print(f"{effect}.wav başarıyla oluşturuldu (alternatif).")
    
    # Müzik parçaları oluştur
    for track in music_tracks:
        output_path = os.path.join(MUSIC_DIR, f"{track}.wav")
        
        # Uzun bir müzik parçası (10 saniye)
        duration = 10.0  # saniye
        sample_rate = 44100  # örnekleme hızı (Hz)
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Basit bir sentetik müzik
        freqs = [261.63, 329.63, 392.00]  # C4, E4, G4 - C major akor
        signal = np.zeros_like(t)
        
        for freq in freqs:
            signal += 0.2 * np.sin(2 * np.pi * freq * t)
        
        # Hacim zarfı
        envelope = np.ones_like(t)
        envelope[:int(0.1 * sample_rate)] = np.linspace(0, 1, int(0.1 * sample_rate))
        envelope[-int(0.1 * sample_rate):] = np.linspace(1, 0, int(0.1 * sample_rate))
        
        signal = signal * envelope
        
        # Stereo ses için çift kanal
        stereo_signal = np.column_stack((signal, signal))
        
        # WAV olarak kaydet
        wavfile.write(output_path, sample_rate, stereo_signal.astype(np.float32))
        print(f"{track}.wav başarıyla oluşturuldu (alternatif).")

def main():
    """Ana fonksiyon"""
    print("Erdem Dünyası ses assetleri oluşturuluyor...")
    
    # Klasörleri oluştur
    os.makedirs(EFFECTS_DIR, exist_ok=True)
    os.makedirs(MUSIC_DIR, exist_ok=True)
    
    # CSound kontrolü yap
    if check_csound():
        print("CSound bulundu, ses assetleri oluşturuluyor...")
        
        # Geçici dizin oluştur
        with tempfile.TemporaryDirectory() as temp_dir:
            # Orkestra dosyasını oluştur
            orc_path = create_orc_file(temp_dir)
            
            # Ses efektlerini oluştur
            create_all_sound_effects(orc_path, temp_dir)
            
            # Müzik parçalarını oluştur
            create_all_music(orc_path, temp_dir)
    else:
        print("CSound bulunamadı! Alternatif yöntemle ses dosyaları oluşturulacak.")
        try:
            # Alternatif olarak numpy ve scipy ile basit ses dosyaları oluştur
            create_dummy_sounds()
        except ImportError:
            print("Ses oluşturmak için gerekli kütüphaneler (numpy ve scipy) bulunamadı.")
            print("Ses dosyaları oluşturulamadı!")
    
    print("İşlem tamamlandı.")

if __name__ == "__main__":
    main() 