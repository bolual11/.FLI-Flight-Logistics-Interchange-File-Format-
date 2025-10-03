# AI Was used to generate ideas and give suggestions for this code.
# Use will be cited

# https://cdn.nakamotoinstitute.org/docs/taoup.pdf

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
                    key, value = line.split(": ", 1) # AI suggested using maxsplit=1
                    rec[key.strip()] = value.strip()
            if rec:
                records.append(rec)
        return records

# function to read and parse FLI file

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

if __name__ == "__main__": # AI gave me the layout for this
    result = read_fli_file("test.fli")

    if result:
        print("\n--- HEADER ---")
        print(result["header"])

        print("\n--- DECODED BODY ---")
        print(result["body_text"])

        print("\n--- FOOTER ---")
        print(result["footer"])

        # export everything to a text file
        with open("decoded_fli.txt", "w", encoding="utf-8") as f:
            f.write("--- HEADER ---\n")
            #f.write(result["header"] + "\n\n")
            f.write("--- DECODED BODY ---\n")
            #f.write(result["body_text"] + "\n\n")
            f.write("--- FOOTER ---\n")
            #f.write(result["footer"])
        print("\nAll decoded content (header, body, footer) saved to 'decoded_fli.txt'")
    else:
        print("Could not read test.fli")