#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
import time
import argparse
import importlib
import subprocess
import pkg_resources

def check_required_modules():
    """
    Gerekli modüllerin yüklü olup olmadığını kontrol eder.
    Eksik modülleri listeler ve yükleme önerisi sunar.
    
    Returns:
        tuple: (Tüm modüller tamam mı?, Eksik modüller listesi)
    """
    required_modules = {
        "pygame": "2.0.0",
        "pytmx": "3.31",
        "numpy": "1.19.0",
        "PIL": "8.0.0",  # PIL/Pillow
        "pathlib": "1.0.0"
    }
    
    missing_modules = []
    
    for module_name, min_version in required_modules.items():
        try:
            # Modülü içe aktarmayı dene
            if module_name == "PIL":
                # PIL için özel kontrol
                try:
                    import PIL
                    version = PIL.__version__
                    print(f"PIL/Pillow sürümü: {version}")
                except ImportError:
                    missing_modules.append(f"pillow (Bulunamadı)")
                    continue
            else:
                module = importlib.import_module(module_name)
                
                # Sürüm kontrolü (bazı modüllerde farklı sürüm formatları olabilir)
                if module_name == "pygame":
                    version = pygame.version.ver
                else:
                    try:
                        version = pkg_resources.get_distribution(module_name).version
                    except:
                        version = getattr(module, "__version__", "0.0.0")
            
            # Minimum sürüm kontrolü
            if pkg_resources.parse_version(version) < pkg_resources.parse_version(min_version):
                missing_modules.append(f"{module_name} (Mevcut: {version}, Gerekli: {min_version})")
                
        except ImportError:
            missing_modules.append(f"{module_name} (Bulunamadı)")
    
    return len(missing_modules) == 0, missing_modules

def install_missing_modules(modules):
    """
    Eksik modülleri yüklemeyi dener.
    
    Args:
        modules (list): Eksik modüllerin listesi
        
    Returns:
        bool: Tüm modüller başarıyla yüklendiyse True, aksi halde False
    """
    print("Eksik modüller yükleniyor...")
    
    for module in modules:
        module_name = module.split(" ")[0]
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            print(f"{module_name} başarıyla yüklendi.")
        except subprocess.CalledProcessError:
            print(f"{module_name} yüklenirken hata oluştu!")
            return False
    
    return True

def main():
    """
    Ana program.
    """
    # Komut satırı argümanlarını işle
    parser = argparse.ArgumentParser(description='Erdem Dünyası')
    parser.add_argument('--from-launcher', action='store_true', help='Başlatıcıdan açıldı')
    parser.add_argument('--install-modules', action='store_true', help='Eksik modülleri otomatik yükle')
    args = parser.parse_args()
    
    # Launcher'dan başlatıldıysa
    if args.from_launcher:
        print("Oyun launcher'dan başlatıldı")
    
    # Gerekli modülleri kontrol et
    modules_ok, missing_modules = check_required_modules()
    
    # Eksik modül varsa
    if not modules_ok:
        print("Eksik modüller tespit edildi:")
        for module in missing_modules:
            print(f" - {module}")
        
        # Otomatik yükleme seçeneği
        if args.install_modules:
            if install_missing_modules(missing_modules):
                print("Tüm eksik modüller yüklendi. Oyun başlatılıyor...")
            else:
                print("Eksik modüller yüklenemedi. Lütfen manuel olarak yükleyin.")
                return
        else:
            print("\nEksik modülleri yüklemek için:")
            print(f"{sys.executable} {sys.argv[0]} --install-modules")
            print("\nveya manuel olarak şu komutları çalıştırın:")
            for module in missing_modules:
                module_name = module.split(" ")[0]
                print(f"pip install {module_name}")
            return
    
    # Pygame'i başlat
    pygame.init()
    pygame.mixer.init()
    
    # Ekranı oluştur
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Erdem Dünyası")
    
    # Renkler
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    
    # Font
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 36)
    font_small = pygame.font.SysFont(None, 24)
    
    # Uygulama başlığı
    title_text = font_large.render("Erdem Dünyası", True, YELLOW)
    title_rect = title_text.get_rect(center=(screen_width // 2, 100))
    
    # Kontroller
    controls = [
        "W, A, S, D: Hareket etme",
        "R: Normal saldırı",
        "Z: En yakın düşmanı seçme",
        "E: Etkileşim",
        "1-4: Ruh hayvanı yetenekleri",
        "B: Banka sistemi",
        "Sağ fare: Hareket et",
        "Sol fare: Düşman/NPC seç"
    ]
    
    # Yeni özellikler
    features = [
        "Banka Sistemi",
        "Yetenek Çubuğu",
        "Gelişmiş Hedefleme",
        "Ruh Hayvanı Dönüşümü"
    ]
    
    def draw_controls():
        """Kontrolleri çizer."""
        header = font_medium.render("Kontroller", True, CYAN)
        screen.blit(header, (50, 180))
        
        for i, text in enumerate(controls):
            control_text = font_small.render(text, True, WHITE)
            screen.blit(control_text, (50, 220 + i * 30))
    
    def draw_features():
        """Yeni özellikleri çizer."""
        header = font_medium.render("Yeni Özellikler", True, CYAN)
        screen.blit(header, (450, 180))
        
        for i, text in enumerate(features):
            feature_text = font_small.render(text, True, WHITE)
            screen.blit(feature_text, (450, 220 + i * 30))
    
    def draw_message():
        """Bilgi mesajını çizer."""
        message1 = font_medium.render("Tüm modüller yüklendi! Oyun çalışmaya hazır.", True, GREEN)
        message2 = font_small.render("Geliştirme tamamlandığında tam oyun burada çalışacak.", True, WHITE)
        message3 = font_small.render("ESC tuşuna basarak çıkabilirsiniz.", True, WHITE)
        
        screen.blit(message1, (screen_width // 2 - message1.get_width() // 2, 450))
        screen.blit(message2, (screen_width // 2 - message2.get_width() // 2, 490))
        screen.blit(message3, (screen_width // 2 - message3.get_width() // 2, 520))
    
    # Ana döngü
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # Olayları işle
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        # Ekranı temizle
        screen.fill(BLACK)
        
        # Başlık ve bilgileri çiz
        screen.blit(title_text, title_rect)
        draw_controls()
        draw_features()
        draw_message()
        
        # Ekranı güncelle
        pygame.display.flip()
        clock.tick(60)
    
    # Pygame'i kapat
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 