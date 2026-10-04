import json
import os
import re


class Temp:

    def __init__(self, filepath, auto_load=True, auto_save=True):
        self.filepath = filepath
        self.auto_save = auto_save
        self._data = None
        if auto_load:
            self.reload()

    def reload(self):
        """Принудительно перечитать файл с диска."""
        if not os.path.exists(self.filepath):
            self._data = {}
            return
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except Exception as e:
            print(f"Failed to load {self.filepath}: {e}")
            self._data = {}

    def save(self):
        """Сохранить текущее состояние на диск."""
        try:
            # Создаем папки пути, если их нет
            dirname = os.path.dirname(self.filepath)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)

            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save {self.filepath}: {e}")
            return False

    def _parse_path(self, path):
        """Разбивает путь по '/' и '.', игнорируя лишние разделители."""
        if path is None or path == "":
            return []
        if isinstance(path, (list, tuple)):
            return list(path)
        return [k for k in re.split(r"[/.]+", str(path).strip("/.")) if k]

    def get(self, path=None, default=None):
        if self._data is None:
            self.reload()

        keys = self._parse_path(path)
        if not keys:
            return self._data

        has_wildcard = "*" in keys
        results = self._query(self._data, keys)

        if not results:
            return default

        return results if has_wildcard else results[0]

    def _query(self, data, keys):
        """Рекурсивное чтение данных."""
        if not keys:
            return [data]

        current_key = keys[0]
        remaining = keys[1:]
        results = []

        if current_key == "*":
            if isinstance(data, list):
                for item in data:
                    results.extend(self._query(item, remaining))
            elif isinstance(data, dict):
                for val in data.values():
                    results.extend(self._query(val, remaining))
        elif isinstance(data, list) and current_key.isdigit():
            idx = int(current_key)
            if 0 <= idx < len(data):
                results.extend(self._query(data[idx], remaining))
        elif isinstance(data, dict) and current_key in data:
            results.extend(self._query(data[current_key], remaining))

        return results

    def set(self, path, value, save=None):
        """Устанавливает значение по указанному пути.

        :param path: Путь (например, 'main_interface/init_styles/Nav-TFrame'
        или 'items/0/title') :param value: Значение для записи :param save:
        Принудительно сохранить (True/False). Если None, используется
        self.auto_save
        """
        if self._data is None:
            self.reload()

        keys = self._parse_path(path)
        if not keys:
            self._data = value
        else:
            self._data = self._set_recursive(self._data, keys, value)

        should_save = self.auto_save if save is None else save
        if should_save:
            return self.save()
        return True

    def _set_recursive(self, data, keys, value):
        """Рекурсивная запись значений с поддержкой списков, словарей и wildcard (*)."""
        if not keys:
            return value

        current_key = keys[0]
        remaining = keys[1:]

        # 1. Если wildcard (*) — обновляем каждый элемент списка или словаря
        if current_key == "*":
            if isinstance(data, list):
                return [self._set_recursive(item, remaining, value) for item in data]
            elif isinstance(data, dict):
                return {
                    k: self._set_recursive(v, remaining, value) for k, v in data.items()
                }
            return data

        # 2. Если работаем со списком по индексу
        is_index = current_key.isdigit() or (
            current_key.startswith("-") and current_key[1:].isdigit()
        )

        if isinstance(data, list) or (data is None and is_index):
            if not isinstance(data, list):
                data = []

            if is_index:
                idx = int(current_key)
                if idx >= 0:
                    while len(data) <= idx:
                        data.append(None)
                elif -len(data) <= idx < 0:
                    pass  # Отрицательный индекс внутри диапазона
                else:
                    return data

                next_data = data[idx]
                if next_data is None and remaining:
                    # Если следующий ключ — число или *, готовим список, иначе словарь
                    next_data = (
                        [] if (remaining[0].isdigit() or remaining[0] == "*") else {}
                    )

                data[idx] = self._set_recursive(next_data, remaining, value)
                return data

        # 3. Если работаем со словарем
        if not isinstance(data, dict):
            data = {}

        next_data = data.get(current_key)
        if next_data is None and remaining:
            next_data = [] if (remaining[0].isdigit() or remaining[0] == "*") else {}

        data[current_key] = self._set_recursive(next_data, remaining, value)
        return data
