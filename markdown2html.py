#!/usr/bin/python3
"""
Markdown to HTML converter - Task 0
"""

import sys
import os

def main():
    # Check argument count
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if markdown file exists
    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        exit(1)

    # Nothing else to do for Task 0
    exit(0)

if __name__ == "__main__":
    main()
