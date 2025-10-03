import os
from typing import Dict,List

def parse_records_from_body(body: str) -> List[Dict]:
        records = []
        # split body with "---" markers
        record_blocks = body.split("\n---\n")

        for block in record_blocks:
            record = {}
            # split each block into lines/pairs
            lines =block.strip().split("\n")
            for line in lines:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    record[key.strip()] = value.strip()
            if record:
                records.append(record)

# function to read and parse FLI file
def read_fli_file(file_path):
    try:
        with open(file_path, 'r') as file:
            fli_file = file.read()
        # extract each section
        header_start = fli_file.find("--BEGIN FLI HEADER")
        header_end = fli_file.find("--END FLI HEADER") + len("--END FLI HEADER")
        # slice header
        header = fli_file[header_start:header_end].strip()


        body_start = fli_file.find("--BEGIN FLI BODY--")
        body_end = fli_file.find("--END FLI BODY--") + len("--END FLI BODY--")
        # slice body
        body = fli_file[body_start:body_end].strip()

        # extract footer
        footer_start = fli_file.find("--BEGIN FLI FOOTER--")
        footer_end = fli_file.find("--END FLI FOOTER--") + len("--END FLI FOOTER--")
        # slice footer
        footer = fli_file[footer_start:footer_end].strip()

        # check if any section is missing
        if -1 in [header_start, header_end, body_start, body_end, footer_start, footer_end]:
            raise ValueError("FLI file is missing one or more sections")
        
        # return sections as dictionary
        records = parse_records_from_body(body)
    

        return {
            "header": header,
            "body": body,
            "footer": footer
        }
    except ValueError as e: # specific error handling
        print(f"Error reading FLI file: {e}")
        return None
    
        
