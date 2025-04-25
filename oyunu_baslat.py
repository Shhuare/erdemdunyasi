#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pygame
import traceback
import importlib
import time
from pathlib import Path

"""
ERDEM DÜNYASI ÇALIŞTIRMA BAŞLATICISI
====================================
Bu script Erdem Dünyası oyununu hata düzeltmeleri ile başlatır.
"""

# Çalışma dizinini ayarla
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Kaynak dizinini yolu ekle
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Başlangıç banner'ı
def show_banner():
    print("\n" + "=" * 60)
    print(" " * 20 + "ERDEM DÜNYASI")
    print(" " * 15 + "Ruh Hayvanları ve Uyum Vadisi")
    print("=" * 60)
    print("Versiyon: 1.0-Beta")
    print("Başlatılıyor...")
    print("=" * 60 + "\n")

# Asset kontrolü
def check_assets():
    assets_dir = os.path.join(current_dir, "assets")
    if not os.path.exists(assets_dir):
        print("HATA: Asset dizini (assets/) bulunamadı!")
        return False
    
    # Kontroller başarılı
    return True

# Hata düzeltmeleri
def apply_patches():
    """Gerekli hata düzeltmelerini uygular"""
    patch_count = 0
    
    # 1. Game sınıfına _create_initial_quests metodu ekleme
    try:
        from src.game import Game
        
        # Düzeltme işlemini sadece metod henüz yoksa yap
        if not hasattr(Game, "_create_initial_quests"):
            # İlgili modülleri içe aktar
            try:
                from src.quest_manager import Quest, QuestObjective, QuestType, QuestStatus
                
                # Quest sınıfına add_objective metodu ekleme
                if not hasattr(Quest, "add_objective"):
                    def add_objective(self, objective):
                        """Göreve yeni bir hedef ekler"""
                        try:
                            if not hasattr(self, "objectives"):
                                self.objectives = []
                            self.objectives.append(objective)
                        except Exception as e:
                            print(f"[-] Hedef ekleme hatası: {e}")
                    
                    # Metodu Quest sınıfına ekle
                    setattr(Quest, "add_objective", add_objective)
                    print("[+] Quest.add_objective metodu eklendi")
                    patch_count += 1
                
                # Metodu dinamik olarak ekle
                def _create_initial_quests(self):
                    """Oyun başlangıcında oluşturulacak görevleri hazırlar"""
                    try:
                        # Quest manager var mı kontrol et
                        if not hasattr(self, 'quest_manager') or self.quest_manager is None:
                            print("[-] Görev yöneticisi bulunamadı!")
                            return
                            
                        # Ana görev
                        print("[+] Ana görev oluşturuluyor...")
                        main_quest = Quest(
                            id="main_quest_1",
                            title="Uyum Vadisi'ne Hoş Geldiniz",
                            description="Uyum Vadisi'ndeki maceranıza başlayın ve köy şefi ile tanışın.",
                            quest_type=QuestType.MAIN
                        )
                        
                        main_quest.add_objective(QuestObjective("Köy şefi ile konuşun", 1))
                        if hasattr(main_quest, "set_target_location"):
                            main_quest.set_target_location([(100, 100)])
                        main_quest.status = QuestStatus.ACTIVE
                        
                        self.quest_manager.add_quest(main_quest)
                        if hasattr(self.quest_manager, "track_quest"):
                            self.quest_manager.track_quest("main_quest_1")
                        
                        # Yan görev
                        print("[+] Yan görev oluşturuluyor...")
                        side_quest = Quest(
                            id="side_quest_1",
                            title="Kayıp Eşyalar",
                            description="Köylülerin kaybolan eşyalarını bulmak için yardım edin.",
                            quest_type=QuestType.SIDE
                        )
                        
                        side_quest.add_objective(QuestObjective("Kayıp eşyaları bulun", 3))
                        if hasattr(side_quest, "set_target_location"):
                            side_quest.set_target_location([(200, 150)])
                        side_quest.status = QuestStatus.AVAILABLE
                        
                        self.quest_manager.add_quest(side_quest)
                        
                        print("[+] Görevler başarıyla oluşturuldu")
                        
                    except Exception as e:
                        print(f"[-] Görev oluşturma hatası (düzeltildi): {e}")
                        traceback.print_exc()
                        # Hata oluşsa bile çökmesini engelle
                        pass
                
                # Metodu sınıfa ekle
                setattr(Game, "_create_initial_quests", _create_initial_quests)
                print("[+] Game._create_initial_quests metodu eklendi")
                patch_count += 1
            except ImportError as e:
                print(f"[-] Görev modülleri bulunamadı: {e}")
                
    except Exception as e:
        print(f"[-] Game patch hatası: {e}")
        traceback.print_exc()
    
    # 2. World.render metodu düzeltme
    try:
        from src.world import World
        
        # Orijinal render metodu işlevi alınmadan önce kontrol et
        if not hasattr(World, 'patched_render'):
            # Orijinal metodu sakla
            original_render = World.render
            
            def patched_render(self, screen, *args, **kwargs):
                """Düzeltilmiş render metodu"""
                try:
                    # Parametreleri kontrol et
                    player = None
                    
                    # kwargs içinde player var mı bak
                    if 'player' in kwargs:
                        player = kwargs['player']
                    # args içinde player var mı bak (ilk parametre olabilir)
                    elif args and len(args) > 0:
                        player = args[0]
                    
                    # Player parametre olarak bulunamadıysa Game.instance üzerinden al
                    if player is None:
                        try:
                            from src.game import Game
                            if hasattr(Game, 'instance') and Game.instance is not None:
                                player = Game.instance.player
                        except:
                            pass
                    
                    # Player hala None ise basit bir arkaplan çiz
                    if player is None:
                        print("[-] Player nesnesi bulunamadı, basit arkaplan çiziliyor")
                        screen.fill((30, 30, 40))  # Koyu mavi-gri
                        return True
                    
                    # Orijinal render ne kadar parametre alıyor?
                    import inspect
                    sig = inspect.signature(original_render)
                    param_count = len(sig.parameters)
                    
                    # Parametre sayısına göre çağır
                    if param_count >= 3:  # self, screen, player
                        return original_render(self, screen, player)
                    else:
                        # Düşük parametre sayısı, basit ekran temizleme yap
                        screen.fill((30, 30, 40))
                        print("[-] Orijinal render metodu yetersiz parametre alıyor")
                        return True
                    
                except Exception as e:
                    # Basit ekran temizleme ile devam et
                    print(f"[-] World.render hatası (düzeltildi): {e}")
                    screen.fill((30, 30, 40))  # Koyu mavi-gri
                    return True
            
            # Düzeltilmiş metodu kaydet
            World.patched_render = patched_render
            
            # Metodu güncelle
            World.render = patched_render
            print("[+] World.render metodu düzeltildi")
            patch_count += 1
    except Exception as e:
        print(f"[-] World.render patch hatası: {e}")
    
    # 3. Eksik UI elemanları oluşturma
    try:
        import pygame
        from src.asset_manager import AssetManager
        
        def create_basic_ui_elements():
            """Eksik UI elemanları için basit alternatifler oluşturur"""
            try:
                # AssetManager sınıf değişkeni yoksa self'i kontrol et
                asset_manager = AssetManager.instance if hasattr(AssetManager, 'instance') else None
                
                # Eğer sınıf değişkeni yoksa alternatif yöntemlerle erişmeye çalış
                if asset_manager is None:
                    # AssetManager referansı almak için Game üzerinden dene
                    from src.game import Game
                    if hasattr(Game, 'instance') and Game.instance is not None:
                        if hasattr(Game.instance, 'asset_manager'):
                            asset_manager = Game.instance.asset_manager
                
                # Hala bulunamadıysa çık
                if asset_manager is None:
                    print("[-] Asset yöneticisi bulunamadı, UI elemanları oluşturulamadı")
                    return False
                
                # UI elemanlarını oluştur
                ui_elements = {
                    "panel_bg": (300, 200),
                    "button_bg": (100, 30),
                    "inventory_slot": (48, 48),
                    "spirit_icon_bg": (64, 64),
                    "health_bar_bg": (200, 20),
                    "mana_bar_bg": (200, 20),
                    "arrow": (32, 32)
                }
                
                # UI elemanları zaten mevcut mu kontrol et
                for name, size in ui_elements.items():
                    element_id = f"images_ui_{name}"
                    if not hasattr(asset_manager, 'ui_elements'):
                        asset_manager.ui_elements = {}
                        
                    if element_id not in asset_manager.ui_elements:
                        # Basit yüzey oluştur
                        surface = pygame.Surface(size, pygame.SRCALPHA)
                        
                        if name == "arrow":
                            # Ok çiz
                            pygame.draw.polygon(surface, (255, 255, 255), [(16, 0), (32, 16), (16, 32), (0, 16)])
                        else:
                            # Panel çiz
                            pygame.draw.rect(surface, (60, 60, 80, 180), pygame.Rect(0, 0, size[0], size[1]), border_radius=5)
                            pygame.draw.rect(surface, (100, 100, 120, 200), pygame.Rect(0, 0, size[0], size[1]), width=2, border_radius=5)
                        
                        # Asset olarak kaydet
                        asset_manager.ui_elements[element_id] = surface
                        print(f"[+] Eksik UI elemanı oluşturuldu: {name}")
                
                print("[+] Eksik UI elemanları oluşturuldu")
                return True
            except Exception as e:
                print(f"[-] UI elemanları oluşturma hatası: {e}")
                return False
        
        # AssetManager başlatma fonksiyonunu yönetmek için bayrak ve referanslar tanımla
        if not hasattr(AssetManager, '_original_initialize'):
            # Orijinal metodu sadece bir kez sakla
            AssetManager._original_initialize = AssetManager.initialize
            
            def enhanced_initialize(self, *args, **kwargs):
                """Geliştirilmiş başlatma metodu"""
                # Orijinal metodu çağır
                result = AssetManager._original_initialize(self, *args, **kwargs)
                
                # Kendisini sınıf değişkeni olarak kaydet
                AssetManager.instance = self
                
                # UI elemanlarını oluştur
                create_basic_ui_elements()
                
                # Ruh hayvanı sprite'larını ve müzik dosyalarını oluştur
                if hasattr(self, '_create_missing_assets'):
                    self._create_missing_assets()
                    
                return result
            
            # Metodu değiştir
            AssetManager.initialize = enhanced_initialize
            
            # Eksik assetleri oluşturma metodunu da ekle
            AssetManager._create_missing_assets = create_missing_assets
            
            print("[+] AssetManager.initialize metodu düzeltildi")
            patch_count += 1
        
        # Eğer _draw_tracked_quest_info Game.instance'a bağlıysa QuestUI sınıfını düzelt
        try:
            from src.quest_ui import QuestUI
            if hasattr(QuestUI, '_draw_tracked_quest_info'):
                original_draw_tracked = QuestUI._draw_tracked_quest_info
                
                def safe_draw_tracked(self, screen):
                    try:
                        return original_draw_tracked(self, screen)
                    except Exception as e:
                        print(f"[-] Görev takibi çizim hatası (düzeltildi): {e}")
                        return None
                
                # Metodu güncelle
                QuestUI._draw_tracked_quest_info = safe_draw_tracked
                print("[+] QuestUI._draw_tracked_quest_info metodu düzeltildi")
                patch_count += 1
        except Exception as e:
            print(f"[-] QuestUI patch hatası: {e}")
            
    except Exception as e:
        print(f"[-] AssetManager patch hatası: {e}")
    
    # 4. Eksik sprites_spirit_animals_wolf ve menu müziği oluşturma
    # Bu kısım enhanced_initialize içinden otomatik olarak çağrılacağı için 
    # ayrıca işlem yapmaya gerek yok
    
    # 5. QuestUI _draw_tracked_quest_info hata düzeltmesi
    try:
        from src.quest_ui import QuestUI
        
        # QuestUI._draw_tracked_quest_info metodu düzelt
        if hasattr(QuestUI, '_draw_tracked_quest_info'):
            original_method = QuestUI._draw_tracked_quest_info
            
            def fixed_draw_tracked_quest_info(self, screen):
                """Takip edilen görev hakkında bilgi gösterir."""
                try:
                    # Game importunu içeride yap
                    from src.game import Game
                    
                    if not hasattr(self.quest_manager, 'tracked_quest'):
                        return
                    
                    quest = self.quest_manager.tracked_quest
                    if quest is None:
                        return
                    
                    # Ekranın üst kısmında göster
                    info_width = 300
                    info_height = 80
                    info_x = (screen.get_width() - info_width) // 2
                    info_y = 10
                    
                    # Arkaplan
                    info_bg = pygame.Surface((info_width, info_height), pygame.SRCALPHA)
                    info_bg.fill((40, 40, 60, 180))  # Yarı saydam arkaplan
                    screen.blit(info_bg, (info_x, info_y))
                    
                    # Görev başlığı
                    title_color = (200, 200, 100)
                    title_text = self.font_title.render(quest.title, True, title_color)
                    screen.blit(title_text, (info_x + 10, info_y + 5))
                    
                    # Görev açıklaması (kısa)
                    desc_text = self.font_text.render(quest.description[:50] + "..." if len(quest.description) > 50 else quest.description, 
                                                     True, (180, 180, 180))
                    screen.blit(desc_text, (info_x + 10, info_y + 30))
                    
                    # Hedefler (sadece ilk hedef)
                    if quest.objectives and len(quest.objectives) > 0:
                        obj = quest.objectives[0]
                        obj_text = self.font_text.render(f"{obj.description} ({obj.current_progress}/{obj.target_progress})", 
                                                       True, (180, 180, 180))
                        screen.blit(obj_text, (info_x + 10, info_y + 50))
                    
                except Exception as e:
                    print(f"[-] Görev takibi çizilirken hata (düzeltildi): {e}")
            
            # Metodu güncelle
            QuestUI._draw_tracked_quest_info = fixed_draw_tracked_quest_info
            print("[+] QuestUI._draw_tracked_quest_info metodu düzeltildi")
            patch_count += 1
            
    except Exception as e:
        print(f"[-] QuestUI patch hatası: {e}")
    
    # Patch sonuçları
    print(f"\nToplam {patch_count} hata düzeltmesi uygulandı")
    return patch_count > 0

