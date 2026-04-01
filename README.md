Pocket Runner: User Guide & Installation

What is Pocket Runner?

Pocket Runner is an app that turns your iPhone into a motion tracker for PC VR and desktop gaming. By running or jogging in place in the real world, you move your character forward in your game!
To make this work, you need two things:
The Pocket Runner app on your iPhone.
The Pocket Runner PC Server running on your Windows computer.
💻 Windows Installation Instructions

Step 1: Download and Run the PC Server

Download the PocketRunnerServer.exe file to your Windows PC.
Double-click PocketRunnerServer.exe to launch it.
A console window will open showing that the server is running and broadcasting your PC's connection info.
Step 2: Allow Network Permissions (Important!)

When you run the server for the first time, Windows Firewall may pop up asking for network permissions.
You must click "Allow" so that your iPhone can find and talk to your PC over your local Wi-Fi network.
Step 3: (Highly Recommended for VR) Install Virtual Gamepad Drivers

By default, Pocket Runner simulates pressing the W/A/S/D keys on your keyboard to move you forward.
If you want smooth, analog joystick movement (which is highly recommended for SteamVR and most modern games), you should install the ViGEmBus driver. Once installed, Pocket Runner will automatically detect it and output virtual Xbox controller movements instead of keyboard presses!
Download the driver here: ViGEmBus Releases (Download and run the latest installer).
📱 How to Use the App

Make sure your PC and your iPhone are connected to the same Wi-Fi network.
Launch the PocketRunnerServer.exe on your PC and leave the window open.
Open the Pocket Runner app on your iPhone.
Your PC's name should automatically appear in the app. Tap your PC name to connect.
Put your phone in your pocket (or strap it to your leg/waist).
Jog in place to start moving in your game!

Running from Python Source (Advanced / Developer Setup)

If you prefer to run the Pocket Runner server directly from the source code instead of using the pre-built .exe, follow these steps:
Step 1: Install Python

You will need Python installed on your Windows PC.
Go to the official Python website (python.org) and download the latest installer (Python 3.8 or newer is recommended).
Run the installer.
CRITICAL: Before clicking "Install Now" at the bottom of the window, make sure to check the box that says "Add python.exe to PATH". If you miss this, the commands in the next steps won't work!
Step 2: Download the Server Script

Download the windows_companion.py file to a folder on your computer (for example, inside a new folder on your Desktop called "PocketRunner").
Step 3: Install Required Libraries

The server relies on a few Python libraries to handle network connections, virtual controllers, and keyboard inputs.
Open the Windows Start Menu, type cmd, and press Enter to open the Command Prompt.
Run the following command exactly as written and press Enter:
Copy
pip install websockets pynput zeroconf vgamepad
Wait for the installation to finish successfully.
Step 4: Run the Server

In your Command Prompt, navigate to the folder where you saved the script. (For example, if it's on your desktop, type cd Desktop\PocketRunner).
Run the script with this command:
Copy
python windows_companion.py
The server will start up and begin broadcasting your PC's connection info so your iPhone can find it.
Note: The first time you run this, Windows Firewall may pop up. Make sure to click Allow so your phone can connect over your local Wi-Fi!
Step 5: (Highly Recommended for VR) Install Virtual Gamepad Drivers

By default, the script simulates pressing the W/A/S/D keys on your keyboard. For smooth, analog joystick movement in SteamVR and modern games, you need to install the ViGEmBus driver.
Download the driver here: ViGEmBus Releases (Download and run the latest installer).
Once installed, the Python script will automatically detect it and output virtual Xbox controller movements instead of keyboard presses!
How does that look? Should be everything they need to get it running from scratch!
