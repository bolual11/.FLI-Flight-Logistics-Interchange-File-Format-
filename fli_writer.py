# AI Was used to generate ideas and give suggestions for this code.
# Use will be cited

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict
import bz2
import base64

# header, body, footer separators 

HEADER_BEGIN = "--BEGIN FLI HEADER--"
HEADER_END = "--END FLI HEADER--"
BODY_BEGIN = "--BEGIN FLI BODY--"
BODY_END = "--END FLI BODY--"
FOOTER_BEGIN = "--BEGIN FLI FOOTER--"
FOOTER_END = "--END FLI FOOTER--"

# order of contents in each record of the body

record_order = [
    "record_id",
    "flight_id",
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
file_version: 1.0
file_id: {file_id}
created_at: {utc_time}
producer_airline: {airline_id}
encoding: base64
header_charset: UTF-8
compression: bzip2
{HEADER_END}"""
    return header

# body
def create_body(records: List[Dict]) -> str:
    # build body key:value pairs, records split with "---" separator
    blocks = []
    for i in records:
        lines = [
            f"record_id: {i.get('record_id','')}",
            f"flight_id: {i.get('flight_id','')}",
            f"tail_id: {i.get('tail_id','')}",
            f"origin_code: {i.get('origin_code','')}",
            f"destination_code: {i.get('destination_code','')}",
            f"utc: {i.get('utc','')}",
        ]
        blocks.append("\n".join(lines)) # AI told me to join these with \n
    plain = ("\n---\n".join(blocks) + "\n").encode("utf-8")

    # compress then encode with base64
    compressed = bz2.compress(plain)
    payload_b64 = base64.b64encode(compressed).decode("ascii")

    # write between markers
    return f"{BODY_BEGIN}\n{payload_b64}\n{BODY_END}"

# footer
# https://docs.python.org/3/library/hashlib.html for hashlib
def create_footer(body: str, records: List[Dict]) -> str:
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return f"""{FOOTER_BEGIN}
record_count: {len(records)}
body_hash: {body_hash}
hash_algorithm: sha256
compression: bzip2
{FOOTER_END}"""

# main function to create the FLI file
def create_fli_file(file_path: str, file_id: str, airline_id: str, records: List[Dict]):
    header = create_header(file_id, airline_id)
    body = create_body(records)
    footer = create_footer(body, records)

    #  this combines all parts
    fli_data = f"{header}\n{body}\n{footer}"

    # write to file
    with open(file_path, "w") as f:
        f.write(fli_data)

def compress_fli_body(body: str):
    # https://docs.python.org/3/library/base64.html for base64
    # https://docs.python.org/3/library/bz2.html for bz2
    # first compress then encode with base64
    compressed = bz2.compress(body.encode())
    return base64.b64encode(compressed).decode() 