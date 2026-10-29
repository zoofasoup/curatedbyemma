#!/usr/bin/env bash
# ==============================================================================
# CuratedByEmma 24/7 Automated VPS Setup Script
# Tested on Ubuntu 22.04 / 24.04 LTS (Rumahweb / Cloud VPS)
# ==============================================================================
set -e

echo "🚀 [1/6] Updating system packages and installing dependencies..."
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip python3-venv ufw curl

INSTALL_DIR="/opt/curatedbyemma"
REPO_URL="https://github.com/zoofasoup/curatedbyemma.git"

echo "📦 [2/6] Setting up project directory at ${INSTALL_DIR}..."
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Directory exists. Pulling latest code..."
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "Cloning repository..."
    sudo git clone "$REPO_URL" "$INSTALL_DIR"
    sudo chown -R $USER:$USER "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

echo "🐍 [3/6] Setting up Python virtual environment & Playwright..."
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "🌐 Installing Playwright Chromium and headless system libraries..."
./venv/bin/playwright install chromium
sudo ./venv/bin/playwright install-deps chromium

echo "🔒 [4/6] Checking for credentials..."
if [ ! -f "$INSTALL_DIR/threads_session.json" ]; then
    echo "⚠️ NOTICE: 'threads_session.json' not found!"
    echo "Please copy your threads_session.json from your Mac using:"
    echo "  scp /Users/macbookair/.gemini/antigravity/scratch/affiliate-engine/threads_session.json root@$(curl -s ifconfig.me):$INSTALL_DIR/"
fi

if [ ! -f "$INSTALL_DIR/.env" ]; then
    echo "⚠️ NOTICE: '.env' not found!"
    echo "Please copy your .env file or create it with your OPENROUTER_API_KEY."
fi

echo "⚙️ [5/6] Creating Systemd Service for 24/7 Dashboard & AutoPilot..."
SERVICE_FILE="/etc/systemd/system/curatedbyemma.service"
sudo bash -c "cat << 'EOF' > $SERVICE_FILE
[Unit]
Description=CuratedByEmma Affiliate Dashboard & AutoPilot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python dashboard_server.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable curatedbyemma
sudo systemctl restart curatedbyemma

echo "⏰ [6/6] Setting up 30-minute Crontab for Dual-Search Rotator..."
CRON_JOB="*/30 * * * * cd $INSTALL_DIR && ./venv/bin/python threads_sniffer.py --rotate >> /var/log/emma_sniffer.log 2>&1"
(crontab -l 2>/dev/null | grep -v "threads_sniffer.py"; echo "$CRON_JOB") | crontab -

echo "🛡️ Configuring UFW firewall for port 7860..."
sudo ufw allow 7860/tcp || true
sudo ufw allow OpenSSH || true

IP=$(curl -s ifconfig.me || hostname -I | awk '{print $1}')
echo ""
echo "=================================================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "Dashboard running at: http://${IP}:7860 (PIN: 2707)"
echo "Service Status: systemctl status curatedbyemma"
echo "Sniffer Logs:   tail -f /var/log/emma_sniffer.log"
echo "=================================================================="
