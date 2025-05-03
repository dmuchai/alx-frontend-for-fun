#!/usr/bin/python3
"""
Markdown to HTML converter
"""
import sys
import os
import re
import hashlib


def format_text(text):
    """Apply all transformations to text."""
    # MD5 conversion for [[text]]
    def md5_replacer(match):
        raw = match.group(1).lower()
        return hashlib.md5(raw.encode()).hexdigest()
    text = re.sub(r'\[\[(.+?)\]\]', md5_replacer, text)

    # Remove all 'c' and 'C' from ((text))
    def remove_c_replacer(match):
        return re.sub(r'[cC]', '', match.group(1))
    text = re.sub(r'\(\((.+?)\)\)', remove_c_replacer, text)

    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    # Emphasis
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)

    return text


def markdown_to_html(input_file, output_file):
    """Convert Markdown to HTML."""
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as out:
        in_ul = False
        in_ol = False
        in_p = False

        for line in lines:
            line = line.rstrip()

            # Skip empty line
            if not line:
                if in_p:
                    out.write('</p>\n')
                    in_p = False
                if in_ul:
                    out.write('</ul>\n')
                    in_ul = False
                if in_ol:
                    out.write('</ol>\n')
                    in_ol = False
                continue

            # Headings
            heading_match = re.match(r'^(#{1,6}) (.*)', line)
            if heading_match:
                if in_p:
                    out.write('</p>\n')
                    in_p = False
                if in_ul:
                    out.write('</ul>\n')
                    in_ul = False
                if in_ol:
                    out.write('</ol>\n')
                    in_ol = False
                level = len(heading_match.group(1))
                content = format_text(heading_match.group(2))
                out.write(f'<h{level}>{content}</h{level}>\n')
                continue

            # Unordered list
            if line.startswith('- '):
                if in_ol:
                    out.write('</ol>\n')
                    in_ol = False
                if not in_ul:
                    out.write('<ul>\n')
                    in_ul = True
                content = format_text(line[2:].strip())
                out.write(f'<li>{content}</li>\n')
                continue

            # Ordered list
            if line.startswith('* '):
                if in_ul:
                    out.write('</ul>\n')
                    in_ul = False
                if not in_ol:
                    out.write('<ol>\n')
                    in_ol = True
                content = format_text(line[2:].strip())
                out.write(f'<li>{content}</li>\n')
                continue

            # Paragraph
            content = format_text(line.strip())
            if not in_p:
                out.write('<p>\n')
                in_p = True
            else:
                out.write('<br/>\n')
            out.write(f'{content}\n')

        # Close open tags at EOF
        if in_p:
            out.write('</p>\n')
        if in_ul:
            out.write('</ul>\n')
        if in_ol:
            out.write('</ol>\n')


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    markdown_to_html(input_file, output_file)
    sys.exit(0)
