import subprocess

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error running command: {result.stderr}")
    return result.stdout.strip()

def start_adb_server():
    """Start the ADB server."""
    print("Starting ADB server...")
    output = run_command("adb start-server")
    print(output)

def connect_device(address):
    """Connect to a device via ADB."""
    print(f"Connecting to device at {address}...")
    output = run_command(f"adb connect {address}")
    print(output)

def iniciarADB(adress0, adress1):
    start_adb_server()

    connect_device(f'{adress0}')
    connect_device(f'{adress1}')