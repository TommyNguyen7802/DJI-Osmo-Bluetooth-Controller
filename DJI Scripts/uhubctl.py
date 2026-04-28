import subprocess

HUB_LOCATION_1 = 2
HUB_LOCATION_2 = 4


def disable_hub():
    """Disable USB hub at given location using uhubctl."""
    cmd1 = ["uhubctl", "-l", HUB_LOCATION_1, "-a", "0"]
    cmd2 = ["uhubctl", "-l", HUB_LOCATION_2, "-a", "0"]
    # print("Running:", " ".join(cmd))
    try:
        output1 = subprocess.run(
            cmd1, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        output2 = subprocess.run(
            cmd2, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        # print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error disabling hub at {HUB_LOCATION_1} or {HUB_LOCATION_2}:", e)


def enable_hub():
    """Enable USB hub at given location using uhubctl."""
    cmd1 = ["uhubctl", "-l", HUB_LOCATION_1, "-a", "1"]
    cmd2 = ["uhubctl", "-l", HUB_LOCATION_2, "-a", "1"]
    # print("Running:", " ".join(cmd))
    try:
        output1 = subprocess.run(
            cmd1, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        output2 = subprocess.run(
            cmd2, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error enabling hub at {HUB_LOCATION_1} or {HUB_LOCATION_2}:", e)
