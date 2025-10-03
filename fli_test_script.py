import os
from typing import Dict, List
from fli_writer import create_fli_file
from fli_reader import read_fli_file

# file paths
output_file = "test.fli"
example_file = "ex_file.txt"
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
# using "str" to avoid crashing if record isn't a string 
def create_record_index(records: List[Dict]) -> Dict:
    # create index for fast lookup
    return {
        str(record.get("record_id")).strip(): record
        for record in records
        if "record_id" != None
    }

def get_record_by_id(record_id: str, index: Dict) -> Dict:
    # find record with record_id
    return index.get(str(record_id), None)

# create and write fli file
def test_writer(records):
    create_fli_file(output_file, file_id, airline_id, records)
    print(f"FLI file '{output_file}' created successfully.")

# read and verify fli file
def test_reader():
    result = read_fli_file(output_file)
    if result != None:
        print("FLI file read successfully.")
        '''print("Header:", result["header"])
        print("Body:", result["body_text"])
        print("Footer:", result["footer"])'''
        
        #create index and verify a record
        record_index = create_record_index(result["records"])
        record = get_record_by_id("1", record_index)
        if record:
            print("Record found")
        else:
            print("Record not found.")

    else:
        print("Failed to read FLI file.")

# run tests
def run_tests():
    print("Running FLI Writer and Reader Tests...")
    # load example data
    fli_data = load_example_data(example_file)

    if fli_data: # create records from body
        print("Loaded data successfully.")
        records = parse_body_to_records(fli_data["body"])
        # write fli file
        test_writer(records) 
        # read and verify fli file
        test_reader()
    else:
        print("Failed to load data.")
        
if __name__ == "__main__":
    run_tests()