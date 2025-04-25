#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Erdem Dünyası logosu ve ikonunu oluşturan betik.
Bu betik PIL (Pillow) kütüphanesini kullanarak basit bir logo ve ikon oluşturur.
"""

import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_logo():
    """Logo ve ikonu oluşturur"""
    # Dizinleri oluştur
    os.makedirs("assets/images", exist_ok=True)
    
    # Logo boyutları
    width, height = 500, 300
    
    # Renkler
    bg_color = (44, 62, 80)  # Koyu mavi
    text_color = (52, 152, 219)  # Açık mavi
    accent_color = (231, 76, 60)  # Kırmızı
    
    # Yeni resim oluştur
    logo = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(logo)
    
    # Fontu yüklemeye çalış, yoksa varsayılan font kullan
    font_size = 60
    try:
        font_path = None
        # Yaygın font dizinlerini kontrol et
        font_dirs = [
            "C:/Windows/Fonts",
            "/usr/share/fonts/truetype",
            "/System/Library/Fonts",
            os.path.expanduser("~/Library/Fonts")
        ]
        
        # Yaygın yazı tiplerini kontrol et
        font_names = [
            "arial.ttf", "Arial.ttf",
            "arialbd.ttf", "Arialbd.ttf",
            "times.ttf", "Times.ttf",
            "DejaVuSans.ttf", "DejaVuSans-Bold.ttf",
            "Verdana.ttf", "Verdana-Bold.ttf"
        ]
        
        for font_dir in font_dirs:
            if not os.path.exists(font_dir):
                continue
                
            for font_name in font_names:
                font_path_check = os.path.join(font_dir, font_name)
                if os.path.exists(font_path_check):
                    font_path = font_path_check
                    break
            
            if font_path:
                break
                
        if font_path:
            title_font = ImageFont.truetype(font_path, font_size)
            subtitle_font = ImageFont.truetype(font_path, font_size // 2)
        else:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    except Exception as e:
        print(f"Font yüklenirken hata: {e}")
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Logo metni
    title_text = "ERDEM DÜNYASI"
    subtitle_text = "Uyum Vadisi"
    
    # Metin boyutunu al
    try:
        title_width = draw.textlength(title_text, font=title_font)
    except:
        # PIL eski sürümleri için
        title_width = title_font.getlength(title_text) if hasattr(title_font, 'getlength') else 300
        
    # Ortalanmış metin
    title_position = ((width - title_width) // 2, 80)
    
    # Metni çiz
    draw.text(title_position, title_text, fill=text_color, font=title_font)
    
    # Alt başlık
    try:
        subtitle_width = draw.textlength(subtitle_text, font=subtitle_font)
    except:
        # PIL eski sürümleri için
        subtitle_width = subtitle_font.getlength(subtitle_text) if hasattr(subtitle_font, 'getlength') else 150
        
    subtitle_position = ((width - subtitle_width) // 2, 160)
    draw.text(subtitle_position, subtitle_text, fill=accent_color, font=subtitle_font)
    
    # Süsleyici şekil (ruh hayvanı simgesi)
    draw.ellipse((width//2 - 25, 30, width//2 + 25, 80), outline=accent_color, width=3)
    
    # Logoyu kaydet
    logo_path = os.path.join("assets", "images", "logo.png")
    logo.save(logo_path)
    print(f"Logo oluşturuldu: {logo_path}")
    
    # İkon oluştur (daha küçük)
    icon_size = (64, 64)
    icon = Image.new("RGBA", icon_size, bg_color)
    icon_draw = ImageDraw.Draw(icon)
    
    # İkon için basit bir hayvan silüeti çiz
    # Tilki kulak şekli
    icon_draw.polygon([(15, 15), (32, 5), (49, 15)], fill=accent_color)
    # Yüz
    icon_draw.ellipse((15, 15, 49, 49), fill=text_color)
    # Göz
    icon_draw.ellipse((22, 25, 28, 31), fill=bg_color)
    icon_draw.ellipse((36, 25, 42, 31), fill=bg_color)
    # Burun
    icon_draw.polygon([(32, 35), (28, 40), (36, 40)], fill=bg_color)
    
    # İkonu kaydet
    icon_path = os.path.join("assets", "images", "icon.png")
    icon.save(icon_path)
    print(f"İkon oluşturuldu: {icon_path}")
    
    # Windows için ICO formatı
    try:
        icon_ico_path = os.path.join("assets", "images", "icon.ico")
        icon.save(icon_ico_path, format="ICO", sizes=[(64, 64), (32, 32), (16, 16)])
        print(f"ICO ikon oluşturuldu: {icon_ico_path}")
    except Exception as e:
        print(f"ICO formatı kaydedilirken hata: {e}")

if __name__ == "__main__":
    print("Erdem Dünyası logo ve ikonları oluşturuluyor...")
    create_logo()
    print("İşlem tamamlandı.") 