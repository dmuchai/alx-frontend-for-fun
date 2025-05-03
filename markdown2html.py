#!/usr/bin/python3
"""
Markdown to HTML converter - Task 4: Paragraph support
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

    return 'paragraph', line.rstrip()

def flush_paragraph(buffer, html_file):
    """Flush collected paragraph lines to output"""
    if not buffer:
        return
    html_file.write("<p>\n")
    html_file.write("<br/>\n".join(buffer) + "\n")
    html_file.write("</p>\n")

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
        paragraph_buffer = []

        for line in md_file:
            line_type, content = convert_line(line)

            if line_type != 'paragraph':
                flush_paragraph(paragraph_buffer, html_file)
                paragraph_buffer = []

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
                flush_paragraph(paragraph_buffer, html_file)
                paragraph_buffer = []
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False

            elif line_type == 'paragraph':
                paragraph_buffer.append(content)

        # Flush any remaining elements
        flush_paragraph(paragraph_buffer, html_file)
        if in_ul:
            html_file.write("</ul>\n")
        if in_ol:
            html_file.write("</ol>\n")

    exit(0)

if __name__ == "__main__":
    main()
