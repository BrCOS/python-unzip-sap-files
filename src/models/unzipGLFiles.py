import zipfile
from pathlib import Path
from src.utils.keywords import KEYWORDS
from src.logs.unzipLog import UnzipLog

class UnzipSAPFiles:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.output_dir = root_path / 'unzip'
        self.output_dir.mkdir(exist_ok=True)
        self.keywords = [keyword.upper() for keyword in KEYWORDS]
        self.selected_keywords = []

    #detec SAP version based on the files
    def sap_version(self):
        for ledger_file in self.root_path.rglob('*zip'):
            sap_name = ledger_file.stem.upper()

            if 'BSEG' in sap_name:
                self.selected_keywords.append('BSEG')
                self.sap_type = 'SAP ECC'
                print('SAP ECC Detected.')
                return
            
            elif 'ACDOCA' in sap_name:
                self.selected_keywords.append('ACDOCA')
                self.sap_type = 'SAP S/4HANA'
                print('SAP S/4HANA Detected.')
                return
        
        self.sap_type = 'Not Detected'
        print('No SAP Version Detected!')
        print('Proceeding to unzip the remaining files...')


    #checks the trial balance files, if there is both, unzips the biggest one
    def trial_balance_files(self):
        glt0 = None
        fagflext = None

        for balance_file in self.root_path.rglob('*zip'):
            sap_balance = balance_file.stem.upper()

            if 'GLT0' in sap_balance:
                glt0 = balance_file
            
            elif 'FAGFLEXT' in sap_balance:
                fagflext = balance_file
        
        #if both files, take the biggest one
        if glt0 and fagflext:
            if glt0.stat().st_size > fagflext.stat().st_size:
                bigger_balance_file = 'GLT0'
            else:
                bigger_balance_file = 'FAGFLEXT'

            print(f'\nBoth GLT0 and FAGFLEXT files found. Unzipping... {bigger_balance_file}\n')
            self.selected_keywords.append(bigger_balance_file)
            self.trial_balance = bigger_balance_file

        elif glt0:
            self.selected_keywords.append('GLT0')
            self.trial_balance = 'GLT0'
        
        elif fagflext:
            self.selected_keywords.append('FAGFLEXT')
            self.trial_balance = 'FAGFLEXT'
        
        else:
            self.trial_balance = 'Not Detected'
            print('No GLT0 or FAGFLEXT files were found.')
            print('Proceeding to unzip the remaining files...')

    #get the remaining keywords from the list
    def remaining_keywords(self):
        for keyword in self.keywords:
            if keyword not in ['BSEG', 'ACDOCA', 'GLT0', 'FAGFLEXT']:
                self.selected_keywords.append(keyword)

    
    def unzip_selected_keywords(self):
        log = UnzipLog(self.root_path, self.output_dir, self.sap_type, self.trial_balance)

        unzipped_files = set()

        for zipped_file in self.root_path.rglob('*.zip'):
            files_to_unzip = zipped_file.stem.upper()

            #unzip and pass the files to a set
            for keyword in self.selected_keywords:
                if keyword in files_to_unzip and zipped_file not in unzipped_files:
                    print(f'Unzipping... {zipped_file.name}')
                    self.unzip_files(zipped_file, log)#unzip the file and pass the log
                    unzipped_files.add(zipped_file)#add the file to the set
                    break#avoid unzipping the same file twice
        
        log.generate_log_file()
    
    def unzip_files(self, zip_path: Path, log):
        unzipped_files = []

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file in zip_ref.infolist():

                    #ignore directories - all files must be in the same folder
                    if file.is_dir():
                        continue
                    
                    #get only .txt files
                    if not file.filename.lower().endswith('.txt'):
                        continue

                    #get the file name
                    filename = Path(file.filename).name
                    unzip_path = self.output_dir / filename

                    #unzip and write the file into the unzip folder
                    with zip_ref.open(file) as source, open(unzip_path, 'wb') as target:
                        target.write(source.read())

                    unzipped_files.append(filename)

                print(f'{zip_path.name} was successfully unzipped!\n')
                log.add_unzipped_files(zip_path.name, unzipped_files)

        #handle unreadable zip files
        except zipfile.BadZipFile:
            print(f'The file {zip_path.name} is corrupted or unreadable.')
            log.add_error(zip_path.name, 'is corrupted or unreadable.')