#!/bin/bash

# Terminal renklerini ayarla
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}===================================="
echo -e "${CYAN}=  ERDEM DUNYASI OYUN BASLATICI   ="
echo -e "${CYAN}====================================${NC}"
echo ""

# Python kontrolü yap
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python bulunamadı!${NC}"
    echo ""
    echo "Oyunu çalıştırmak için önce Python'u kurmanız gerekiyor."
    echo "Python'u aşağıdaki yöntemlerle kurabilirsiniz:"
    echo ""
    echo -e "${YELLOW}Linux için:${NC}"
    echo "  sudo apt-get update && sudo apt-get install python3 python3-pip  # Debian/Ubuntu için"
    echo "  sudo dnf install python3 python3-pip  # Fedora için"
    echo ""
    echo -e "${YELLOW}macOS için:${NC}"
    echo "  brew install python  # Homebrew kullanıyorsanız"
    echo "  veya Python resmi web sitesinden indirin: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

# Tkinter kontrolü yap (Başlatıcı için gerekli)
if ! python3 -c "import tkinter" &> /dev/null; then
    echo -e "${RED}Tkinter bulunamadı!${NC}"
    echo ""
    echo "Başlatıcı için Tkinter gereklidir. Lütfen yükleyin:"
    echo ""
    echo -e "${YELLOW}Linux için:${NC}"
    echo "  sudo apt-get install python3-tk  # Debian/Ubuntu için"
    echo "  sudo dnf install python3-tkinter  # Fedora için"
    echo ""
    echo -e "${YELLOW}macOS için:${NC}"
    echo "  brew install python-tk  # Homebrew kullanıyorsanız"
    echo ""
    echo "Python'unuza uygun bir şekilde Tkinter'ı yükledikten sonra tekrar deneyin."
    exit 1
fi

echo -e "${GREEN}===================================="
echo -e "${GREEN}=       BAŞLATICI AÇILIYOR        ="
echo -e "${GREEN}====================================${NC}"

# Launcher'ı çalıştır
if [ -f "launcher.py" ]; then
    python3 launcher.py
else
    echo -e "${RED}Başlatıcı (launcher.py) bulunamadı!${NC}"
    echo ""
    echo "Alternatif olarak oyun doğrudan çalıştırılmaya çalışılıyor..."
    echo ""
    
    # Ana oyun dosyasını doğrudan çalıştırmayı dene
    if [ -f "main.py" ]; then
        echo -e "${GREEN}Ana oyun dosyası bulundu. Oyun başlatılıyor...${NC}"
        python3 main.py
    elif [ -f "src/main.py" ]; then
        echo -e "${GREEN}src/main.py bulundu. Oyun başlatılıyor...${NC}"
        cd src
        python3 -m main
    else
        echo -e "${RED}Oyun dosyaları bulunamadı!${NC}"
        echo "Lütfen oyun dosyalarının tam olarak yüklendiğinden emin olun."
    fi
    
    echo ""
    echo -e "${YELLOW}Devam etmek için ENTER tuşuna basın...${NC}"
    read
fi

exit 0 