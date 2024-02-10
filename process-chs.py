import os
import argparse
import re
import zipfile

parser = argparse.ArgumentParser(description='')

parser.add_argument('directory', type=str, help='the path to the directory')

args = parser.parse_args()

directory_path = args.directory
file_names = os.listdir(directory_path)

chapters = set()
for file_name in file_names:
    chapter = re.findall(r"c\d{4}", file_name)

    if len(chapter) == 0:
        raise RuntimeError("No c number found")
    if len(chapter) > 1:
        raise RuntimeError("Multiple c numbers found")

    chapters.add(chapter[0])

for chapter in chapters:
    chapter_files = list(filter(lambda file_name: chapter in file_name, file_names))
    chapter_files.sort()

    # chapter_file_name = " - ".join(os.path.splitext(chapter_files[0])[0].split(" - ")[:3])
    chapter_file_name = re.sub(r" - p\d{3}", "", chapter_files[0])
    with zipfile.ZipFile(f"{chapter_file_name}.zip", "w") as ch_zip:
        for chapter_file in chapter_files:
            ch_zip.write(os.path.join(directory_path, chapter_file))
    
    os.rename(f"{chapter_file_name}.zip", f"{chapter_file_name}.cbz")
