import argparse
import logging
import sys
from shutil import copyfile
from pathlib import Path
from threading import Thread


CATEGORIES = {
    "Archives": [".zip", ".gz", ".tar"],
    "Audio": [".mp3", ".wav", ".flac", ".wma", ".ogg"],
    "Video": [".avi", ".mp4", ".mov", ".mkv"],
    "Images": [".jpeg", ".png", ".jpg", ".svg", ".gif"],
    "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "Python": [
        ".py",
        ".rpy",
        ".pyw",
        ".cpy",
        ".gyp",
        ".gypi",
        ".pui",
        ".ipy",
        ".pyt",
        ".whl",
    ],
    "Other": [],
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "jo",
    "zh",
    "z",
    "y",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "`",
    "y",
    "'",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[c] = l
    TRANS[c.upper()] = l.upper()


def normalize(file_name: str) -> str:
    name = str(Path(file_name).stem)
    result = ""
    for i in range(len(name)):
        if "0" <= name[i] <= "9" or "a" <= name[i] <= "z" or "A" <= name[i] <= "Z":
            result += name[i]
        elif name[i] in TRANS:
            result += TRANS[name[i]]
        else:
            result += "_"
    return result + str(Path(file_name).suffix)


def get_categories(file: Path) -> str:  
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


"""
--source [-s] 
--output [-o] default folder = dist
"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

print(parser.parse_args())
args = vars(parser.parse_args())
print(args)

source = Path(args.get("source"))
output = Path(args.get("output"))

folders = []


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(path: Path) -> None:
     for el in path.iterdir():
       if el.is_file():
            ext_folder = source / get_categories(el)
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)
                copyfile(el, ext_folder / normalize(el.name))
            except OSError as err:
                logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    folders.append(source)
    grabs_folder(source)
    print(folders)

    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder, ))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print(f"Можна видалять {source}")