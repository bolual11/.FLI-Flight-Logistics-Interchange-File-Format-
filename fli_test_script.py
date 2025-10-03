import os
from fli_writer import create_fli_file
from fli_reader import read_fli_file

# file paths
output_file = "test.fli"
example_file = "ex-file.txt"
file_id= "WS-20251002-001"
airline_id = "WS"

# load data from example file
def load_example_data(file_path: str):
    try:
        # read ex file and parse records
        with open(file_path, 'r') as f:
            content = f.read()

        header_start = content.find("--BEGIN FLI HEADER--") + len("--BEGIN FLI HEADER--")
        header_end = content.find("--END FLI HEADER--")
        header = content[header_start:header_end].strip()

        body_start = content.find("--BEGIN FLI BODY--") + len("--BEGIN FLI BODY--")
        body_end = content.find("--END FLI BODY--")
        body = content[body_start:body_end].strip()

        footer_start = content.find("--BEGIN FLI FOOTER--") + len("--BEGIN FLI FOOTER--")
        footer_end = content.find("--END FLI FOOTER--")
        footer = content[footer_start:footer_end].strip()

        # return parsed sections - dictionary
        return {
            "header": header,
            "body": body,
            "footer": footer
        }
    except Exception as e: # error handling
        print(f"Error loading example data: {e}")
        return None
    
# parse body to records
def parse_body_to_records(body: str):
    records = []
    # split body with "---" markers
    record_blocks = body.split("\n---\n")

    for block in record_blocks:
        record = {}
        # split each block into lines/pairs
        lines = block.strip().split("\n")
        for line in lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                record[key.strip()] = value.strip()
        if record:
            records.append(record)
    return records

# create and write fli file
def test_writer(records):
    create_fli_file(output_file, file_id, airline_id, records)
    print(f"FLI file '{output_file}' created successfully.")

# read and verify fli file
def test_reader():
    result = read_fli_file(output_file)
    if result is not None:
        print("FLI file read successfully. Sections:")
        print("Header:", result["header"])
        print("Body:", result["body"])
        print("Footer:", result["footer"])

    else:
        print("Failed to read FLI file.")

# run tests
def run_tests():
    # load example data
    fli_data = load_example_data(example_file)

    if fli_data: # create records from body
        records = parse_body_to_records(fli_data["body"])
        # write fli file
        test_writer(records) 
        # read and verify fli file
        test_reader()