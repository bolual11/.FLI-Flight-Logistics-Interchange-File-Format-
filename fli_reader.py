import os
import base64
import bz2
from typing import Dict,List

BODY_BEGIN = "--BEGIN FLI BODY--"
BODY_END   = "--END FLI BODY--"

def parse_records_from_body(plain_text):
        records = []
        # split body with "---" markers
        
        # record_blocks = body.split("\n---\n")
        for block in plain_text.split("\n---\n"):
            rec = {}
            # split each block into lines/pairs
            lines = block.strip().split("\n")
            for line in lines:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    rec[key.strip()] = value.strip()
            if rec:
                records.append(rec)
        return records

# function to read and parse FLI file
"""old function
    try:
        with open(file_path, 'r') as file:
            fli_file = file.read()
        # extract each section
        header_start = fli_file.find("--BEGIN FLI HEADER--")
        header_end = fli_file.find("--END FLI HEADER--") + len("--END FLI HEADER")
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
        """
# updated function
def read_fli_file(file_path):
    try:
        data = open(file_path, "r", encoding="utf-8").read()

        # cut out each section, split into chunks
        header = data.split("--BEGIN FLI HEADER--")[1].split("--END FLI HEADER--")[0].strip()
        body_b64 = data.split("--BEGIN FLI BODY--")[1].split("--END FLI BODY--")[0].strip()
        footer = data.split("--BEGIN FLI FOOTER--")[1].split("--END FLI FOOTER--")[0].strip()

        # decode body: base64>bz2>text
        plain = bz2.decompress(base64.b64decode(body_b64)).decode("utf-8")

        # turn plain text into record dicts
        records = parse_records_from_body(plain)

        return {"header": header, "body_text": plain, "records": records, "footer": footer}
    except Exception as e:
        print("Error reading FLI file:", e)
        return None
        
