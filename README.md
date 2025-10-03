**Overview**

The Flight Logistics Interchange (FLI) file format is a universal and portable file format designed to store and transfer aviation-related information (such as flight details, origin/destination, and flight status) between airlines and airports. Some key features of the FLI format include integrity checks with checksum validation (SHA-256), security through optional encryption (AES-256) for more sensitive data, and compression using bzip2 for efficient storage. The format is easy to search with built-in indexing, allowing quick access to specific flight records without having to rewrite the entire file. Additionally, the format’s structured headers, body, and footer sections ensure clear metadata organization, while the footer tracks the integrity of the file, and a summary of the file contents. The design of the file format allows for simple record updates, easy indexing of entries, and ensures data integrity across systems, making it both scalable and reliable for use in aviation.


I opted not to contain sensitive data, meaning I need only encode using SHA-256. While this is not AES, it still fits the description from our presentation, and it is still an encryption. I compressed the file with bzip2, then encoded it using base64, before using SHA-256.

-----------

**Run:**

To run this read/write program, first unzip the files and make sure all 5 files are present. Since the zipped file includes example files, you need to run the 'fli_test_script.py' file. This will generate the final product named 'test.fli', which is the FLI file.

To only run 'fli_reader' after creating a test file, run 'python fli_reader.py' in the terminal. You will now see the full contents of the FLI file in a different file called 'decoded_fli.txt'.

Lookup works in the terminal. You will see a prompt after running 'fli_test_script.py'.

To switch to a different example file, edit the "example_file" on line 8 of the 'fle_test_script.py' file.
