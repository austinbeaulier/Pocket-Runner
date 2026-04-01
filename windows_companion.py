#!/usr/bin/env python3
"""
PocketRunner Companion — Windows
"""

import sys
import time

try:
    import asyncio
    import json
    import socket
    import logging
    import threading

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    from zeroconf import ServiceInfo, Zeroconf
    import websockets
    from pynput.keyboard import Controller, Key

    # Make vgamepad completely optional
    VGP_AVAILABLE = False
    try:
        import vgamepad as vg
        VGP_AVAILABLE = True
    except Exception as e:
        print(f"\n[i] Virtual Gamepad library not loaded (running in keyboard-only mode).")

    keyboard = Controller()

    KEY_MAP = {
        "w": "w", "a": "a", "s": "s", "d": "d",
        "space": Key.space, "shift": Key.shift,
        "e": "e", "q": "q", "r": "r", "f": "f",
    }

    held_keys = set()
    gamepad = None
    axis_x = 0.0
    axis_y = 0.0
    zeroconf_instance = None
    zeroconf_info = None

    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def register_zeroconf_sync(port, ip_address):
        """Runs zeroconf in a separate thread so it doesn't block asyncio"""
        global zeroconf_instance, zeroconf_info
        hostname = socket.gethostname()
        zeroconf_info = ServiceInfo(
            "_pocketrunner._tcp.local.",
            f"{hostname}._pocketrunner._tcp.local.",
            addresses=[socket.inet_aton(ip_address)],
            port=port,
            properties={'version': '1.0'},
            server=f"{hostname}.local.",
        )
        try:
            zeroconf_instance = Zeroconf()
            zeroconf_instance.register_service(zeroconf_info)
            print(f"  [i] Broadcasting mDNS as '{hostname}' -> Open the app to connect automatically.")
        except Exception as e:
            print(f"  [!] Failed to broadcast mDNS. You can still connect manually via IP. Error: {e}")

    def setup_zeroconf(port, ip_address):
        # Start Zeroconf in a background thread to prevent asyncio EventLoopBlocked
        t = threading.Thread(target=register_zeroconf_sync, args=(port, ip_address), daemon=True)
        t.start()

    def clamp(v, lo=-1.0, hi=1.0):
        return max(lo, min(hi, v))

    def init_gamepad():
        global gamepad
        if not VGP_AVAILABLE:
            print("\n  [!] Virtual Xbox controller output disabled.")
            print("      For smooth SteamVR locomotion, you need the ViGEmBus driver.")
            print("      Download: https://github.com/nefarius/ViGEmBus/releases\n")
            return
        try:
            gamepad = vg.VX360Gamepad()
            print("  [i] Virtual Xbox gamepad enabled!")
        except Exception as e:
            print(f"  [!] ViGEmBus driver not installed. Keyboard-only mode active.")

    def update_gamepad_axis():
        if not gamepad: return
        try:
            gamepad.left_joystick_float(x_value_float=clamp(axis_x), y_value_float=clamp(axis_y))
            gamepad.update()
        except Exception: pass

    def set_axis_for_action(action, down):
        global axis_x, axis_y
        if action == "w": axis_y = 1.0 if down else (0.0 if "s" not in held_keys else -1.0)
        elif action == "s": axis_y = -1.0 if down else (0.0 if "w" not in held_keys else 1.0)
        elif action == "a": axis_x = -1.0 if down else (0.0 if "d" not in held_keys else 1.0)
        elif action == "d": axis_x = 1.0 if down else (0.0 if "a" not in held_keys else -1.0)

        if action == "shift" and gamepad:
            if down: gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
            else: gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        update_gamepad_axis()

    def press_key(key, down: bool = True):
        try:
            if down: keyboard.press(key)
            else: keyboard.release(key)
        except Exception: pass

    def handle_message(data: dict):
        action = data.get("action", "")
        state = data.get("state", "")
        key = KEY_MAP.get(action)
        if key is None: return

        if state == "down" and action not in held_keys:
            press_key(key, down=True)
            held_keys.add(action)
            set_axis_for_action(action, down=True)
            print(f"  [DOWN] {action.upper()}")
        elif state == "up" and action in held_keys:
            press_key(key, down=False)
            held_keys.discard(action)
            set_axis_for_action(action, down=False)
            print(f"  [ UP ] {action.upper()}")

    def release_all():
        global axis_x, axis_y
        for action in list(held_keys):
            if key := KEY_MAP.get(action): press_key(key, down=False)
        held_keys.clear()
        axis_x, axis_y = 0.0, 0.0
        if gamepad:
            try:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
                gamepad.left_joystick_float(0.0, 0.0)
                gamepad.update()
            except Exception: pass

    async def handler(websocket):
        client_ip = websocket.remote_address[0] if websocket.remote_address else "unknown"
        print(f"\n[+] iPhone connected from {client_ip}")
        try:
            async for message in websocket:
                try: handle_message(json.loads(message))
                except json.JSONDecodeError: pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            release_all()
            print(f"\n[-] iPhone disconnected ({client_ip})")

    async def main():
        host, port = "0.0.0.0", 8765
        local_ip = get_local_ip()
        
        print("=" * 56)
        print("  PocketRunner Windows Server")
        print("=" * 56)
        print(f"\n  Listening on ws://{local_ip}:{port}")
        
        init_gamepad()
        setup_zeroconf(port, local_ip)
        
        server = await websockets.serve(handler, host, port)
        try:
            await asyncio.Future()  # run forever
        finally:
            if zeroconf_instance and zeroconf_info:
                zeroconf_instance.unregister_service(zeroconf_info)
                zeroconf_instance.close()

    if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\nExiting...")
            
except Exception as global_err:
    print(f"\nFATAL CRASH: {global_err}")
    import traceback
    traceback.print_exc()
    print("\nWaiting 30 seconds before closing...")
    time.sleep(30)
