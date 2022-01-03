from compiler.lexer.readers import StringReader


def test_filereader():
    lines = [
        "123",
        "Hello",
        "",
        ""
    ]
    reader = StringReader("\n".join(lines))
    reader.advance_pointer()
    
    for i in range(len(lines[0]) - 1):
        assert reader.current_line() == lines[0], "Got wrong line!"
        assert reader.current_character() == lines[0][i], "Got wrong character!"
        assert reader.current_line_number() == 1, "Got wrong line number!"
        reader.advance_pointer()

    for line_no, line in enumerate(lines[1:]):
        assert reader.current_line() != line, "Got wrong line!"

        reader.advance_pointer()
        reader.advance_pointer()

        assert reader.current_line() == line, "Got wrong line!"
        assert reader.current_line_number() == line_no + 1, "Got wrong line number!"

        for i in range(len(line)):
            assert reader.current_character() == line[i], "Got wrong character!"
            reader.advance_pointer()

        assert reader.current_line() == line, "Got wrong line!"
        reader.retreat_pointer()
