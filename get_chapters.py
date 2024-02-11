import os
import argparse
import zipfile
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

parser = argparse.ArgumentParser(description='')

parser.add_argument('directory', type=str, help='the path to the directory')

args = parser.parse_args()

directory_path = args.directory
file_names = os.listdir(directory_path)

def unzip_file(zip_filename):
    with zipfile.ZipFile(os.path.join(directory_path, zip_filename), "r") as cbz_file:
        cbz_file.extractall("chapters")

def run(func, file_names):
    n_workers = os.cpu_count()

    with ProcessPoolExecutor(n_workers) as executor:
        results = list(tqdm(executor.map(func, file_names), total=len(file_names)))
    return results

run(unzip_file, file_names)
