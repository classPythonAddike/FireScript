from parser.lexer.readers import StringReader


def test_filereader():
    reader = StringReader("Hello!\n1234")

    reader.advance_pointer()

    for _ in range(4):
        reader.advance_pointer()
    assert (
        reader.current_line() == "Hello!"
    ), "Didn't get expected line from file reader!"

    for _ in range(4):
        reader.advance_pointer()
    assert reader.current_line() == "1234", "Didn't get expected line from file reader!"
