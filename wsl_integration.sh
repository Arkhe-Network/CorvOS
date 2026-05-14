#!/bin/bash
# Integrate ArkheOS with WSL
echo "Integrating ArkheOS with WSL..."

# Install basic CLI tools in the WSL distro
mkdir -p /usr/local/bin
cp bin/arkh/arkh.py /usr/local/bin/arkh
chmod +x /usr/local/bin/arkh

# Add an entry to WSL wsl.conf to automatically start arkhe components
mkdir -p /etc/wsl.conf.d
cat << 'WSL_CONF' > /etc/wsl.conf
[boot]
command = "arkh status > /var/log/arkh_wsl_boot.log 2>&1"
WSL_CONF

echo "WSL Integration complete."
