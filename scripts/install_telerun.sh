#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   telerun_url="https://raw.githubusercontent.com/SophiaSun18/student_software/refs/heads/main/telerun/submit.py"
   echo "Installing telerun"
   mkdir -p /opt/spe
   curl -O --output-dir /opt/spe $telerun_url
   chmod +x /opt/spe/submit.py
   ln -sf /opt/spe/submit.py /usr/bin/telerun
fi