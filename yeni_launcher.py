#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import pygame
import traceback
import subprocess

# Ana dizini paths'e ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Kaynak kodlarının olduğu src klasörünü ekleyelim
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Varlık kontrol fonksiyonu
def check_assets():
    assets_dir = os.path.join(current_dir, "assets")
    if not os.path.exists(assets_dir):
        print("Varlık dizini (assets) bulunamadı!")
        return False
    
    asset_registry = os.path.join(assets_dir, "asset_registry.json")
    if not os.path.exists(asset_registry):
        print("Varlık kaydı (asset_registry.json) bulunamadı!")
        return False
    
    return True

# Python ve Pygame sürüm kontrol fonksiyonu
def check_versions():
    print(f"Python {sys.version.split()[0]}")
    
    try:
        print(f"pygame {pygame.version.ver}")
        return True
    except Exception as e:
        print(f"Pygame kontrol hatası: {e}")
        return False

# Başlangıç fonksiyonu
def start_game(debug_mode=False, fullscreen=False, skip_intro=False):
    """Oyunu başlatır"""
    print("=" * 60)
    print("                ERDEM DÜNYASI")
    print("           Yeni Çağ'a Hoş Geldiniz")
    print("=" * 60)
    print("Uyum Vadisi'nde geleneksel yaşam ile teknoloji bir arada...")
    print("Ruh hayvanınız ve yeteneklerinizle dünyayı keşfedin!")
    
    if not skip_intro:
        print("Yükleniyor...")
        for _ in range(10):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.1)
        print("\n")
    
    # Pygame başlat
    pygame.init()
    
    # Monkeypatching (Kod yamalaması) fonksiyonları
    def apply_monkeypatches():
        """Eksik veya hatalı fonksiyonları düzeltir"""
        try:
            # Game sınıfı tanımını ekle
            if 'Game' not in globals():
                from src.game import Game
            
            # Dünya render metodunu düzelt
            from src.world import World
            if not hasattr(World, 'original_render') and hasattr(World, 'render'):
                World.original_render = World.render
                
                def patched_render(self, screen, player=None, camera_x=None, camera_y=None):
                    # Game.instance üzerinden player nesnesini al
                    from src.game import Game
                    if player is None and hasattr(Game, 'instance') and Game.instance is not None:
                        player = Game.instance.player
                    
                    # Camera değerlerini de kullan
                    if camera_x is None and hasattr(self, 'camera_x'):
                        camera_x = self.camera_x
                    if camera_y is None and hasattr(self, 'camera_y'):
                        camera_y = self.camera_y
                        
                    if hasattr(self, 'original_render'):
                        # Mevcut parametre yapısına göre çağır
                        sig = getattr(self.original_render, '__code__', None)
                        if sig and sig.co_argcount >= 4:  # self, screen, player parametreleri
                            return self.original_render(screen, player)
                        elif sig and sig.co_argcount >= 4:  # self, screen, camera_x, camera_y
                            return self.original_render(screen, camera_x or 0, camera_y or 0)
                        else:
                            # En fazla 2 parametre alıyorsa
                            return self.original_render(screen)
                    
                    # Orijinal render yoksa basit bir arkaplan çiz
                    screen.fill((30, 30, 40))  # Koyu mavi-gri
                    return True
                
                World.render = patched_render
                print("World.render metodu yamalandı")
                
            # UI elemanları için gerekli varlıkları yükle
            # Eksik UI varlıkları için basit sürümler oluştur
            from src.asset_manager import AssetManager
            if hasattr(AssetManager, 'instance') and AssetManager.instance is not None:
                asset_mgr = AssetManager.instance
                
                # Eksik UI elemanlarını oluştur
                ui_elements = {
                    "panel_bg": (300, 200),
                    "button_bg": (100, 30),
                    "inventory_slot": (48, 48),
                    "spirit_icon_bg": (64, 64),
                    "health_bar_bg": (200, 20),
                    "mana_bar_bg": (200, 20),
                    "arrow": (32, 32)
                }
                
                for name, size in ui_elements.items():
                    element_id = f"images_ui_{name}"
                    if not asset_mgr.get_ui_element(element_id):
                        # Basit bir yüzey oluştur
                        surf = pygame.Surface(size, pygame.SRCALPHA)
                        if name == "arrow":
                            # Ok çiz
                            pygame.draw.polygon(surf, (255, 255, 0), [(16, 0), (32, 16), (16, 32), (0, 16)])
                        else:
                            # Basit dikdörtgen çiz
                            pygame.draw.rect(surf, (60, 60, 80, 180), pygame.Rect(0, 0, size[0], size[1]), border_radius=5)
                            pygame.draw.rect(surf, (100, 100, 120, 200), pygame.Rect(0, 0, size[0], size[1]), width=2, border_radius=5)
                        
                        # Asset olarak kaydet
                        asset_mgr.ui_elements[element_id] = surf
                        print(f"Eksik UI elemanı oluşturuldu: {element_id}")
                        
            # Eksik müzik dosyalarını tanımla
            try:
                from src.audio_manager import AudioManager
                if hasattr(AudioManager, 'instance') and AudioManager.instance is not None:
                    audio_mgr = AudioManager.instance
                    
                    # Eksik müzikleri yükle
                    missing_music = ["menu"]
                    
                    for music_name in missing_music:
                        # Müzik listesini kontrol et
                        from src.constants import MUSIC
                        if music_name in MUSIC:
                            continue  # Zaten tanımlıysa pas geç
                        
                        # Mevcut müziklerden birini kopyala
                        existing_music_found = False
                        for existing_music in MUSIC:
                            if existing_music and existing_music != music_name:
                                # Sabit sözlüğe eksik müziği ekle
                                MUSIC[music_name] = MUSIC[existing_music]
                                print(f"Eksik müzik sabitine alternatif eklendi: {music_name}")
                                existing_music_found = True
                                break
                        
                        # AudioManager instance'ında da güncelle
                        if hasattr(audio_mgr, 'music'):
                            for existing_music_path in audio_mgr.music.values():
                                if existing_music_path:
                                    audio_mgr.music[f"sounds_music_{music_name}"] = existing_music_path
                                    print(f"Eksik müzik yerine alternatif yüklendi: {music_name}")
                                    break
            except Exception as music_error:
                print(f"Müzik yükleme hatası: {music_error}")
                traceback.print_exc()
                
            # Eksik sprite'ları tanımla
            try:
                # Eksik sprite'ları başka sprite'larla değiştir
                missing_sprites = ["sprites_spirit_animals_wolf"]
                
                for sprite_path in missing_sprites:
                    # Asset yöneticisinde eksik sprite'ı kontrol et
                    if hasattr(AssetManager, 'instance') and AssetManager.instance is not None:
                        asset_mgr = AssetManager.instance
                        
                        if hasattr(asset_mgr, 'sprites') and not asset_mgr.get_sprite(sprite_path):
                            # Sprite listesindeki varolan sprite'ları kullan
                            replacement_found = False
                            for existing_sprite in asset_mgr.sprites.keys():
                                if existing_sprite and "spirit_animal" in existing_sprite:
                                    # Varolan farklı bir ruh hayvanı sprite'ını kullan
                                    print(f"Eksik sprite için bulunan alternatif: {existing_sprite}")
                                    # Yeni bir yüzey oluştur ve mevcut sprite'ı kopyala
                                    sprite_surface = asset_mgr.sprites[existing_sprite].copy()
                                    asset_mgr.sprites[sprite_path] = sprite_surface
                                    print(f"Eksik sprite yerine alternatif yüklendi: {sprite_path} -> {existing_sprite}")
                                    replacement_found = True
                                    break
                            
                            # Eğer uygun bir ruh hayvanı bulunamazsa, herhangi bir sprite kullan
                            if not replacement_found:
                                for existing_sprite in asset_mgr.sprites.keys():
                                    if existing_sprite and existing_sprite != sprite_path:
                                        # Herhangi bir sprite'ı kullan
                                        sprite_surface = asset_mgr.sprites[existing_sprite].copy()
                                        asset_mgr.sprites[sprite_path] = sprite_surface
                                        print(f"Eksik sprite yerine genel alternatif yüklendi: {sprite_path} -> {existing_sprite}")
                                        break
                            
                            # Hala sprite bulunamadıysa yeni bir sprite oluştur
                            if sprite_path not in asset_mgr.sprites:
                                # Geçici bir sprite oluştur
                                temp_sprite = pygame.Surface((64, 64), pygame.SRCALPHA)
                                pygame.draw.circle(temp_sprite, (100, 200, 255), (32, 32), 30)
                                pygame.draw.circle(temp_sprite, (50, 100, 200), (32, 32), 30, 2)
                                # Wolf şekli için kulaklar ve burun ekle
                                pygame.draw.polygon(temp_sprite, (80, 80, 80), [(20, 10), (25, 25), (15, 25)])
                                pygame.draw.polygon(temp_sprite, (80, 80, 80), [(44, 10), (49, 25), (39, 25)])
                                pygame.draw.ellipse(temp_sprite, (50, 50, 50), (28, 35, 8, 5))
                                
                                asset_mgr.sprites[sprite_path] = temp_sprite
                                print(f"Eksik sprite için geçici sprite oluşturuldu: {sprite_path}")
            except Exception as sprite_error:
                print(f"Sprite yükleme hatası: {sprite_error}")
                traceback.print_exc()
                
            # QuestUI'a Game referansı ekle
            try:
                import sys
                from src.game import Game
                # quest_ui.py'yi doğrudan modifiye et
                # Önce modülün varlığını kontrol et
                if 'quest_ui' in sys.modules:
                    sys.modules['quest_ui'].Game = Game
                elif 'src.quest_ui' in sys.modules:
                    sys.modules['src.quest_ui'].Game = Game
                else:
                    # Modülü import et ve Game'i ekle
                    import importlib
                    quest_ui_module = importlib.import_module('src.quest_ui')
                    quest_ui_module.Game = Game
            except Exception as e:
                print(f"QuestUI'a Game referansı eklenirken hata: {e}")
                traceback.print_exc()
                
            print("Monkeypatching tamamlandı")
            return True
            
        except Exception as e:
            print(f"Monkeypatching hatası: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    # Ana oyunu yükle
    try:
        # Önce gerekli düzeltmeleri uygula
        apply_monkeypatches()
        
        # Ana oyun modülünü yükle
        from src.game import Game
        
        # Ekran boyutunu belirle
        width, height = 1024, 768
        
        # Oyun nesnesini oluştur
        game_instance = Game(
            width=width,
            height=height,
            fullscreen=fullscreen,
            sound_volume=80,
            music_volume=60,
            language="tr"
        )
        
        # Debug modu ayarla
        if debug_mode:
            game_instance.debug_mode = True
            print("Debug modu açık.")
        
        # Oyunu başlat
        if game_instance.initialize():
            # Hata yakalama ile oyun döngüsünü başlat
            try:
                print("Oyun başlıyor...")
                game_instance.run()
            except Exception as e:
                print(f"Oyun çalıştırılırken hata oluştu: {e}")
                traceback.print_exc()
            finally:
                try:
                    game_instance._shutdown()
                except:
                    pass
                print("Oyun sonlandırılıyor...")
        else:
            print("Oyun başlatılamadı!")
            
    except Exception as e:
        print(f"Oyun yüklenirken hata oluştu: {e}")
        traceback.print_exc()
    
    # Pygame kapat
    pygame.quit()

# Varlıkları yapılandır
def configure_assets():
    """Varlıkları yapılandırır ve kontrol eder"""
    print("Varlıklar kontrol ediliyor...")
    
    if not check_assets():
        # Varlık yapılandırma batch dosyasını çalıştır
        configure_batch = os.path.join(current_dir, "configure_assets.bat")
        if os.path.exists(configure_batch):
            print("Varlıklar yapılandırılıyor...")
            try:
                subprocess.run(configure_batch, shell=True, check=True)
                print("Varlıklar başarıyla yapılandırıldı.")
                return True
            except subprocess.CalledProcessError:
                print("Varlık yapılandırma hatası!")
                return False
        else:
            print("Varlık yapılandırma dosyası bulunamadı!")
            return False
    return True

# Ana başlatıcı fonksiyonu
def main():
    """Ana başlatıcı fonksiyonu"""
    import argparse
    
    # Komut satırı argümanlarını ayarla
    parser = argparse.ArgumentParser(description="Erdem Dünyası Oyun Başlatıcısı")
    parser.add_argument("--debug", action="store_true", help="Debug modunu aktifleştirir")
    parser.add_argument("--fullscreen", action="store_true", help="Tam ekran modunda başlatır")
    parser.add_argument("--skip-intro", action="store_true", help="Giriş animasyonunu atlar")
    parser.add_argument("--no-asset-check", action="store_true", help="Varlık kontrolünü atlar")
    
    args = parser.parse_args()
    
    # Sürüm kontrolü
    print("Erdem Dünyası - Başlatıcı")
    print("========================")
    print("Python kontrolu yapiliyor...")
    if not check_versions():
        print("Hata: Python veya Pygame kurulumu eksik veya hatalı!")
        return
    
    # Varlık kontrolü
    if not args.no_asset_check:
        if not configure_assets():
            print("Hata: Varlık yapılandırma işlemi başarısız!")
            return
    
    # Oyunu başlat
    print("Erdem Dünyası başlatılıyor...")
    start_game(
        debug_mode=args.debug,
        fullscreen=args.fullscreen,
        skip_intro=args.skip_intro
    )

if __name__ == "__main__":
    main() 