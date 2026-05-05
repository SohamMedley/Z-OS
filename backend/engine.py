import subprocess
import pyautogui
import time
import urllib.parse
import os

pyautogui.FAILSAFE = True

def navigate(url: str):
    if not url.startswith("http"):
        url = "https://www." + url
    
    # MASTER FIX: ALWAYS open a fresh New Tab first.
    # This guarantees the Z-OS screen is never overwritten.
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1.5) # Wait for tab to fully render
    
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    
    # The typing effect
    pyautogui.write(url, interval=0.03)
    time.sleep(0.2)
    pyautogui.press('space')
    pyautogui.press('backspace')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(2) 
    return f"Uplink established to: {url}"

def search_web(query: str):
    # MASTER FIX: ALWAYS open a fresh New Tab first.
    pyautogui.hotkey('ctrl', 't')
    time.sleep(1.5)
    
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"
    
    pyautogui.write(search_url, interval=0.02)
    time.sleep(0.2)
    pyautogui.press('space')
    pyautogui.press('backspace')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(2)
    return f"Executed secure global search for: {query}"

def type_text(text: str):
    pyautogui.write(text, interval=0.02)
    pyautogui.press('enter')
    return "Injected text payload."

def press_key(key: str):
    pyautogui.press(key)
    return f"Triggered hardware key: {key}"

def desktop_mode():
    pyautogui.hotkey('win', 'd')
    return "Cleared workspace. Desktop mode engaged."

def open_app(app_name: str):
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write(app_name)
    time.sleep(0.8)
    pyautogui.press('enter')
    time.sleep(2)
    return f"Launched native process: {app_name}"

def run_ps_command(command: str):
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    if result.returncode == 0:
        return f"Shell executed: {result.stdout.strip()[:100]}..." 
    else:
        raise Exception(f"Shell Error: {result.stderr.strip()}")

def wait(seconds: int):
    """Pauses the engine for a specific amount of time."""
    time.sleep(int(seconds))
    return f"Timer completed: Waited for {seconds} seconds."

def force_close(app_exe: str):
    """Instantly kills an application at the OS level, bypassing save prompts."""
    os.system(f"taskkill /F /IM {app_exe} /T >nul 2>&1")
    return f"Forcefully terminated {app_exe} without saving."