import json
import os
from pathlib import Path
import subprocess
import sys
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from sections import Section
from temp import Temp


class AdobeHomeApp(Tk):

    def __init__(self):
        super().__init__()
        self.last_cols = None
        self._resize_job = None
        current_dir = Path(__file__).resolve().parent.parent
        json_path = current_dir / "data" / "temp.json"
        if not json_path.exists():
            json_path = current_dir / "data" / "Temp.json"

        temp_loader = Temp(json_path)

        style_file = temp_loader.get("loaded_json/style", "default.json")
        style_path = current_dir / "assets" / "styles" / f"{style_file}"
        self.styles = Temp(style_path)
        self.files_style = temp_loader.get("loaded_json/style_files")

        # Настройка окна (сделали базовый размер больше)
        self.title("Tkinter FrameWork")
        self.geometry("1200x800")
        self.minimum_size = (800, 600)
        self.wm_minsize(*self.minimum_size)
        self.configure(bg=self.styles.get("window_color", "#1e1e1e"))

        try:
            self.iconbitmap("assets/system/icon/favicon.ico")
        except Exception:
            pass

        self.tk.call("tk", "scaling", 3.0)

        # Исправление размытия на Windows (High DPI)
        try:
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        # Переменные
        self.section = Section()
        self.widgets_on_screen = []
        self.current_section = "home"

        self.state("zoomed")

        self.init_styles()
        self.create_widgets()

    def init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Nav.TFrame",
            background=self.styles.get(
                "main_interface/init_styles/Nav-TFrame", "#141414"
            ),
        )  # "#141414"
        self.style.configure(
            "UP.TFrame",
            background=self.styles.get(
                "main_interface/init_styles/UP-TFrame", "#383838"
            ),
        )

        self.style.configure(
            "Vertical.TScrollbar",
            **(self.styles.get("main_interface/init_styles/Vertical-TScrollbar") or {}),
        )  # Цвет стрелочек внутри кнопок

        # Изменение цвета при наведении (hover)
        self.style.map(
            "Vertical.TScrollbar",
            background=[
                (
                    "active",
                    self.styles.get(
                        "main_interface/init_styles/active/Vertical-TScrollbar"
                    ),
                )
            ],
        )

        self.style.configure(
            "NavFocus.TButton",
            **(self.styles.get("main_interface/init_styles/NavFocus-TButton") or {}),
            background=self.styles.get(
                "main_interface/init_styles/Nav-TFrame", "#141414"
            ),
        )
        self.style.map(
            "NavFocus.TButton",
            background=[
                (
                    "active",
                    self.styles.get("main_interface/init_styles/Nav-TFrame"),
                )
            ],
        )

        self.style.configure(
            "NavFocusOut.TButton",
            **(self.styles.get("main_interface/init_styles/NavFocusOut-TButton") or {}),
            background=self.styles.get(
                "main_interface/init_styles/Nav-TFrame", "#141414"
            ),
        )
        self.style.map(
            "NavFocusOut.TButton",
            background=[
                (
                    "active",
                    self.styles.get(
                        "main_interface/init_styles/active/NavFocusOut-TButton"
                    ),
                )
            ],
        )

        self.style.configure(
            "ActionOpen.TButton",
            **(self.styles.get("main_interface/init_styles/ActionOpen-TButton") or {}),
        )
        self.style.map(
            "ActionOpen.TButton",
            background=[
                (
                    "active",
                    self.styles.get(
                        "main_interface/init_styles/active/ActionOpen-TButton"
                    ),
                )
            ],
        )
        self.style.configure(
            "ActionCreate.TButton",
            **(
                self.styles.get("main_interface/init_styles/ActionCreate-TButton") or {}
            ),
        )
        self.style.map(
            "ActionCreate.TButton",
            background=[
                (
                    "active",
                    self.styles.get(
                        "main_interface/init_styles/active/ActionCreate-TButton"
                    ),
                )
            ],
        )

    def create_widgets(self):
        # ------------------------------------------------------ Элементы topbar ------------------------------------------------------
        topbar = ttk.Frame(self, style="UP.TFrame", height=190)
        topbar.pack(side=TOP, fill=X)
        topbar.pack_propagate(False)
        # ------------------------------------------------------ Элементы topbar ------------------------------------------------------

        micon = self.resize_image(
            topbar,
            background=self.styles.get(
                "main_interface/init_styles/UP-TFrame", "#383838"
            ),
            path="assets/system/icon/favicon-Normal-preview.png",
            size=(150, 150),
        )
        micon.pack(padx=25, side=LEFT)  # padx=25, pady=35,

        welcome_label = Label(
            topbar,
            text="Welcome to Tkinter FrameWork",
            bg=self.styles.get("main_interface/init_styles/UP-TFrame", "#383838"),
            fg=self.styles.get(
                "main_interface/create_widgets/welcome_label", "#ADADAD"
            ),
            font=("Century Gothic", 16, "bold"),
        )
        welcome_label.pack(expand=True)

        # ------------------------------------------------------ Элементы sidebar ------------------------------------------------------
        sidebar = ttk.Frame(self, style="Nav.TFrame", width=440)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)
        # ------------------------------------------------------ Элементы sidebar ------------------------------------------------------

        btn_home = ttk.Button(
            sidebar,
            text="Home",
            style="NavFocus.TButton",
            cursor="hand2",
            command=lambda: self.open_section("home", btn_home),
        )
        btn_home.pack(fill=X, padx=25, pady=(35, 0), ipady=4, side="top")

        btn_utilites = ttk.Button(
            sidebar,
            text="Utilites",
            style="NavFocusOut.TButton",
            cursor="hand2",
            command=lambda: self.open_section("utilites", btn_utilites),
        )
        btn_utilites.pack(fill=X, padx=25, pady=(35, 0), ipady=4, side="top")

        btn_styles = ttk.Button(
            sidebar,
            text="Styles",
            style="NavFocusOut.TButton",
            cursor="hand2",
            command=lambda: self.open_section("styles", btn_styles),
        )
        btn_styles.pack(fill=X, padx=25, pady=(35, 0), ipady=4, side="top")

        btn_settings = ttk.Button(
            sidebar,
            text="Settings",
            style="NavFocusOut.TButton",
            cursor="hand2",
            command=lambda: self.open_section("settings", btn_settings),
        )
        btn_settings.pack(fill=X, padx=25, pady=(35, 0), ipady=4, side="top")

        self.sections_btns = [btn_home, btn_utilites, btn_styles, btn_settings]

        btn_open = ttk.Button(
            sidebar, text="Open", style="ActionOpen.TButton", cursor="hand2"
        )
        btn_open.pack(fill=X, padx=25, pady=(0, 35), ipady=4, side="bottom")
        btn_create = ttk.Button(
            sidebar, text="Create", style="ActionCreate.TButton", cursor="hand2"
        )
        btn_create.pack(fill=X, padx=25, pady=(0, 35), ipady=4, side="bottom")

        # ------------------------------------------------------ Элементы main_content ------------------------------------------------------
        win_color = self.styles.get("window_color", "#1e1e1e")
        self.main_content = Frame(self, bg=win_color)
        self.main_content.pack(side=LEFT, fill=BOTH, expand=True, padx=40, pady=35)
        # ------------------------------------------------------ Элементы main_content ------------------------------------------------------

        search_entry = Entry(
            self.main_content,
            **(self.styles.get("main_interface/create_widgets/search_entry") or {}),
        )
        search_entry.pack(anchor="ne", ipady=6, padx=10)
        search_entry.insert(0, " Search recent files...")
        search_entry.bind(
            "<FocusIn>",
            lambda e: (
                search_entry.delete(0, END)
                if search_entry.get() == " Search recent files..."
                else None
            ),
        )

        recent_label = Label(
            self.main_content,
            text="Recent",
            **(self.styles.get("main_interface/create_widgets/recent_label") or {}),
            bg=win_color,
        )
        recent_label.pack(side=TOP, padx=10)

        # ------------------------------------------------------ Рендер карточек проектов ------------------------------------------------------

        self.canvas = Canvas(
            self.main_content,
            bg=win_color,
            bd=0,
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            self.main_content,
            style="Vertical.TScrollbar",
            orient="vertical",
            command=self.canvas.yview,
        )

        # Фрейм внутри Canvas, где будут размещаться карточки
        self.grid_frame = Frame(
            self.canvas,
            bg=win_color,
        )

        # Настройка связи Canvas и Scrollbar
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.grid_frame, anchor="nw"
        )

        # Растягиваем внутренний grid_frame по ширине canvas
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Обновление области прокрутки при изменении размеров внутреннего фрейма
        self.grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Позволяем прокручивать колесиком мыши
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        # Первичная отрисовка карточек
        self.open_section("home", btn_home)

    def on_canvas_configure(self, event):
        # 1. Растягиваем внутренний фрейм по ширине canvas
        self.canvas.itemconfig(self.canvas_window, width=event.width)

        # 2. Вычисляем новое количество колонок
        card_width = 240
        gap = 20
        raw_cols = event.width // (card_width + gap)

        if raw_cols >= 6:
            new_cols = 6
        elif raw_cols == 5:
            new_cols = 5
        elif raw_cols == 4:
            new_cols = 4
        else:
            new_cols = 3

        # 3. Если количество колонок изменилось, плавно перерисовываем карточки
        if self.last_cols != new_cols:
            self.last_cols = new_cols
            if self._resize_job:
                self.after_cancel(self._resize_job)
            self._resize_job = self.after(50, self.render_current_section)

    def open_section(self, section, section_btn):
        self.current_section = section
        self.last_cols = None  # Сбрасываем для принудительной отрисовки

        # Переключаем подсветку кнопок меню
        for btn in self.sections_btns:
            btn.configure(style="NavFocusOut.TButton")
        section_btn.configure(style="NavFocus.TButton")

        # Отрисовываем выбранную секцию
        self.render_current_section()

    def render_current_section(self):
        """Очищает экран и отрисовывает карточки текущей вкладки."""
        self.clear_screen()
        if self.current_section == "home":
            self.section.render_grid(self.grid_frame, self.canvas)
        elif self.current_section == "styles":
            self.section.render_styles_grid(self.grid_frame, self.canvas)

    def clear_screen(self):
        # 1. Удаляем все виджеты
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # 2. Сбрасываем старые колонки сетки (чтобы они не сжимали новые карточки)
        cols, rows = self.grid_frame.grid_size()
        for c in range(cols + 10):  # с запасом обнуляем все колонки
            self.grid_frame.columnconfigure(c, weight=0, minsize=0)

        # 3. Сбрасываем скролл в самый верх
        self.canvas.yview_moveto(0)

    def resize_image(self, parent, background, path="", size=(50, 50)):
        # 1. Открываем изображение (используем исходный модуль PIL.Image)
        original_img = Image.open(path)

        # 2. Изменяем размер
        resized_img = original_img.resize(size, Image.Resampling.LANCZOS)

        # 3. Конвертируем в формат для Tkinter (переменная с маленькой буквы)
        tk_photo = ImageTk.PhotoImage(resized_img)

        # 4. Создаем Label и называем переменную по-другому (не Image)
        image_label = Label(parent, image=tk_photo, bg=background)

        # Сохраняем ссылку на картинку в самом виджете
        image_label.image = tk_photo

        return image_label


if __name__ == "__main__":
    app = AdobeHomeApp()
    app.mainloop()
