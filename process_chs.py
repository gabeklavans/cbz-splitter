import os
import argparse
import re
import zipfile
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

out_dir = "chapter_cbzs"
os.mkdir(out_dir)

def create_ch(chapter: str):
    chapter_files = list(filter(lambda file_name: chapter in file_name, file_names))
    chapter_files.sort()

    chapter_file_name = re.sub(r" - p\d{3}", "", chapter_files[0])
    chapter_file_name = os.path.splitext(chapter_file_name)[0]
    with zipfile.ZipFile(f"{chapter_file_name}.zip", "w") as ch_zip:
        for chapter_file in chapter_files:
            ch_zip.write(os.path.join(directory_path, chapter_file))

    os.rename(f"{chapter_file_name}.zip", os.path.join(out_dir, f"{chapter_file_name}.cbz"))

def run(func, chapters):
    n_workers = os.cpu_count()

    with ProcessPoolExecutor(n_workers) as executor:
        results = list(tqdm(executor.map(func, chapters), total=len(chapters)))
    return results

parser = argparse.ArgumentParser(description='')

parser.add_argument('directory', type=str, help='the path to the directory')

args = parser.parse_args()

directory_path = args.directory
file_names = os.listdir(directory_path)

chapters = set()
for file_name in file_names:
    chapter = re.findall(r"c\d{4}", file_name)

    if len(chapter) == 0:
        print(f"No c number found for {file_name}")
        continue
    if len(chapter) > 1:
        raise RuntimeError("Multiple c numbers found")

    chapters.add(chapter[0])

run(create_ch, chapters)
