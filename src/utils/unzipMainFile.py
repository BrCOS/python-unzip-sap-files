import zipfile
from pathlib import Path

def unzip_main_zip_file(main_zip_file_path: Path) -> Path:
    #add an 'unzip' prefix to the folder to be created
    create_unzip_dir = f'unzip_{main_zip_file_path.stem}'

    #create the folder with the prefix to unzip the file into
    #check if the folder already exists, creates it if it doesn't
    unzip_path = main_zip_file_path.parent / create_unzip_dir
    unzip_path.mkdir(exist_ok=True)

    #unzip the main file into the created folder
    with zipfile.ZipFile(main_zip_file_path, 'r') as main_zip_file:
        print('Unzipping Main File...')
        main_zip_file.extractall(unzip_path)

    return unzip_path