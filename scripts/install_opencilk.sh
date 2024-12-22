#!/bin/bash
set -e

if [[ $EUID -ne 0 ]]; then
   sudo -E $0
else
  opencilk_url="http://6.172.scripts.mit.edu/opencilk_6106.tar.gz"
  echo "Installing OpenCilk"
  mkdir -p /opt/spe/opencilk
  rm -rf /opt/spe/opencilk/*
  curl -L $opencilk_url | tar -zxv --strip-components=1 -C /opt/spe/opencilk

  ln -sf /opt/spe/opencilk/bin/clang /usr/bin/clang-spe
fi
