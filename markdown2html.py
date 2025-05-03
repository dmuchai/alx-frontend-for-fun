#!/usr/bin/python3
"""
Markdown to HTML converter - Task 3: Ordered and Unordered Lists
"""

import sys
import os
import re

def convert_line(line):
    """Classify the line and return (type, content)"""
    heading_match = re.match(r'^(#{1,6}) (.+)', line)
    if heading_match:
        level = len(heading_match.group(1))
        content = heading_match.group(2).strip()
        return 'heading', f"<h{level}>{content}</h{level}>"

    unordered_match = re.match(r'^- (.+)', line)
    if unordered_match:
        return 'ul_item', unordered_match.group(1).strip()

    ordered_match = re.match(r'^\* (.+)', line)
    if ordered_match:
        return 'ol_item', ordered_match.group(1).strip()

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
        in_ul = False
        in_ol = False

        for line in md_file:
            line_type, content = convert_line(line)

            if line_type == 'heading':
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                html_file.write(content + "\n")

            elif line_type == 'ul_item':
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                if not in_ul:
                    html_file.write("<ul>\n")
                    in_ul = True
                html_file.write(f"<li>{content}</li>\n")

            elif line_type == 'ol_item':
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if not in_ol:
                    html_file.write("<ol>\n")
                    in_ol = True
                html_file.write(f"<li>{content}</li>\n")

            elif line_type == 'blank':
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False

            else:
                # Future paragraph or text support
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                html_file.write(content + "\n")

        # Close any open list at EOF
        if in_ul:
            html_file.write("</ul>\n")
        if in_ol:
            html_file.write("</ol>\n")

    exit(0)

if __name__ == "__main__":
    main()
