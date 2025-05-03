#!/usr/bin/python3
"""
Markdown to HTML converter - Task 2: Unordered Lists
"""

import sys
import os
import re

def convert_line(line):
    """Convert headings or return line type and content."""
    heading_match = re.match(r'^(#{1,6}) (.+)', line)
    if heading_match:
        level = len(heading_match.group(1))
        content = heading_match.group(2).strip()
        return 'heading', f"<h{level}>{content}</h{level}>"

    list_match = re.match(r'^- (.+)', line)
    if list_match:
        return 'ul_item', list_match.group(1).strip()

    if line.strip() == "":
        return 'blank', None

    return 'text', line.strip()

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        exit(1)

    with open(input_file, 'r') as md_file, open(output_file, 'w') as html_file:
        in_list = False

        for line in md_file:
            line_type, content = convert_line(line)

            if line_type == 'heading':
                if in_list:
                    html_file.write("</ul>\n")
                    in_list = False
                html_file.write(content + "\n")

            elif line_type == 'ul_item':
                if not in_list:
                    html_file.write("<ul>\n")
                    in_list = True
                html_file.write(f"<li>{content}</li>\n")

            elif line_type == 'blank':
                if in_list:
                    html_file.write("</ul>\n")
                    in_list = False

            else:
                if in_list:
                    html_file.write("</ul>\n")
                    in_list = False
                # Placeholder for future paragraph handling

        if in_list:
            html_file.write("</ul>\n")

    exit(0)

if __name__ == "__main__":
    main()
