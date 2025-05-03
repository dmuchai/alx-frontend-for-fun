#!/usr/bin/python3
"""
markdown2html.py - Converts a Markdown file to HTML.
Supports: headings, paragraphs, unordered/ordered lists, bold, emphasis.
"""

import sys
import os
import re


def format_text(text):
    """Apply bold and emphasis formatting."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    return text


def parse_line(line):
    """Determine the type of line and return corresponding HTML."""
    line = line.rstrip()
    if not line:
        return 'blank', ''
    if line.startswith('#'):
        level = len(line) - len(line.lstrip('#'))
        content = line[level:].strip()
        return 'heading', f"<h{level}>{format_text(content)}</h{level}>"
    if line.startswith('- '):
        return 'ul', f"<li>{format_text(line[2:].strip())}</li>"
    if line.startswith('* '):
        return 'ol', f"<li>{format_text(line[2:].strip())}</li>"
    return 'text', format_text(line)


def convert_markdown(input_file, output_file):
    """Convert markdown content to HTML and write to output_file."""
    with open(input_file, 'r') as md_file:
        lines = md_file.readlines()

    html_lines = []
    in_ul = False
    in_ol = False
    in_paragraph = False
    paragraph_buffer = []

    for line in lines:
        line_type, content = parse_line(line)

        if line_type == 'blank':
            if in_paragraph:
                html_lines.append("<p>\n" + "<br/>\n".join(paragraph_buffer) + "\n</p>")
                paragraph_buffer = []
                in_paragraph = False
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            continue

        if line_type == 'heading':
            if in_paragraph:
                html_lines.append("<p>\n" + "<br/>\n".join(paragraph_buffer) + "\n</p>")
                paragraph_buffer = []
                in_paragraph = False
            html_lines.append(content)
        elif line_type == 'ul':
            if in_paragraph:
                html_lines.append("<p>\n" + "<br/>\n".join(paragraph_buffer) + "\n</p>")
                paragraph_buffer = []
                in_paragraph = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            html_lines.append(content)
        elif line_type == 'ol':
            if in_paragraph:
                html_lines.append("<p>\n" + "<br/>\n".join(paragraph_buffer) + "\n</p>")
                paragraph_buffer = []
                in_paragraph = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            html_lines.append(content)
        elif line_type == 'text':
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            in_paragraph = True
            paragraph_buffer.append(content)

    # Flush remaining open tags
    if in_paragraph:
        html_lines.append("<p>\n" + "<br/>\n".join(paragraph_buffer) + "\n</p>")
    if in_ul:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")

    with open(output_file, 'w') as html_file:
        for html in html_lines:
            html_file.write(html + '\n')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.isfile(input_path):
        sys.stderr.write(f"Missing {input_path}\n")
        sys.exit(1)

    convert_markdown(input_path, output_path)
    sys.exit(0)
