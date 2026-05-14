#!/bin/bash
set -e
echo "Generating ArkheOS ISO Baremetal..."
# Using the existing generate_iso.sh as a base
bash arkhe-sync/scripts/generate_iso.sh
echo "ArkheOS ISO Baremetal ready."
