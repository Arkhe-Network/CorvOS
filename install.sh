#!/bin/bash
echo "Installing Arkhe Runtime..."
mkdir -p /usr/local/bin
cp bin/arkh/arkh.py /usr/local/bin/arkh
chmod +x /usr/local/bin/arkh
echo "Arkhe Runtime installed successfully. You can now use the 'arkh' command."
