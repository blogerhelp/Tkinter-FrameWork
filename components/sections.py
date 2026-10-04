from pathlib import Path
from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from temp import Temp


class Section:

    def __init__(self):
        current_dir = Path(__file__).resolve().parent.parent
        json_path = current_dir / "data" / "temp.json"
        if not json_path.exists():
            json_path = current_dir / "data" / "Temp.json"

        style_file_loader = Temp(json_path)
        style_file = style_file_loader.get("loaded_json/style", "default.json")
        style_path = current_dir / "assets" / "styles" / f"{style_file}"
        self.styles = Temp(style_path)

    # ------------------ КАРТОЧКИ ПРОЕКТОВ (HOME) ------------------

    def render_grid(self, grid_frame, canvas):
        self.grid_frame = grid_frame
        self.canvas = canvas
        self.canvas.update_idletasks()

        card_width = 840
        card_height = 650
        gap = 20  # отступы между карточками

        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 1200

        # Считаем, сколько карточек ПОЛНОГО размера влезает
        raw_cols = canvas_width // (card_width + gap)

        # Ограничиваем: максимум 6, минимум 3
        if raw_cols >= 6:
            columns = 6
        elif raw_cols == 5:
            columns = 5
        elif raw_cols == 4:
            columns = 4
        else:
            # 3 карточки минимум (если экран еще уже, они будут сжиматься)
            columns = 3

        # Настраиваем колонки одинаковой ширины
        for c in range(columns):
            self.grid_frame.columnconfigure(c, weight=1, uniform="card_col")

        current_dir = Path(__file__).resolve().parent.parent
        json_path = current_dir / "data" / "temp.json"
        if not json_path.exists():
            json_path = current_dir / "data" / "Temp.json"
        json_manager_temp = Temp(json_path)

        projects = json_manager_temp.get("loaded_projects.*") or []
        for i, project in enumerate(projects):
            name = project.get("name", "Project")
            fmt = project.get("fmt", "Py")
            time_ago = project.get("time", "20-Aug-2026")
            self.create_card(i, name, fmt, time_ago, columns, card_height, card_width)

        self.grid_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_card(self, i, name, fmt, time_ago, columns, card_height, card_width):
        row = i // columns
        col = i % columns

        # Контейнер карточки
        card = Frame(
            self.grid_frame,
            **self.styles.get(
                "main_interface/create_widgets/main_space/card/cardFrame"
            ),
        )
        card.grid(row=row, column=col, padx=8, pady=10, sticky="nsew")
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
            wraplength=card_width - 20,
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

    # ------------------ КАРТОЧКИ СТИЛЕЙ (STYLES) ------------------

    def render_styles_grid(self, grid_frame, canvas):
        self.grid_frame = grid_frame
        self.canvas = canvas
        self.canvas.update_idletasks()

        card_width = 240
        card_height = 650
        gap = 20

        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 1200

        # Считаем, сколько карточек ПОЛНОГО размера влезает
        raw_cols = canvas_width // (card_width + gap)

        if raw_cols >= 6:
            columns = 6
        elif raw_cols == 5:
            columns = 5
        elif raw_cols == 4:
            columns = 4
        else:
            columns = 3

        # Настраиваем колонки одинаковой ширины
        for c in range(columns):
            self.grid_frame.columnconfigure(c, weight=1, uniform="card_col")

        current_dir = Path(__file__).resolve().parent.parent
        json_path = current_dir / "data" / "temp.json"
        if not json_path.exists():
            json_path = current_dir / "data" / "Temp.json"
        json_manager_temp = Temp(json_path)

        style_files = json_manager_temp.get("loaded_json.style_files") or []
        for i, file in enumerate(style_files):
            style_file_path = current_dir / "assets" / "styles" / f"{file}"
            if not style_file_path.exists():
                continue

            self.single_style = Temp(style_file_path)

            name = self.single_style.get("style_info.name", "Default")
            author = self.single_style.get("style_info.author.title", "Unknown")
            description = self.single_style.get(
                "style_info.description.title", "No description"
            )

            self.create_style_card(
                i,
                name,
                self.single_style.get("style_info.name_box.name") or {},
                author,
                self.single_style.get("style_info.bg", "#1a1a1a"),
                self.single_style.get("style_info.name_box.bg", "#282828"),
                self.single_style.get("style_info.author.styles") or {},
                description,
                self.single_style.get("style_info.description.styles") or {},
                columns,
                card_height,
                card_width,
            )

        self.grid_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_style_card(
        self,
        i,
        name,
        name_styles,
        author,
        card_bg,
        name_box,
        author_styles,
        description,
        description_styles,
        columns,
        card_height,
        card_width,
    ):
        row = i // columns
        col = i % columns

        # Контейнер карточки
        card = Frame(
            self.grid_frame,
            bg=card_bg,
        )
        card.grid(row=row, column=col, padx=8, pady=10, sticky="nsew")
        card.configure(height=card_height)
        card.pack_propagate(False)

        # Миниатюра
        preview_box = Frame(
            card,
            bg=name_box,
            height=450,
        )
        preview_box.pack(fill=X, padx=10, pady=10)
        preview_box.pack_propagate(False)

        fmt_label = Label(
            preview_box,
            text=name,
            **(name_styles or {}),
            bg=name_box,
        )
        fmt_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Метаданные
        info_frame = Frame(
            card,
            bg=card_bg,
        )
        info_frame.pack(fill=X, padx=12, pady=(0, 10))

        lbl_name = Label(
            info_frame,
            text=author,
            bg=card_bg,
            **(author_styles or {}),
            anchor=W,
            wraplength=card_width - 20,
        )
        lbl_name.pack(fill=X)

        lbl_time = Label(
            info_frame,
            text=description,
            bg=card_bg,
            **(description_styles or {}),
            anchor=W,
            wraplength=card_width - 20,
        )
        lbl_time.pack(fill=X)

        hoverstyle = self.single_style.get("style_info.hover_effect.on_enter")

        self.add_style_hover_effect(
            card,
            preview_box,
            info_frame,
            lbl_name,
            lbl_time,
            fmt_label,
            hoverstyle,
        )

    # ------------------ ХОВЕР ЭФФЕКТЫ ------------------

    def add_hover_effect(self, card, preview, info, title, time, fmt):
        widgets_map = {
            "card": card,
            "preview": preview,
            "info": info,
            "title": title,
            "time": time,
            "fmt": fmt,
        }

        hover_in = (
            self.styles.get(
                "main_interface/create_widgets/main_space/card/hover_effect/on_enter"
            )
            or {}
        )

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

        for widget in widgets_map.values():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def add_style_hover_effect(self, card, preview, info, title, time, fmt, hoverstyle):
        widgets_map = {
            "card": card,
            "preview": preview,
            "info": info,
            "title": title,
            "time": time,
            "fmt": fmt,
        }

        hover_in = hoverstyle or {}

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

        for widget in widgets_map.values():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
