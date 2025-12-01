import subprocess

def disable_hub(location):
    """Disable USB hub at given location using uhubctl."""
    cmd = ["uhubctl", "-l", str(location), "-a", "0"]
    print("Running:", " ".join(cmd))
    try:
        output = subprocess.check_output(cmd, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error disabling hub {location}:", e)

def enable_hub(location):
    """Enable USB hub at given location using uhubctl."""
    cmd = ["uhubctl", "-l", str(location), "-a", "1"]
    print("Running:", " ".join(cmd))
    try:
        output = subprocess.check_output(cmd, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error enabling hub {location}:", e)