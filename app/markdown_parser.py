#
# markdown_parser.py
#

import re

def parse_full_markdown(markdown):
    # Replace headers
    parsed_text = re.sub(r"^# (.+)\n", lambda x: "<p class='md_header'>" + x.group(1) + "</p>", markdown)

    return parse_light_markdown(parsed_text)


def parse_light_markdown(markdown):
    # Replace newlines
    parsed_text = markdown.replace("\n", "<br>")

    # Embolden
    parsed_text = re.sub(r"\*\*(.+)\*\*", lambda x: "<b>" + x.group(1) + "</b>", parsed_text)
    parsed_text = re.sub(r"__(.+)__", lambda x: "<i>" + x.group(1) + "</i>", parsed_text)

    # Italicize
    parsed_text = re.sub(r"\*(.+)\*", lambda x: "<i>" + x.group(1) + "</i>", parsed_text)
    parsed_text = re.sub(r"_(.+)_", lambda x: "<i>" + x.group(1) + "</i>", parsed_text)

    # Replace urls
    parsed_text = re.sub(r"\[(.+?)\]\+\((.+?)\)", lambda x: f"<a target='_blank' rel='noopener' href=\"" + x.group(2) + "\">" + x.group(1) + "</a>", parsed_text)
    parsed_text = re.sub(r"\[(.+?)\]\((.+?)\)", lambda x: f"<a rel='noopener' href=\"" + x.group(2) + "\">" + x.group(1) + "</a>", parsed_text)

    return parsed_text
