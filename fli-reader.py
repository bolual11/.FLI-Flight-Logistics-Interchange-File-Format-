def read_fli_file(file_path):
    try:
        with open(file_path, 'r') as file:
            fli_file = file.read()
        # extract each section
        header_start = fli_file.find("--BEGIN FLI HEADER")
        header_end = fli_file.find("--END FLI HEADER") + len("--END FLI HEADER")
        body_start = fli_file.find("--BEGIN FLI BODY--")
        body_end = fli_file.find("--END FLI BODY--") + len("--END FLI BODY--")
        footer_start = fli_file.find("--BEGIN FLI FOOTER--")
        footer_end = fli_file.find("--END FLI FOOTER--") + len("--END FLI FOOTER--")
        
        # check if any section is missing
        if -1 in [header_start, header_end, body_start, body_end, footer_start, footer_end]:
            raise ValueError("FLI file is missing one or more sections")
        
        # slice out each part
        header = fli_file[header_start:header_end].strip()
        body = fli_file[body_start:body_end].strip()
        footer = fli_file[footer_start:footer_end].strip()

        return {
            "header": header,
            "body": body,
            "footer": footer
        }
    except ValueError as e: # specific error handling
        print(f"Error reading FLI file: {e}")
        return None