import tkinter as tk
from tkinter import ttk


class AdobeHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Настройка окна (сделали базовый размер больше)
        self.title("Adobe Home Workspace")
        self.geometry("1200x800")
        self.minimum_size = (800, 600)
        self.wm_minsize(*self.minimum_size)
        self.configure(bg="#1e1e1e")

        # Исправление размытия на Windows (High DPI)
        try:
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        # Тестовые данные проектов
        self.dummy_projects = [
            ("Website_Banner_Final", "PSD", "2 hours ago"),
            ("Instagram_Post_v2", "PSD", "Yesterday"),
            ("Logo_Concept_Draft", "AI", "3 days ago"),
            ("UI_Kit_Desktop_v1", "PSD", "1 week ago"),
            ("Photo_Retouch_09", "TIFF", "2 weeks ago"),
            ("Thumbnail_Youtube", "PSD", "3 weeks ago"),
            ("Vector_Illustration", "AI", "1 month ago"),
            ("Presentation_Layout", "INDD", "1 month ago"),
        ]

        self.card_widgets = []  # Список для хранения созданных карточек
        self.init_styles()
        self.create_widgets()

        # Привязываем событие изменения размера окна для перестройки сетки
        self.bind("<Configure>", self.on_window_resize)

    def init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Стили увеличены для лучшей читаемости
        self.style.configure("Nav.TFrame", background="#141414")
        self.style.configure(
            "NavActive.TButton",
            font=("Segoe UI", 12, "bold"),
            background="#2c2c2c",
            foreground="#ffffff",
            borderwidth=0,
            focuscolor="#2c2c2c",
        )
        self.style.configure(
            "Nav.TButton",
            font=("Segoe UI", 12),
            background="#141414",
            foreground="#b5b5b5",
            borderwidth=0,
            focuscolor="#141414",
        )
        self.style.map(
            "Nav.TButton",
            background=[("active", "#2c2c2c")],
            foreground=[("active", "#ffffff")],
        )

        self.style.configure(
            "ActionCreate.TButton",
            font=("Segoe UI", 11),
            background="#1e1e1e",
            foreground="#ffffff",
            borderwidth=1,
            bordercolor="#b5b5b5",
            focuscolor="#1e1e1e",
        )
        self.style.map(
            "ActionCreate.TButton",
            background=[("active", "#323232")],
            bordercolor=[("active", "#ffffff")],
        )

        self.style.configure(
            "ActionOpen.TButton",
            font=("Segoe UI", 11, "bold"),
            background="#1473e6",
            foreground="#ffffff",
            borderwidth=0,
            focuscolor="#1473e6",
        )
        self.style.map("ActionOpen.TButton", background=[("active", "#105cb8")])

    def create_widgets(self):
        # 1. ЛЕВАЯ ПАНЕЛЬ НАВИГАЦИИ (Sidebar) - увеличена ширина до 220
        sidebar = ttk.Frame(self, style="Nav.TFrame", width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        logo_label = tk.Label(
            sidebar,
            text="Ps",
            bg="#141414",
            fg="#3fa9f5",
            font=("Segoe UI", 24, "bold"),
        )
        logo_label.pack(anchor=tk.W, padx=30, pady=(35, 25))

        btn_home = ttk.Button(
            sidebar, text="  Home", style="NavActive.TButton", cursor="hand2"
        )
        btn_home.pack(fill=tk.X, padx=15, pady=4, ipady=6)

        btn_learn = ttk.Button(
            sidebar, text="  Learn", style="Nav.TButton", cursor="hand2"
        )
        btn_learn.pack(fill=tk.X, padx=15, pady=4, ipady=6)

        btn_files = ttk.Button(
            sidebar, text="  Your files", style="Nav.TButton", cursor="hand2"
        )
        btn_files.pack(fill=tk.X, padx=15, pady=4, ipady=6)

        spacer = tk.Label(sidebar, bg="#141414")
        spacer.pack(fill=tk.Y, expand=True)

        btn_create = ttk.Button(
            sidebar, text="Create new", style="ActionCreate.TButton", cursor="hand2"
        )
        btn_create.pack(fill=tk.X, padx=25, pady=6, ipady=4)

        btn_open = ttk.Button(
            sidebar, text="Open", style="ActionOpen.TButton", cursor="hand2"
        )
        btn_open.pack(fill=tk.X, padx=25, pady=(0, 35), ipady=4)

        # 2. ГЛАВНАЯ РАБОЧАЯ ОБЛАСТЬ (Main Content)
        self.main_content = tk.Frame(self, bg="#1e1e1e")
        self.main_content.pack(
            side=tk.LEFT, fill=tk.BOTH, expand=True, padx=40, pady=35
        )

        # Верхний заголовок и поиск
        header_frame = tk.Frame(self.main_content, bg="#1e1e1e")
        header_frame.pack(fill=tk.X, pady=(0, 25))

        recent_label = tk.Label(
            header_frame,
            text="Recent",
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Segoe UI", 20, "bold"),
        )
        recent_label.pack(side=tk.LEFT)

        search_entry = tk.Entry(
            header_frame,
            bg="#2b2b2b",
            fg="#ffffff",
            insertbackground="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#3e3e3e",
            highlightcolor="#1473e6",
            font=("Segoe UI", 11),
            width=30,
        )
        search_entry.pack(side=tk.RIGHT, ipady=6, padx=5)
        search_entry.insert(0, " Search recent files...")
        search_entry.bind(
            "<FocusIn>",
            lambda e: (
                search_entry.delete(0, tk.END)
                if search_entry.get() == " Search recent files..."
                else None
            ),
        )

        # 3. АДАПТИВНАЯ ОБЛАСТЬ СКРОЛЛИНГА
        # Создаем Canvas для реализации прокрутки карточек
        self.canvas = tk.Canvas(
            self.main_content, bg="#1e1e1e", bd=0, highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.main_content, orient="vertical", command=self.canvas.yview
        )

        # Фрейм внутри Canvas, где будут размещаться карточки
        self.grid_frame = tk.Frame(self.canvas, bg="#1e1e1e")

        # Настройка связи Canvas и Scrollbar
        self.canvas.create_window(
            (0, 0), window=self.grid_frame, anchor="nw", tags="self.grid_frame"
        )
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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

    def render_grid(self):
        """Отрисовка карточек проектов"""
        # Очищаем старые виджеты, если они были
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.card_widgets.clear()

        # Параметры карточки
        card_width = 240
        card_height = 200

        # Вычисляем сколько колонок поместится в текущую ширину Canvas
        canvas_width = self.canvas.winfo_width()
        if (
            canvas_width <= 1
        ):  # Если окно еще не отрисовалось полностью, берем дефолтное значение
            canvas_width = 900

        columns = max(1, canvas_width // (card_width + 20))  # 20 — это отступы (padx)

        # Настраиваем колонки сетки, чтобы они растягивались
        for c in range(columns):
            self.grid_frame.columnconfigure(c, weight=1, minsize=card_width)

        for i, (name, fmt, time_ago) in enumerate(self.dummy_projects):
            row = i // columns
            col = i % columns

            # Контейнер карточки (теперь они крупнее)
            card = tk.Frame(
                self.grid_frame,
                bg="#1a1a1a",
                highlightthickness=1,
                highlightbackground="#2d2d2d",
                cursor="hand2",
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            card.configure(height=card_height)
            card.grid_propagate(False)

            # Миниатюра
            preview_box = tk.Frame(card, bg="#282828", height=120)
            preview_box.pack(fill=tk.X, padx=10, pady=10)
            preview_box.pack_propagate(False)

            fmt_label = tk.Label(
                preview_box,
                text=fmt,
                bg="#282828",
                fg="#5a5a5a",
                font=("Segoe UI", 18, "bold"),
            )
            fmt_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            # Метаданные
            info_frame = tk.Frame(card, bg="#1a1a1a")
            info_frame.pack(fill=tk.X, padx=12, pady=(0, 10))

            lbl_name = tk.Label(
                info_frame,
                text=name,
                bg="#1a1a1a",
                fg="#e2e2e2",
                font=("Segoe UI", 11, "bold"),
                anchor=tk.W,
                wraplength=card_width - 30,
            )
            lbl_name.pack(fill=tk.X)

            lbl_time = tk.Label(
                info_frame,
                text=time_ago,
                bg="#1a1a1a",
                fg="#7a7a7a",
                font=("Segoe UI", 10),
                anchor=tk.W,
            )
            lbl_time.pack(fill=tk.X)

            self.add_hover_effect(card, preview_box, info_frame, lbl_name, lbl_time)

    def on_window_resize(self, event):
        """Вызывается автоматически при растягивании или сужении окна"""
        # Защита от зацикливания: реагируем только на изменение размеров самого главного окна
        if event.widget == self:
            # Обновляем ширину внутреннего фрейма под Canvas
            self.canvas.itemconfig("self.grid_frame", width=self.canvas.winfo_width())
            # Перестраиваем сетку под новую ширину
            self.render_grid()

    def add_hover_effect(self, card, preview, info, title, time):
        def on_enter(e):
            card.configure(bg="#262626", highlightbackground="#444444")
            preview.configure(bg="#333333")
            info.configure(bg="#262626")
            title.configure(bg="#262626", fg="#ffffff")
            time.configure(bg="#262626")

        def on_leave(e):
            card.configure(bg="#1a1a1a", highlightbackground="#2d2d2d")
            preview.configure(bg="#282828")
            info.configure(bg="#1a1a1a")
            title.configure(bg="#1a1a1a", fg="#e2e2e2")
            time.configure(bg="#1a1a1a")

        for widget in (card, preview, info, title, time):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)


if __name__ == "__main__":
    app = AdobeHomeApp()
    app.mainloop()
