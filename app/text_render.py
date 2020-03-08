from flask import escape

def render_text_file(source, destination):
    with open(source, "r") as source_file:
        escaped_source_text = str(escape(source_file.read()))

    destination_text = escaped_source_text.replace("\n\n", "\n<br><br>\n")

    with open(destination, "w") as destination_file:
        destination_file.write(destination_text)
