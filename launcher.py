#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import pygame
import traceback
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from pathlib import Path
import importlib
import pkg_resources
import threading
import json

# Ana dizini paths'e ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Kaynak kodlarının olduğu src klasörünü ekleyelim
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

class ErdemDunyasiLauncher:
    """
    Erdem Dünyası oyun başlatıcısı.
    
    Bu uygulama:
    - Gerekli bağımlılıkların yüklü olup olmadığını kontrol eder
    - Eksik bağımlılıkları yükler
    - Oyunu başlatır
    - Ayarları yapılandırır
    """
    
    def __init__(self, root):
        """
        Başlatıcı arayüzünü oluşturur.
        
        Args:
            root: Tkinter ana penceresi
        """
        self.root = root
        self.root.title("Erdem Dünyası Başlatıcısı")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        self.root.iconbitmap("assets/images/icon.ico") if os.path.exists("assets/images/icon.ico") else None
        
        # Ayarları yükle
        self.settings = self.load_settings()
        
        # Arka plan rengini ayarla
        self.root.configure(bg="#2c3e50")
        
        # Ana stil ayarları
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 12), background="#3498db", foreground="white")
        style.configure("TLabel", font=("Helvetica", 12), background="#2c3e50", foreground="white")
        style.configure("TFrame", background="#2c3e50")
        style.configure("Header.TLabel", font=("Helvetica", 24, "bold"), background="#2c3e50", foreground="#3498db")
        style.configure("Subheader.TLabel", font=("Helvetica", 16), background="#2c3e50", foreground="#ecf0f1")
        style.configure("Info.TLabel", font=("Helvetica", 10), background="#2c3e50", foreground="#bdc3c7")
        
        # Başlık ve logo çerçevesi
        header_frame = ttk.Frame(root)
        header_frame.pack(pady=20, fill="x")
        
        # Logo ekle (eğer varsa)
        try:
            logo_path = "assets/images/logo.png"
            if os.path.exists(logo_path):
                logo_img = PhotoImage(file=logo_path)
                logo_img = logo_img.subsample(2, 2)  # Boyutu küçült
                logo_label = ttk.Label(header_frame, image=logo_img, background="#2c3e50")
                logo_label.image = logo_img  # Referansı koru
                logo_label.pack()
        except Exception as e:
            print(f"Logo yüklenirken hata: {e}")
        
        # Başlık
        title_label = ttk.Label(header_frame, text="ERDEM DÜNYASI", style="Header.TLabel")
        title_label.pack(pady=10)
        subtitle_label = ttk.Label(header_frame, text="Ruh Hayvanı Sistemi ve Uyum Vadisi", style="Subheader.TLabel")
        subtitle_label.pack()
        
        # Ana içerik çerçevesi
        content_frame = ttk.Frame(root)
        content_frame.pack(padx=50, pady=20, fill="both", expand=True)
        
        # Durum bilgisi
        self.status_frame = ttk.Frame(content_frame)
        self.status_frame.pack(fill="x", pady=10)
        
        self.status_label = ttk.Label(self.status_frame, text="Sistem kontrol ediliyor...", style="Info.TLabel")
        self.status_label.pack(anchor="w", pady=5)
        
        # Bağımlılık durumu
        self.dependencies_frame = ttk.Frame(content_frame)
        self.dependencies_frame.pack(fill="x", pady=10)
        
        dependency_title = ttk.Label(self.dependencies_frame, text="Bağımlılık Durumu:", style="Subheader.TLabel")
        dependency_title.pack(anchor="w", pady=5)
        
        self.dependency_labels = {}
        required_modules = ["pygame", "numpy", "pillow", "pytmx", "pyyaml", "pathlib"]
        
        for module in required_modules:
            frame = ttk.Frame(self.dependencies_frame)
            frame.pack(fill="x", pady=2)
            
            label_name = ttk.Label(frame, text=f"{module}: ", width=12, anchor="e")
            label_name.pack(side="left")
            
            label_status = ttk.Label(frame, text="Kontrol ediliyor...", foreground="#f39c12")
            label_status.pack(side="left", padx=5)
            
            self.dependency_labels[module] = label_status
        
        # Düğmeler çerçevesi
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(pady=20)
        
        # Başlat düğmesi
        self.start_button = ttk.Button(button_frame, text="Oyunu Başlat", command=self.start_game)
        self.start_button.pack(side="left", padx=10)
        self.start_button["state"] = "disabled"  # Başlangıçta devre dışı
        
        # Bağımlılıkları yükle düğmesi
        self.install_button = ttk.Button(button_frame, text="Bağımlılıkları Yükle", command=self.install_dependencies)
        self.install_button.pack(side="left", padx=10)
        self.install_button["state"] = "disabled"  # Başlangıçta devre dışı
        
        # Ayarlar düğmesi
        self.settings_button = ttk.Button(button_frame, text="Ayarlar", command=self.open_settings)
        self.settings_button.pack(side="left", padx=10)
        
        # Yardım düğmesi
        self.help_button = ttk.Button(button_frame, text="Yardım", command=self.open_help)
        self.help_button.pack(side="left", padx=10)
        
        # Durum bilgisi alanı
        self.log_frame = ttk.Frame(content_frame)
        self.log_frame.pack(fill="both", expand=True, pady=10)
        
        log_label = ttk.Label(self.log_frame, text="İşlem Günlüğü:", anchor="w")
        log_label.pack(fill="x")
        
        self.log_text = tk.Text(self.log_frame, height=10, wrap="word", bg="#34495e", fg="#ecf0f1")
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")
        
        # Alt bilgi çerçevesi
        footer_frame = ttk.Frame(root)
        footer_frame.pack(fill="x", pady=10)
        
        version_label = ttk.Label(footer_frame, text="Erdem Dünyası v1.0", style="Info.TLabel")
        version_label.pack(side="left", padx=20)
        
        # Sistem kontrolü başlat
        self.check_dependencies()
    
    def log(self, message):
        """
        Günlük alanına mesaj ekler.
        
        Args:
            message: Eklenecek mesaj
        """
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update()
    
    def check_dependencies(self):
        """
        Gerekli bağımlılıkların yüklü olup olmadığını kontrol eder.
        """
        self.log("Sistem kontrolü başlatılıyor...")
        self.missing_modules = []
        
        # Python'un kendisini kontrol et
        python_version = sys.version.split()[0]
        self.log(f"Python sürümü: {python_version}")
        
        # Tüm modülleri kontrol et
        for module, label in self.dependency_labels.items():
            try:
                if module == "pillow":
                    # PIL/Pillow özel durum
                    import PIL
                    version = PIL.__version__
                    is_installed = True
                else:
                    # Diğer modüller
                    is_installed = importlib.util.find_spec(module) is not None
                    if is_installed:
                        try:
                            version = pkg_resources.get_distribution(module).version
                        except:
                            mod = importlib.import_module(module)
                            version = getattr(mod, "__version__", "Bilinmiyor")
                    else:
                        version = "Yüklü değil"
                
                if is_installed:
                    label.config(text=f"Yüklü (v{version})", foreground="#2ecc71")
                else:
                    label.config(text="Yüklü değil", foreground="#e74c3c")
                    self.missing_modules.append(module)
                
            except Exception as e:
                label.config(text="Hata", foreground="#e74c3c")
                self.missing_modules.append(module)
                self.log(f"Modül kontrol hatası ({module}): {str(e)}")
        
        # Düğmeleri güncelle
        if self.missing_modules:
            self.status_label.config(text=f"Eksik bağımlılıklar bulundu: {', '.join(self.missing_modules)}")
            self.install_button["state"] = "normal"
            self.log("Eksik bağımlılıklar tespit edildi. 'Bağımlılıkları Yükle' düğmesine tıklayın.")
        else:
            self.status_label.config(text="Tüm bağımlılıklar kurulu. Oyun başlatılmaya hazır!")
            self.start_button["state"] = "normal"
            self.log("Sistem kontrolü tamamlandı. Tüm bağımlılıklar kurulu.")
        
        # Oyun dosyasının varlığını kontrol et
        if not os.path.exists("main.py") and not os.path.exists("src/main.py"):
            self.log("HATA: main.py bulunamadı!")
            self.status_label.config(text="main.py bulunamadı! Lütfen oyun dosyalarını kontrol edin.")
            self.start_button["state"] = "disabled"
    
    def install_dependencies(self):
        """
        Eksik bağımlılıkları yükler.
        """
        self.install_button["state"] = "disabled"
        self.log("Eksik bağımlılıklar yükleniyor...")
        
        def install_thread():
            success = True
            for module in self.missing_modules:
                try:
                    pkg_name = "pillow" if module == "pillow" else module
                    self.log(f"Yükleniyor: {pkg_name}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
                    self.log(f"{pkg_name} başarıyla yüklendi.")
                except subprocess.CalledProcessError as e:
                    self.log(f"HATA: {pkg_name} yüklenirken sorun oluştu. Hata kodu: {e.returncode}")
                    success = False
            
            # GUI güncellemesi
            self.root.after(0, lambda: self._after_install(success))
        
        # Ayrı bir iş parçacığında yükleme işlemini başlat
        threading.Thread(target=install_thread, daemon=True).start()
    
    def _after_install(self, success):
        """
        Yükleme işlemi tamamlandıktan sonra çağrılır.
        """
        if success:
            self.log("Tüm bağımlılıklar başarıyla yüklendi.")
            self.status_label.config(text="Bağımlılıklar yüklendi. Oyun başlatılmaya hazır!")
            self.start_button["state"] = "normal"
        else:
            self.log("Bazı bağımlılıklar yüklenemedi. Lütfen manuel olarak yüklemeyi deneyin.")
            self.status_label.config(text="Bağımlılık yükleme hatası! Lütfen manuel olarak yükleyin.")
            self.install_button["state"] = "normal"
        
        # Bağımlılık durumunu tekrar kontrol et
        self.check_dependencies()
    
    def start_game(self):
        """
        Oyunu başlatır.
        """
        self.log("Oyun başlatılıyor...")
        self.status_label.config(text="Oyun başlatılıyor...")
        self.start_button["state"] = "disabled"
        
        def game_thread():
            try:
                # Varlıkların var olduğundan emin ol
                assets_path = Path.cwd() / "assets"
                if not assets_path.exists() or not any(assets_path.iterdir()):
                    self.log("Varlıklar bulunamadı. Varlıklar oluşturuluyor...")
                    # Varlık oluşturma işlemi (Python modülünün mevcut olduğunu varsayar)
                    try:
                        import src.uyum_vadisi_assets
                        src.uyum_vadisi_assets.main()
                    except ImportError:
                        self.log("uyum_vadisi_assets modülü bulunamadı")
                    self.log("Varlıklar başarıyla oluşturuldu.")
                
                # Komut satırı argümanları oluştur
                cmd_args = ["--from-launcher"]
                
                # Tam ekran ayarı
                if self.settings.get("fullscreen", False):
                    cmd_args.append("--fullscreen")
                
                # Ses seviyesi ayarı
                if "sound_volume" in self.settings:
                    cmd_args.append(f"--sound-volume={self.settings['sound_volume']}")
                
                if "music_volume" in self.settings:
                    cmd_args.append(f"--music-volume={self.settings['music_volume']}")
                
                # Oyun başlatma süreci
                if os.path.exists("src/main.py"):
                    self.log("src/main.py kullanılıyor...")
                    # src dizinine geçerek relatif importları düzelt
                    process = subprocess.Popen([sys.executable, "-m", "main"] + cmd_args, 
                                              cwd=os.path.join(os.getcwd(), "src"),
                                              env=dict(os.environ, PYTHONPATH=os.getcwd()))
                elif os.path.exists("main.py"):
                    self.log("main.py kullanılıyor...")
                    process = subprocess.Popen([sys.executable, "main.py"] + cmd_args)
                else:
                    raise FileNotFoundError("Ana oyun dosyası (main.py) bulunamadı")
                
                self.log("Oyun sürecini başlattı. Çalışıyor...")
                
                # Oyun sürecini bekle
                process.wait()
                
                # GUI güncellemesi
                return_code = process.returncode
                self.root.after(0, lambda: self._after_game(return_code))
                
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self._game_error(error_msg))
        
        # Ayrı bir iş parçacığında oyunu başlat
        threading.Thread(target=game_thread, daemon=True).start()
    
    def _after_game(self, return_code):
        """
        Oyun kapatıldıktan sonra çağrılır.
        """
        if return_code == 0:
            self.log("Oyun normal şekilde kapatıldı.")
        else:
            self.log(f"Oyun bir hata ile kapatıldı. Çıkış kodu: {return_code}")
        
        self.status_label.config(text="Oyun kapatıldı. Tekrar başlatılmaya hazır.")
        self.start_button["state"] = "normal"
    
    def _game_error(self, error_msg):
        """
        Oyun başlatma hatası durumunda çağrılır.
        """
        self.log(f"HATA: Oyun başlatılırken bir sorun oluştu: {error_msg}")
        messagebox.showerror("Başlatma Hatası", f"Oyun başlatılırken bir hata oluştu:\n\n{error_msg}")
        self.status_label.config(text="Oyun başlatılamadı!")
        self.start_button["state"] = "normal"
    
    def load_settings(self):
        """
        Ayarları yükler.
        
        Returns:
            dict: Ayarlar sözlüğü
        """
        settings_path = Path.cwd() / "settings.json"
        default_settings = {
            "fullscreen": False,
            "sound_volume": 50,
            "music_volume": 50,
            "graphics_quality": "Orta"
        }
        
        if settings_path.exists():
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    # Varsayılan ayarlarla birleştir
                    for key, value in default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
            except Exception as e:
                print(f"Ayarlar yüklenirken hata: {e}")
                return default_settings
        else:
            return default_settings
    
    def save_settings(self, settings):
        """
        Ayarları kaydeder.
        
        Args:
            settings (dict): Ayarlar sözlüğü
        """
        settings_path = Path.cwd() / "settings.json"
        try:
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            self.settings = settings
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilirken bir hata oluştu:\n\n{str(e)}")
    
    def open_settings(self):
        """
        Ayarlar penceresini açar.
        """
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Erdem Dünyası - Ayarlar")
        settings_window.geometry("500x400")
        settings_window.minsize(400, 300)
        settings_window.grab_set()  # Ana pencereyi kilitler
        
        # Stil ve renkler
        settings_window.configure(bg="#2c3e50")
        
        # Ana çerçeve
        main_frame = ttk.Frame(settings_window)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="Oyun Ayarları", style="Subheader.TLabel")
        title_label.pack(pady=10)
        
        # Ayarlar çerçevesi
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill="both", expand=True, pady=10)
        
        # Ses ayarı
        sound_frame = ttk.Frame(settings_frame)
        sound_frame.pack(fill="x", pady=5)
        
        sound_label = ttk.Label(sound_frame, text="Ses Seviyesi:", width=15, anchor="e")
        sound_label.pack(side="left", padx=5)
        
        sound_var = tk.IntVar(value=self.settings.get("sound_volume", 50))
        sound_scale = ttk.Scale(sound_frame, from_=0, to=100, variable=sound_var, orient="horizontal")
        sound_scale.pack(side="left", fill="x", expand=True, padx=5)
        
        sound_value = ttk.Label(sound_frame, text=f"{sound_var.get()}%", width=5)
        sound_value.pack(side="left", padx=5)
        
        # Ses değeri değiştiğinde etiketi güncelle
        def update_sound_label(*args):
            sound_value.config(text=f"{sound_var.get()}%")
        
        sound_var.trace_add("write", update_sound_label)
        
        # Müzik ayarı
        music_frame = ttk.Frame(settings_frame)
        music_frame.pack(fill="x", pady=5)
        
        music_label = ttk.Label(music_frame, text="Müzik Seviyesi:", width=15, anchor="e")
        music_label.pack(side="left", padx=5)
        
        music_var = tk.IntVar(value=self.settings.get("music_volume", 50))
        music_scale = ttk.Scale(music_frame, from_=0, to=100, variable=music_var, orient="horizontal")
        music_scale.pack(side="left", fill="x", expand=True, padx=5)
        
        music_value = ttk.Label(music_frame, text=f"{music_var.get()}%", width=5)
        music_value.pack(side="left", padx=5)
        
        # Müzik değeri değiştiğinde etiketi güncelle
        def update_music_label(*args):
            music_value.config(text=f"{music_var.get()}%")
        
        music_var.trace_add("write", update_music_label)
        
        # Grafik kalitesi ayarı
        graphics_frame = ttk.Frame(settings_frame)
        graphics_frame.pack(fill="x", pady=5)
        
        graphics_label = ttk.Label(graphics_frame, text="Grafik Kalitesi:", width=15, anchor="e")
        graphics_label.pack(side="left", padx=5)
        
        graphics_var = tk.StringVar(value=self.settings.get("graphics_quality", "Orta"))
        graphics_combo = ttk.Combobox(graphics_frame, textvariable=graphics_var, values=["Düşük", "Orta", "Yüksek"], state="readonly")
        graphics_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Tam ekran ayarı
        fullscreen_frame = ttk.Frame(settings_frame)
        fullscreen_frame.pack(fill="x", pady=5)
        
        fullscreen_var = tk.BooleanVar(value=self.settings.get("fullscreen", False))
        fullscreen_check = ttk.Checkbutton(fullscreen_frame, text="Tam Ekran", variable=fullscreen_var)
        fullscreen_check.pack(side="left", padx=20)
        
        # Dil seçimi
        language_frame = ttk.Frame(settings_frame)
        language_frame.pack(fill="x", pady=5)
        
        language_label = ttk.Label(language_frame, text="Dil:", width=15, anchor="e")
        language_label.pack(side="left", padx=5)
        
        language_var = tk.StringVar(value=self.settings.get("language", "Türkçe"))
        language_combo = ttk.Combobox(language_frame, textvariable=language_var, values=["Türkçe", "English"], state="readonly")
        language_combo.pack(side="left", fill="x", expand=True, padx=5)
        
        # Bilgi metni
        info_label = ttk.Label(settings_frame, text="Not: Bazı ayarlar oyun içinde etkin olacaktır.", style="Info.TLabel")
        info_label.pack(pady=10)
        
        # Düğmeler çerçevesi
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        # Kaydet düğmesi
        def save():
            new_settings = {
                "sound_volume": sound_var.get(),
                "music_volume": music_var.get(),
                "graphics_quality": graphics_var.get(),
                "fullscreen": fullscreen_var.get(),
                "language": language_var.get()
            }
            self.save_settings(new_settings)
            settings_window.destroy()
            self.log("Ayarlar kaydedildi.")
        
        save_button = ttk.Button(button_frame, text="Kaydet", command=save)
        save_button.pack(side="right", padx=5)
        
        # İptal düğmesi
        cancel_button = ttk.Button(button_frame, text="İptal", command=settings_window.destroy)
        cancel_button.pack(side="right", padx=5)
        
        # Varsayılan ayarlar düğmesi
        def reset_defaults():
            sound_var.set(50)
            music_var.set(50)
            graphics_var.set("Orta")
            fullscreen_var.set(False)
            language_var.set("Türkçe")
        
        defaults_button = ttk.Button(button_frame, text="Varsayılanlar", command=reset_defaults)
        defaults_button.pack(side="left", padx=5)

    def open_help(self):
        """
        Yardım penceresini açar.
        """
        help_window = tk.Toplevel(self.root)
        help_window.title("Erdem Dünyası - Yardım")
        help_window.geometry("600x500")
        help_window.minsize(500, 400)
        help_window.grab_set()  # Ana pencereyi kilitler
        
        # Stil ve renkler
        help_window.configure(bg="#2c3e50")
        
        # Ana çerçeve
        main_frame = ttk.Frame(help_window)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="Erdem Dünyası - Kullanım Kılavuzu", style="Subheader.TLabel")
        title_label.pack(pady=10)
        
        # İçerik çerçevesi (kaydırılabilir)
        canvas = tk.Canvas(main_frame, bg="#34495e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        content_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Yardım içeriği
        sections = [
            {
                "title": "Başlatıcı Kullanımı",
                "content": """
Erdem Dünyası başlatıcısı, oyunu başlatmadan önce:
- Gerekli bağımlılıkların yüklü olup olmadığını kontrol eder
- Eksik bağımlılıkları yüklemenizi sağlar
- Oyun ayarlarını yapılandırmanızı sağlar

İşlem Günlüğü bölümünden yapılan işlemleri takip edebilirsiniz.
                """
            },
            {
                "title": "Oyun Kontrolleri",
                "content": """
W, A, S, D: Hareket etme
E: Etkileşim (NPC'lerle konuşma, nesneleri kullanma)
I: Envanter
Q: Görev günlüğü
1-4: Ruh hayvanı yetenekleri
Space: Ruh hayvanı dönüşümü
R: Normal saldırı
Z: En yakın düşmanı hedefleme
B: Banka sistemini açma

Fare Kontrolleri:
- Sol Tık: NPC veya düşman seçme
- Sağ Tık: Hedefe hareket etme
- Sürükle-Bırak: Yetenek çubuğunda yetenekleri düzenleme
                """
            },
            {
                "title": "Ruh Hayvanı Sistemi",
                "content": """
Erdem Dünyası'nda dört farklı ruh hayvanı seçeneği bulunur:
- Kurt: Hızlı ve çevik, grup halinde çalışmada ustadır.
- Kartal: Keskin görüşlü ve özgür, uzaktaki tehlikeleri görebilir.
- Ayı: Güçlü ve dayanıklı, doğanın zorluklarına direnebilir.
- Tilki: Kurnaz ve zeki, yeni yollar keşfetmede ustadır.

Ruh hayvanınızla olan bağınız güçlendikçe yeni yetenekler kazanırsınız.
                """
            },
            {
                "title": "Banka Sistemi",
                "content": """
Banka sistemi, tüm karakterleriniz arasında eşya ve altın paylaşımı yapabilmenizi sağlar.
Banka noktalarında 'B' tuşuna basarak banka arayüzüne erişebilirsiniz.
                """
            },
            {
                "title": "Sorun Giderme",
                "content": """
Oyun başlatılamıyorsa:
1. Python'un doğru bir şekilde kurulu olduğundan emin olun
2. Başlatıcıdaki "Bağımlılıkları Yükle" düğmesini kullanarak eksik kütüphaneleri yükleyin
3. Hala sorun yaşıyorsanız, konsoldan manuel olarak şu komutu çalıştırın:
   pip install -r requirements.txt
4. Ekran hatası yaşıyorsanız, ekran çözünürlüğünüzün en az 800x600 olduğundan emin olun
                """
            }
        ]
        
        # Bölümleri ekle
        for i, section in enumerate(sections):
            # Bölüm başlığı
            section_frame = ttk.Frame(content_frame)
            section_frame.pack(fill="x", pady=10)
            
            section_title = ttk.Label(section_frame, text=section["title"], font=("Helvetica", 12, "bold"),
                                     foreground="#ecf0f1", background="#2c3e50")
            section_title.pack(anchor="w")
            
            # Bölüm içeriği
            content_text = tk.Text(content_frame, wrap="word", height=6, width=60, bg="#34495e", fg="#ecf0f1")
            content_text.insert("1.0", section["content"].strip())
            content_text.config(state="disabled")
            content_text.pack(fill="x", padx=10)
            
            # Ayırıcı çizgi
            if i < len(sections) - 1:
                separator = ttk.Separator(content_frame, orient="horizontal")
                separator.pack(fill="x", padx=10, pady=10)
        
        # Kapat düğmesi
        close_button = ttk.Button(main_frame, text="Kapat", command=help_window.destroy)
        close_button.pack(pady=10)

def main():
    """
    Ana uygulama fonksiyonu.
    """
    root = tk.Tk()
    app = ErdemDunyasiLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main() 