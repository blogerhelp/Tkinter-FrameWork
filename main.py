from tkinter import *
from tkinter import messagebox
import os
import json
import sys
from pathlib import Path
from PIL import Image, ImageTk
import subprocess
import time

from components.open_project import *
from components.export import *
from components.window import *


current_dir = Path(__file__).resolve().parent
target_script = current_dir / "components" / "load.py"

# run() полностью остановит выполнение текущего скрипта до закрытия main.py
result = subprocess.run([sys.executable, str(target_script)])
time.sleep(1)
if result.returncode == 1:
    print("End this Programm")
    sys.exit(0)
else:
    target_script = current_dir / "components" / "main_interface.py"
    subprocess.run([sys.executable, str(target_script)])
