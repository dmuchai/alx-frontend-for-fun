#!/usr/bin/python3
"""
Markdown to HTML converter - Task 1: Headings
"""

import sys
import os
import re

def convert_line(line):
    """Convert a Markdown heading to HTML if it's a heading."""
    match = re.match(r'^(#{1,6}) (.+)', line)
    if match:
        hashes, content = match.groups()
        level = len(hashes)
        return f"<h{level}>{content.strip()}</h{level}>\n"
    return None

def main():
    # Check arguments
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if file exists
    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        exit(1)

    # Convert and write output
    with open(input_file, 'r') as md_file, open(output_file, 'w') as html_file:
        for line in md_file:
            stripped = line.strip()
            if not stripped:
                continue
            html = convert_line(stripped)
            if html:
                html_file.write(html)

    exit(0)

if __name__ == "__main__":
    main()
