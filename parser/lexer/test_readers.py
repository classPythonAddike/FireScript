import os

from lexer.readers import FileReader

dummy_file = "code.txt"

def delete_file(file):
    os.remove(file)

def test_filereader():
    with open(dummy_file, "w") as f:
        f.write("Hello!\n1234")

    reader = FileReader(dummy_file)

    for _ in range(4): reader.advance_pointer()
    assert reader.current_line() == "Hello!", "Didn't get expected line from file reader!"

    for _ in range(4): reader.advance_pointer()
    assert reader.current_line() == "1234", "Didn't get expected line from file reader!"

    delete_file(dummy_file)
