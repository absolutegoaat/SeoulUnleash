import os
import platform
import subprocess
import uuid

def check_vm():
    indicators = []

    # Check system manufacturer and product name (common in VMs)
    if platform.system() == "Windows":
        try:
            output = subprocess.check_output(
                ["wmic", "computersystem", "get", "manufacturer,model"],
                universal_newlines=True
            )
            if "VMware" in output or "VirtualBox" in output or "KVM" in output:
                indicators.append("Manufacturer/Model indicates VM")
        except Exception:
            pass
    else:
        try:
            output = subprocess.check_output(
                ["dmesg"], stderr=subprocess.DEVNULL, universal_newlines=True
            )
            if "VirtualBox" in output or "VMware" in output or "hypervisor" in output:
                indicators.append("dmesg reports hypervisor")
        except Exception:
            pass

    # Check MAC address prefixes (VMware, VirtualBox, etc.)
    try:
        mac = uuid.getnode()
        mac_prefix = mac >> 40
        vm_mac_prefixes = {
            0x00: "VirtualBox",
            0x08: "VMware",
            0x0A: "Parallels"
        }
        if mac_prefix in vm_mac_prefixes:
            indicators.append(f"MAC address suggests {vm_mac_prefixes[mac_prefix]}")
    except Exception:
        pass

    return indicators

if __name__ == "__main__":
    print('module cannot be ran directly')