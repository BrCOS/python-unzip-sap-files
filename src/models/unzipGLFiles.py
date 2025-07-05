import zipfile
from pathlib import Path
from src.utils.keywords import KEYWORDS

class UnzipSAPFiles:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.output_dir = root_path / 'unzip'
        self.output_dir.mkdir(exist_ok=True)
        self.keywords = [keyword.upper() for keyword in KEYWORDS]
        self.selected_keywords = []

    def sap_version(self):
        for ledger_file in self.root_path.rglob('*zip'):
            sap_name = ledger_file.stem.upper()

            if 'BSEG' in sap_name:
                self.selected_keywords.append('BSEG')
                print('SAP ECC Detected.')
                return
            
            elif 'ACDOCA' in sap_name:
                self.selected_keywords.append('ACDOCA')
                print('SAP S/4HANA Detected.')
                return
            
        print('No SAP Version Detected!')
        print('Proceeding to unzip the remaining files...')


    def trial_balance_files(self):
        glt0 = None
        fagflext = None

        for balance_file in self.root_path.rglob('*zip'):
            sap_balance = balance_file.stem.upper()

            if 'GLT0' in sap_balance:
                glt0 = balance_file
            
            elif 'FAGFLEXT' in sap_balance:
                fagflext = balance_file
        
        if glt0 and fagflext:
            bigger_balance_file = 'GLT0' if glt0.stat().st_size >= fagflext.stat().st_size else 'FAGFLEXT'
            print(f'\nBoth GLT0 and FAGFLEXT files found. Unzipping... {bigger_balance_file}\n')
            self.selected_keywords.append(bigger_balance_file)

        elif glt0:
            self.selected_keywords.append('GLT0')
        
        elif fagflext:
            self.selected_keywords.append('FAGFLEXT')
        
        else:
            print('No GLT0 or FAGFLEXT files were found.')
            print('Proceeding to unzip the remaining files...')

    
    def remaining_keywords(self):
        for keyword in self.keywords:
            if keyword not in ['BSEG', 'ACDOCA', 'GLT0', 'FAGFLEXT']:
                self.selected_keywords.append(keyword)

    
    def unzip_selected_keywords(self):
        unzipped_files = set()

        for zipped_file in self.root_path.rglob('*.zip'):
            files_to_unzip = zipped_file.stem.upper()

            for keyword in self.selected_keywords:
                if keyword in files_to_unzip and zipped_file not in unzipped_files:
                    print(f'Unzipping... {zipped_file.name}')
                    self.unzip_files(zipped_file)
                    unzipped_files.add(zipped_file)
                    break

    
    def unzip_files(self, zip_path: Path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file in zip_ref.infolist():
                    if file.is_dir():
                        continue

                    if not file.filename.lower().endswith('.txt'):
                        continue

                    filename = Path(file.filename).name
                    unzip_path = self.output_dir / filename

                    with zip_ref.open(file) as source, open(unzip_path, 'wb') as target:
                        target.write(source.read())

                print(f'{zip_path.name} was successfully unzipped!\n')
            
        except zipfile.BadZipFile:
            print(f'The file {zip_path.name} is corrupted or unreadable.')