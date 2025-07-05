import zipfile
from pathlib import Path

def unzip_main_zip_file(main_zip_file_path: Path) -> Path:
    create_unzip_dir = f'unzip_{main_zip_file_path.stem}'

    unzip_path = main_zip_file_path.parent / create_unzip_dir
    unzip_path.mkdir(exist_ok=True)

    with zipfile.ZipFile(main_zip_file_path, 'r') as main_zip_file:
        main_zip_file.extractall(unzip_path)

    return unzip_path