from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import os
import json
import sys
from pathlib import Path
from PIL import Image, ImageTk
import subprocess
from temp import Temp


class AdobeHomeApp(Tk):
    def __init__(self):
        super().__init__()
        current_dir = Path(__file__).resolve().parent.parent
        json_path = current_dir / "data" / "temp.json"
        style_file_loader = Temp(json_path)
        style_file = style_file_loader.get("loaded_json/style")
        style_path = current_dir / "assets" / "styles" / f"{style_file}"
        self.styles = Temp(style_path)

        # Настройка окна (сделали базовый размер больше)
        self.title("Tkinter Frame Work")
        self.geometry("1200x800")
        self.minimum_size = (800, 600)
        self.wm_minsize(*self.minimum_size)
        self.configure(bg=self.styles.get("window_color"))
        self.iconbitmap("assets/system/icon/favicon.ico")
        self.tk.call("tk", "scaling", 3.0)

        # Исправление размытия на Windows (High DPI)
        try:
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.state("zoomed")
        self.init_styles()
        self.create_widgets()

    def init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Nav.TFrame",
            background=self.styles.get("main_interface/init_styles/Nav-TFrame"),
        )  # "#141414"
        self.style.configure(
            "UP.TFrame",
            background=self.styles.get("main_interface/init_styles/UP-TFrame"),
        )

        self.style.configure(
            "Vertical.TScrollbar",
            **self.styles.get("main_interface/init_styles/Vertical-TScrollbar"),
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
            **self.styles.get("main_interface/init_styles/NavFocus-TButton"),
            background=self.styles.get("main_interface/init_styles/Nav-TFrame"),
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
            **self.styles.get("main_interface/init_styles/NavFocusOut-TButton"),
            background=self.styles.get("main_interface/init_styles/Nav-TFrame"),
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
            **self.styles.get("main_interface/init_styles/ActionOpen-TButton"),
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
            **self.styles.get("main_interface/init_styles/ActionCreate-TButton"),
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
            background=self.styles.get("main_interface/init_styles/UP-TFrame"),
            path="assets/system/icon/favicon-Normal-preview.png",
            size=(150, 150),
        )
        micon.pack(padx=25, side=LEFT)  # padx=25, pady=35,

        welcome_label = Label(
            topbar,
            text="Welcome to Tkinter FrameWork",
            bg=self.styles.get("main_interface/init_styles/UP-TFrame"),
            fg=self.styles.get("main_interface/create_widgets/welcome_label"),
            font=("Century Gothic", 16, "bold"),
        )
        welcome_label.pack(expand=True)

        # ------------------------------------------------------ Элементы sidebar ------------------------------------------------------
        sidebar = ttk.Frame(self, style="Nav.TFrame", width=440)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)
        # ------------------------------------------------------ Элементы sidebar ------------------------------------------------------

        btn_home = ttk.Button(
            sidebar, text="Home", style="NavFocus.TButton", cursor="hand2"
        )
        btn_home.pack(fill=X, padx=25, pady=(35, 0), ipady=4, side="top")

        btn_utilites = ttk.Button(
            sidebar, text="Utilites", style="NavFocusOut.TButton", cursor="hand2"
        )
        btn_utilites.pack(fill=X, padx=25, pady=(35, 0), ipady=4, side="top")

        btn_styles = ttk.Button(
            sidebar, text="Styles", style="NavFocusOut.TButton", cursor="hand2"
        )
        btn_styles.pack(fill=X, padx=25, pady=(35, 0), ipady=4, side="top")

        btn_settings = ttk.Button(
            sidebar, text="Settings", style="NavFocusOut.TButton", cursor="hand2"
        )
        btn_settings.pack(fill=X, padx=25, pady=(35, 0), ipady=4, side="top")

        btn_open = ttk.Button(
            sidebar, text="Open", style="ActionOpen.TButton", cursor="hand2"
        )
        btn_open.pack(fill=X, padx=25, pady=(0, 35), ipady=4, side="bottom")
        btn_create = ttk.Button(
            sidebar, text="Create", style="ActionCreate.TButton", cursor="hand2"
        )
        btn_create.pack(fill=X, padx=25, pady=(0, 35), ipady=4, side="bottom")

        # ------------------------------------------------------ Элементы main_content ------------------------------------------------------
        self.main_content = Frame(self, bg=self.styles.get("window_color"))
        self.main_content.pack(side=LEFT, fill=BOTH, expand=True, padx=40, pady=35)
        # ------------------------------------------------------ Элементы main_content ------------------------------------------------------

        search_entry = Entry(
            self.main_content,
            **self.styles.get("main_interface/create_widgets/search_entry"),
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
            **self.styles.get("main_interface/create_widgets/recent_label"),
            bg=self.styles.get("window_color"),
        )
        recent_label.pack(side=TOP, padx=10)

        # ------------------------------------------------------ Рендер карточек проектов ------------------------------------------------------

        self.canvas = Canvas(
            self.main_content,
            bg=self.styles.get("window_color"),
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
            bg=self.styles.get("window_color"),
        )

        # Настройка связи Canvas и Scrollbar
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.grid_frame, anchor="nw"
        )

        # Растягиваем внутренний grid_frame по ширине canvas
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )
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
        self.render_grid()

    def create_card(self, i, name, fmt, time_ago, columns, card_height, card_width):
        row = i // columns
        col = i % columns

        # Контейнер карточки (теперь они крупнее)
        card = Frame(
            self.grid_frame,
            **self.styles.get(
                "main_interface/create_widgets/main_space/card/cardFrame"
            ),
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.configure(height=card_height)
        card.pack_propagate(False)

        # Миниатюра
        preview_box = Frame(
            card,
            bg=self.styles.get(
                "main_interface/create_widgets/main_space/card/preview_box/bg"
            ),
            height=450,
        )
        preview_box.pack(fill=X, padx=10, pady=10)
        preview_box.pack_propagate(False)

        fmt_label = Label(
            preview_box,
            text=fmt,
            **self.styles.get(
                "main_interface/create_widgets/main_space/card/preview_box/fmt_label"
            ),
            bg=self.styles.get(
                "main_interface/create_widgets/main_space/card/preview_box/bg"
            ),
        )
        fmt_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Метаданные
        info_frame = Frame(
            card,
            bg=self.styles.get(
                "main_interface/create_widgets/main_space/card/cardFrame/bg"
            ),
        )
        info_frame.pack(fill=X, padx=12, pady=(0, 10))

        lbl_name = Label(
            info_frame,
            text=name,
            bg=self.styles.get(
                "main_interface/create_widgets/main_space/card/cardFrame/bg"
            ),
            **self.styles.get("main_interface/create_widgets/main_space/card/lbl_name"),
            anchor=W,
            wraplength=card_width - 30,
        )
        lbl_name.pack(fill=X)

        lbl_time = Label(
            info_frame,
            text=time_ago,
            bg=self.styles.get(
                "main_interface/create_widgets/main_space/card/cardFrame/bg"
            ),
            **self.styles.get("main_interface/create_widgets/main_space/card/lbl_time"),
            anchor=W,
        )
        lbl_time.pack(fill=X)

        self.add_hover_effect(
            card, preview_box, info_frame, lbl_name, lbl_time, fmt_label
        )
        print("work")

    def render_grid(self):
        card_width = 240
        card_height = 600
        canvas_width = self.canvas.winfo_width()
        if (
            canvas_width <= 1
        ):  # Если окно еще не отрисовалось полностью, берем дефолтное значение
            canvas_width = 900

        columns = max(1, canvas_width // (card_width + 20))  # 20 — это отступы (padx)

        # Настраиваем колонки сетки, чтобы они растягивались
        current_dir = Path(__file__).resolve().parent
        json_path = current_dir.parent / "data" / "temp.json"
        json_manager_temp = Temp(json_path)
        for c in range(columns):
            self.grid_frame.columnconfigure(c, weight=1, minsize=card_width)
        projects = json_manager_temp.get("loaded_projects.*") or []
        for i, project in enumerate(projects):
            name = project["name"]
            fmt = project["fmt"]
            time_ago = project["time"]
            print(f"time_ago + {time_ago}")
            self.create_card(i, name, fmt, time_ago, columns, card_height, card_width)

    def add_hover_effect(self, card, preview, info, title, time, fmt):
        widgets_map = {
            "card": card,
            "preview": preview,
            "info": info,
            "title": title,
            "time": time,
            "fmt": fmt,
        }

        # Получаем стили для наведения
        hover_in = (
            self.styles.get(
                "main_interface/create_widgets/main_space/card/hover_effect/on_enter"
            )
            or {}
        )

        # Автоматически считываем и запоминаем начальные параметры виджетов
        initial_styles = {}
        for key, widget in widgets_map.items():
            if key in hover_in:
                initial_styles[key] = {
                    prop: widget.cget(prop) for prop in hover_in[key].keys()
                }

        def on_enter(e):
            for key, widget in widgets_map.items():
                if key in hover_in:
                    widget.configure(**hover_in[key])

        def on_leave(e):
            for key, widget in widgets_map.items():
                if key in initial_styles:
                    widget.configure(**initial_styles[key])

        # Привязываем события ко всем элементам карточки
        for widget in widgets_map.values():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def resize_image(self, parent, background, path="", size=(50, 50)):
        # 1. Открываем изображение (используем исходный модуль PIL.Image)
        # Если вы импортировали как "from PIL import Image", используйте просто Image.open
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
