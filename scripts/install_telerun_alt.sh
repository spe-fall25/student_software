#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   telerun_url="https://raw.githubusercontent.com/CSE491-spring25/student_software/main/telerun/submit_alt.py"
   echo "Installing telerun"
   mkdir -p /opt/6106
   curl -O --output-dir /opt/6106 $telerun_url
   chmod +x /opt/6106/submit_alt.py
   ln -sf /opt/6106/submit_alt.py /usr/bin/telerun-alt
fi
