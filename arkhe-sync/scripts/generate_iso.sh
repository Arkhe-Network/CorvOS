#!/bin/bash
# generate_iso.sh - Build the ArkheOS ISO

set -e

ISO_ROOT="iso_root"
BOOT_DIR="$ISO_ROOT/boot"
ISOLINUX_DIR="$BOOT_DIR/isolinux"

echo "🜏 Preparing ISO structure..."
mkdir -p "$ISOLINUX_DIR" "$ISO_ROOT/bin" "$ISO_ROOT/lib"

# Copy binaries
cp corvos_kernel "$ISO_ROOT/bin/"
cp arkhe-sync/arkhe-daemon/target/release/arkhe-daemon "$ISO_ROOT/bin/"
cp arkhe-sync/arkhe-ebpf/target/release/arkhe-ebpf "$ISO_ROOT/bin/"

# Copy libraries (assuming x86_64)
cp /lib/x86_64-linux-gnu/libncurses.so.6 "$ISO_ROOT/lib/"
cp /lib/x86_64-linux-gnu/libm.so.6 "$ISO_ROOT/lib/"
cp /lib/x86_64-linux-gnu/libc.so.6 "$ISO_ROOT/lib/"
cp /lib/x86_64-linux-gnu/libtinfo.so.6 "$ISO_ROOT/lib/"
cp /lib64/ld-linux-x86-64.so.2 "$ISO_ROOT/lib/"

# Copy bootloader files
cp /usr/lib/ISOLINUX/isolinux.bin "$ISOLINUX_DIR/"
cp /usr/lib/syslinux/modules/bios/ldlinux.c32 "$ISOLINUX_DIR/" 2>/dev/null || true

# Generate initramfs
echo "Generating initramfs..."
(cd "$ISO_ROOT" && find . | cpio -o -H newc | gzip) > "$BOOT_DIR/initrd.img"

# Use existing kernel from system for simulation or external source
if [ -f "/boot/vmlinuz-$(uname -r)" ]; then
    cp "/boot/vmlinuz-$(uname -r)" "$BOOT_DIR/vmlinuz"
else
    # Fallback for CI/sandbox environments
    touch "$BOOT_DIR/vmlinuz"
fi

# Generate ISO
echo "Building ISO image..."
xorriso -as mkisofs -o ArkheOS_Grace_v2.iso \
    -b boot/isolinux/isolinux.bin -c boot/isolinux/boot.cat \
    -no-emul-boot -boot-load-size 4 -boot-info-table \
    "$ISO_ROOT"

echo "🜏 ISO generated: ArkheOS_Grace_v2.iso"
