# Connect the Raspberry Pi 5 through SSH over direct Ethernet on Ubuntu

0. Begin with Pi disconnected
1. Go to "Network Connections" --> "IPv4 Settings"
2. Change "Method" setting to "Shared to other computers"
    - This sets the PC as the DHCP server
3. Connect Pi to PC over Ethernet
3. if hostname is `raspberrypi` (default), enter `ssh {username}@raspberrypi.local`
4. Enter credentials

- **If the PC has internet, the Pi should have network+internet access**