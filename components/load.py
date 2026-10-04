# python -m components.load

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sys
from pathlib import Path
import json
from PIL import Image, ImageTk
import time
import threading
import subprocess
import glob
from temp import Temp


current_dir = Path(__file__).resolve().parent.parent
json_path = current_dir / "data" / "temp.json"
style_file_loader = Temp(json_path)
style_file = style_file_loader.get("loaded_json/style")
style_path = current_dir / "assets" / "styles" / f"{style_file}"
styles = Temp(style_path)


def on_loading_finished():
    """Функция, которая вызывается сразу после завершения загрузки."""
    root.quit()

    print("Data Loaded")


def start_loading():
    global updated
    updated = False

    def funexit(winname, message):
        messagebox.showerror(winname, message)
        root.quit()
        sys.exit(1)

    current_dir = Path(__file__).resolve().parent
    json_path = current_dir.parent / "data" / "main.json"

    json_manager_main = Temp(json_path)
    json_data_main = json_manager_main.get()
    if json_data_main == None:
        funexit("Error loading", f"Failed to load main.json")

    json_path = current_dir.parent / "data" / "projects.json"
    json_manager_main = Temp(json_path)
    json_data_projects = json_manager_main.get()
    if json_data_projects == None:
        funexit("Error loading", f"Failed to load projects.json")

    json_path = current_dir.parent / "data" / "temp.json"
    json_manager_temp = Temp(json_path)
    json_manager_temp.set("loaded_data", True)
    json_manager_temp.set("loaded_projects", json_data_projects)
    json_manager_temp.set("loaded_json", json_data_main)
    json_files = glob.glob("*.json", root_dir="./assets/styles")
    json_manager_temp.set("loaded_json.style_files", json_files)

    def update(i):
        global updated
        # Запускаем цикл для демонстрации прогресса
        if i <= 100:
            # Обновляем прогресс и текст
            progress["value"] = i
            percent_label.config(text=f"{i}%")

            # Просим Tkinter вызвать эту же функцию снова через 50 миллисекунд, передав i + 1
            # Окно НЕ лагает, так как между вызовами Tkinter успевает обрабатывать интерфейс
            root.after(35, update, i + 1)
        else:
            # Действие, которое должно произойти ПОСЛЕ окончания загрузки
            print("Загрузка успешно завершена!")
            time.sleep(1)
            updated = True

    def start_loading_and_wait():
        """Запускает поток и инициирует процесс ожидания."""

        # 2. Создаем и запускаем фоновый поток
        update(0)

        # 3. Запускаем периодическую проверку окончания потока
        check_thread_status()

    def check_thread_status():
        global updated
        """Каждые 100 мс проверяет, завершился ли поток."""
        if updated:
            on_loading_finished()
        else:
            # Если поток еще работает, проверяем снова через 100 миллисекунд
            root.after(100, check_thread_status)

    start_loading_and_wait()


def init_styles():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Horizontal.TProgressbar",
        troughcolor="#131313",  # Цвет незаполненной дорожки (фон)
        background="#009cda",  # Цвет заполненной линии (индикатор прогресса)
        lightcolor="#00b7ff",  # Цвет блика (делаем в тон индикатора для flat-эффекта)
        darkcolor="#0074a1",  # Цвет тени индикатора
        thickness=15,
        bordercolor="#131313",  # Цвет внешней рамки
    )  # Толщина прогресс-бара в пикселях


def resize_image(path="", size=(50, 50)):
    # 1. Открываем изображение (используем исходный модуль PIL.Image)
    # Если вы импортировали как "from PIL import Image", используйте просто Image.open
    original_img = Image.open(path)

    # 2. Изменяем размер
    resized_img = original_img.resize(size, Image.Resampling.LANCZOS)

    # 3. Конвертируем в формат для Tkinter (переменная с маленькой буквы)
    tk_photo = ImageTk.PhotoImage(resized_img)

    # 4. Создаем Label и называем переменную по-другому (не Image)
    image_label = Label(root, image=tk_photo, bg=styles.get("window_color"))

    # Сохраняем ссылку на картинку в самом виджете
    image_label.image = tk_photo

    return image_label


root = Tk()
# Убрал root.geometry, так как root.state("zoomed") сразу разворачивает окно
root.config(bg=styles.get("window_color"))
root.overrideredirect(True)
root.title("Tkinter Frame-Work")
root.iconbitmap("assets/system/icon/favicon.ico")
root.state("zoomed")

width = root.winfo_width()
height = root.winfo_height()

micon = resize_image("assets/system/icon/favicon-Normal-preview.png", (200, 200))
micon.place(x=width / 2 - 100, y=height / 2 - 100)
python = resize_image("assets/system/logos/python.jpg", (200, 200))
python.place(x=width / 2 - 350, y=height / 2 - 100)
tkinter = resize_image("assets/system/logos/tkinter.png", (320, 200))
tkinter.place(x=width / 2 + 150, y=height / 2 - 100)

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=300,
    mode="determinate",
    style="Horizontal.TProgressbar",
)
progress.place(x=width / 2 - 100, y=height / 2 + 150)
percent_label = Label(root, text="0%", font=("Arial", 12), bg="#ffffff")
percent_label.place(x=width / 2 - 100, y=height / 2 + 160)

init_styles()
load_result = start_loading()


if __name__ == "__main__":
    root.mainloop()