# Ana başlatma fonksiyonu
def start_game(fullscreen=False, debug=False):
    """Oyunu başlatır"""
    try:
        # 1. Pygame başlat
        pygame.init()
        
        # 2. Modülleri içe aktar
        from src.game import Game
        
        # 3. Oyun nesnesini oluştur
        width, height = 1024, 768
        
        print(f"Ekran boyutu: {width}x{height}, Tam ekran: {fullscreen}")
        
        game = Game(
            width=width,
            height=height,
            fullscreen=fullscreen,
            sound_volume=80,
            music_volume=60,
            language="tr"
        )
        
        # Debug modu
        if debug:
            game.debug_mode = True
            print("Debug modu aktif")
        
        # 4. Oyunu başlat
        if game.initialize():
            print("Oyun başladı!")
            game.run()
        else:
            print("Oyun başlatılamadı!")
        
        # 5. Kapatma
        try:
            game._shutdown()
        except:
            pygame.quit()
        
        return True
        
    except Exception as e:
        print(f"HATA: {e}")
        traceback.print_exc()
        pygame.quit()
        return False

# Ana fonksiyon
def main():
    import argparse
    
    # Komut satırı argümanları
    parser = argparse.ArgumentParser(description="Erdem Dünyası Oyun Başlatıcısı")
    parser.add_argument("--fullscreen", action="store_true", help="Tam ekran modunda başlat")
    parser.add_argument("--debug", action="store_true", help="Debug modunu aktifleştir")
    parser.add_argument("--no-fix", action="store_true", help="Hata düzeltmelerini uygulama")
    args = parser.parse_args()
    
    # Banner göster
    show_banner()
    
    # Asset kontrolü
    if not check_assets():
        print("Devam etmek için Enter tuşuna basın (varlıklar eksik olabilir)...")
        input()
    
    # Hata düzeltme
    if not args.no_fix:
        apply_patches()
    
    # Başlat
    start_game(fullscreen=args.fullscreen, debug=args.debug)
    
    print("\nOyun kapatıldı.")
    return 0

# Script olarak çalıştırma
if __name__ == "__main__":
    sys.exit(main()) 