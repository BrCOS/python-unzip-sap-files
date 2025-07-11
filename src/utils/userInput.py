from pathlib import  Path

def userInput():
    while True:
        
        zipped_file = str(input('Paste the path to the zipped file: ')).strip().strip('"')#allow copy as path

        #check if input is empty
        if not zipped_file:
            print('Please enter a valid file path.')
            continue

        #check if Path exists
        if not Path(zipped_file).exists():
            print('The path does not exist or the file was not found.')
            continue

        #check if the Path is a valid zip file
        if not Path(zipped_file).is_file() or Path(zipped_file).suffix.lower() != '.zip':
            print('Only .zip files are allowed!')
            continue

        return Path(zipped_file)