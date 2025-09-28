import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict

# header, body, footer separators 

HEADER_BEGIN = "--BEGIN FLI HEADER"
HEADER_END = "--END FLI HEADER"
BODY_BEGIN = "--BEGIN FLI BODY--"
BODY_END = "--END FLI BODY--"
FOOTER_BEGIN = "--BEGIN FLI FOOTER--"
FOOTER_END = "--END FLI FOOTER--"

# order of contents in each record of the body

record_order = [
    "record_id",
    "flight_id,"
    "tail_id",
    "origin_code",
    "destination_code",
    "utc",
]

# function to get the time for utc

def get_utc_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# header
def create_header(file_id: str, airline_id: str) -> str:
    utc_time = get_utc_time()
    header = f"""{HEADER_BEGIN}
file_version
file_id: {file_id}
created_at
producer_airline
encoding:
header_charset
compression: bzip2
{HEADER_END}"""
    return header

# body
def create_body(records: List[Dict]) -> str:
    body = BODY_BEGIN + "\n"
    for record in records:
        record_line = ",".join(str(record.get(field, "")) for field in record_order)
        body += record_line + "\n"
    body += BODY_END
    return body

# footer
def create_footer(body: str) -> str:
    body_hash = hashlib.sha256(body.encode()).hexdigest()
    footer = f"""{FOOTER_BEGIN}
record_count: len(records)
body_hash: {body_hash}
hash_algorithm: sha256
compression: bzip2
{FOOTER_END}"""
    return footer

# main function to create the FLI file
def create_fli_file(file_path: str, file_id: str, airline_id: str, records: List[Dict]):
    header = create_header(file_id, airline_id)
    body = create_body(records)
    footer = create_footer(body)

    #  this combines all parts
    fli_data = "\n".join([header, body, footer])
    
    # write to file
    with open(file_path, "w") as f:
        f.write(fli_data)