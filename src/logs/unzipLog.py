from pathlib import Path
from datetime import datetime
import time

class UnzipLog:
    def __init__(self, source_zip: Path, output_dir: Path, sap_version: str, trial_balance: str):
        self.source_zip = source_zip
        self.output_dir = output_dir
        self.sap_version = sap_version
        self.trial_balance = trial_balance
        self.start_time = time.time()
        self.zipped_files = []
        self.unzipped_files = {}
        self.errors = []

    #get the zip filename and unzipped filename in a dictionary
    def add_unzipped_files(self, zip_filename: str, unzip_filename: list):
        self.unzipped_files[zip_filename] = unzip_filename
    
    #get the error message
    def add_error(self, filename: str, error_message: str):
        self.errors.append(f'{filename}: {error_message}')

    #generate the log file before the unzip folder
    def generate_log_file(self):
        end_time = time.time()
        duration = end_time - self.start_time
        log_path = self.output_dir.parent / 'unzip_log.txt'

        with open(log_path, 'w', encoding='utf-8') as log:
            log.write(f'Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n')
            log.write(f'Main zip file: {self.source_zip.resolve()}\n')
            log.write(f'Output folder: {self.output_dir.resolve()}\n')

            minutes, seconds = divmod(int(duration), 60)
            if minutes:
                log.write(f'Total Time: {minutes} minutes and {seconds} seconds\n\n')
            else:
                log.write(f'Total Time: {seconds} seconds\n\n')

            log.write(f'Sap Version Detected: {self.sap_version}\n')
            log.write(f'Trial Balance File Detected: {self.trial_balance}\n')

            if self.unzipped_files:
                log.write(f'\nSuccessfully unzipped files:\n')

                for zip_file, unzipped_file in self.unzipped_files.items():
                    log.write(f'\n - {zip_file}:\n')

                    for txt_file in unzipped_file:
                        log.write(f'      -- {txt_file}\n')
            
            else:
                log.write('No files were unzipped.')

            if self.errors:
                log.write('\n Errors found: \n')

                for error in self.errors:
                    log.write(f' - {error}\n')
            
            else:
                log.write(f'\nNo errors were found!')

        print(f'Log saved in: {log_path.resolve()}')