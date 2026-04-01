# 🏃 Pocket Runner

> Turn your iPhone into a motion tracker for PC VR and desktop gaming — jog in place in the real world to move your character forward in-game.

---

## How It Works

Pocket Runner has two components that work together over your local Wi-Fi network:

| Component | What It Does |
|---|---|
| **Pocket Runner** (iPhone app) | Tracks your motion using the phone's sensors |
| **Pocket Runner PC Server** (Windows) | Receives motion data and translates it into in-game movement |

---

## 💻 Windows Installation

### Option 1 — Pre-built Executable (Recommended)

**Step 1: Download & launch the server**

Download `PocketRunnerServer.exe` and double-click it to run. A console window will open confirming the server is running and broadcasting your PC's connection info.

**Step 2: Allow network permissions**

On first launch, Windows Firewall will ask for network access. **Click "Allow"** — this is required for your iPhone to communicate with your PC over Wi-Fi.

**Step 3: Install virtual gamepad drivers *(highly recommended for VR)***

By default, Pocket Runner simulates `W`/`A`/`S`/`D` keypresses. For smooth, analog joystick movement (strongly recommended for SteamVR and most modern games), install the **ViGEmBus** driver:

👉 [Download ViGEmBus](https://github.com/nefarius/ViGEmBus/releases) — run the latest installer.

Once installed, Pocket Runner will automatically detect it and switch to virtual Xbox controller output.

---

### Option 2 — Run from Python Source *(Advanced / Developer)*

**Step 1: Install Python**

Download and install **Python 3.8+** from [python.org](https://python.org).

> ⚠️ **Important:** During installation, check **"Add python.exe to PATH"** before clicking Install. Missing this will cause the commands below to fail.

**Step 2: Download the server script**

Download `windows_companion.py` into a folder on your PC (e.g., `Desktop\PocketRunner`).

**Step 3: Install required libraries**

Open **Command Prompt** and run:

```bash
pip install websockets pynput zeroconf vgamepad
```

**Step 4: Start the server**

Navigate to the folder containing the script and run it:

```bash
cd Desktop\PocketRunner
python windows_companion.py
```

The server will start and broadcast your PC's connection info for your iPhone to discover.

> ⚠️ **First run:** Windows Firewall may prompt for network access. Click **Allow** so your phone can connect.

**Step 5: Install virtual gamepad drivers *(highly recommended for VR)***

Same as above — install [ViGEmBus](https://github.com/nefarius/ViGEmBus/releases) for analog joystick output instead of keyboard simulation.

---

## 📱 Using the App

1. Connect both your PC and iPhone to the **same Wi-Fi network**
2. Launch `PocketRunnerServer.exe` (or `windows_companion.py`) on your PC and leave it running
3. Open the **Pocket Runner** app on your iPhone
4. Your PC's name will appear automatically — tap it to connect
5. Put your phone in your pocket (or strap it to your leg or waist)
6. **Jog in place** to move forward in your game!

---

## 📋 Requirements

- Windows PC
- iPhone with the Pocket Runner app installed
- Both devices on the same local Wi-Fi network
- *(Optional but recommended)* [ViGEmBus](https://github.com/nefarius/ViGEmBus/releases) for analog controller support
