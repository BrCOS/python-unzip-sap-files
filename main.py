from src.utils.userInput import userInput
from src.utils.unzipMainFile import unzip_main_zip_file
from src.models.unzipGLFiles import UnzipSAPFiles

def main():
    zip_path = userInput()
    print(f'\nZip file received: {zip_path}\n')

    unzip_main_zip = unzip_main_zip_file(zip_path)
    print(f'Files extracted to: {unzip_main_zip}\n')

    unzip = UnzipSAPFiles(unzip_main_zip)
    unzip.sap_version()
    unzip.trial_balance_files()
    unzip.remaining_keywords()
    unzip.unzip_selected_keywords()
    
main()