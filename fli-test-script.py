from writer import create_fli_file
from reader import read_fli_file

# file paths
output_file = "test_output.fli"
example_file = "ex-file"
file_id= "WS-20251002-001"
airline_id = "WS"

# create fli file with sample records
create_fli_file(output_file, file_id, airline_id, )