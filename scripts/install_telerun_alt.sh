#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   telerun_url="https://raw.githubusercontent.com/CSE491-spring25/student_software/main/telerun/submit_alt.py"
   echo "Installing telerun"
   mkdir -p /opt/spe
   curl -O --output-dir /opt/spe $telerun_url
   chmod +x /opt/spe/submit_alt.py
   ln -sf /opt/spe/submit_alt.py /usr/bin/telerun-alt
fi
