import os
import shutil
from pathlib import Path
import stat

class FileManager:
    def __init__(self, base_path):
        self.base_path = Path(base_path).resolve()
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True)

    def list_directory(self):
        print(f"Содержимое каталога {self.base_path}:")
        for item in self.base_path.iterdir():
            item_type = "Папка" if item.is_dir() else "Файл"
            print(f"{item_type}: {item.name}")

    def create_file(self, file_name):
        file_path = self.base_path / file_name
        try:
            file_path.touch(exist_ok=False)
            print(f"Файл '{file_name}' создан.")
        except FileExistsError:
            print(f"Файл '{file_name}' уже существует.")

    def create_directory(self, dir_name):
        dir_path = self.base_path / dir_name
        try:
            dir_path.mkdir()
            print(f"Каталог '{dir_name}' создан.")
        except FileExistsError:
            print(f"Каталог '{dir_name}' уже существует.")

    def delete(self, name):
        path = self.base_path / name
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"'{name}' удалено.")
        except FileNotFoundError:
            print(f"'{name}' не найдено.")

    def move(self, name, target_dir):
        src_path = self.base_path / name
        target_path = self.base_path / target_dir / name
        try:
            shutil.move(str(src_path), str(target_path))
            print(f"'{name}' перемещено в '{target_dir}'.")
        except FileNotFoundError:
            print(f"'{name}' или '{target_dir}' не найдено.")

    def rename(self, old_name, new_name):
        src_path = self.base_path / old_name
        dst_path = self.base_path / new_name
        try:
            src_path.rename(dst_path)
            print(f"'{old_name}' переименовано в '{new_name}'.")
        except FileNotFoundError:
            print(f"'{old_name}' не найдено.")

    def copy(self, name, target_dir):
        src_path = self.base_path / name
        target_path = self.base_path / target_dir / name
        try:
            if src_path.is_dir():
                shutil.copytree(src_path, target_path)
            else:
                shutil.copy(src_path, target_path)
            print(f"'{name}' скопировано в '{target_dir}'.")
        except FileNotFoundError:
            print(f"'{name}' или '{target_dir}' не найдено.")
        except FileExistsError:
            print(f"'{name}' уже существует в '{target_dir}'.")

    def change_permissions(self, name, read=True, write=True, execute=False):
        path = self.base_path / name
        try:
            mode = 0
            if read:
                mode |= stat.S_IREAD
            if write:
                mode |= stat.S_IWRITE
            if execute:
                mode |= stat.S_IEXEC
            path.chmod(mode)
            print(f"Права для '{name}' обновлены.")
        except FileNotFoundError:
            print(f"'{name}' не найдено.")

    def search(self, keyword):
        print(f"Результаты поиска для '{keyword}':")
        for item in self.base_path.rglob(f"*{keyword}*"):
            print(item.relative_to(self.base_path))

    def edit_file(self, file_name):
        file_path = self.base_path / file_name
        try:
            with file_path.open('r+') as file:
                print(f"Содержимое '{file_name}':")
                print(file.read())
                file.seek(0, os.SEEK_END)
                content = input("Введите текст для добавления: ")
                file.write("\n" + content)
                print(f"Текст добавлен в '{file_name}'.")
        except FileNotFoundError:
            print(f"Файл '{file_name}' не найден.")
        except IsADirectoryError:
            print(f"'{file_name}' является каталогом, а не файлом.")

# Пример использования:
if __name__ == "__main__":
    manager = FileManager(".")
    manager.list_directory()
    manager.create_file("example.txt")
    manager.edit_file("example.txt")
    manager.create_directory("new_folder")
    manager.move("example.txt", "new_folder")
    manager.copy("new_folder", "copy_folder")
    manager.rename("new_folder", "renamed_folder")
    manager.delete("copy_folder")
    manager.search("example")
