#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
   mkdir -p /opt/spe

   echo "Creating symlink update-clang-spe"
   cp scripts/install_opencilk.sh /opt/spe/update-clang-spe.sh
   ln -sf /opt/spe/update-clang-spe.sh /usr/bin/update-clang-spe

   echo "Creating symlink update-telerun"
   cp scripts/install_telerun.sh /opt/spe/update-telerun.sh
   ln -sf /opt/spe/update-telerun.sh /usr/bin/update-telerun

   echo "Creating symlink authorize-telerun"
   cp scripts/authorize_telerun.sh /opt/spe/authorize-telerun.sh
   ln -sf /opt/spe/authorize-telerun.sh /usr/bin/authorize-telerun
fi
