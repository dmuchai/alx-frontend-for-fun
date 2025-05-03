#!/usr/bin/python3
"""
markdown2html.py: A script to convert Markdown files to HTML.

This script takes two arguments: the input Markdown file path and the output
HTML file path. It supports converting headings, unordered lists, ordered lists,
paragraphs, bold text, emphasis text, MD5 hashing, and 'c'/'C' removal based
on specific Markdown syntax.
"""

import sys
import os.path
import re
import hashlib

def convert_inline_formatting(line):
    """
    Applies inline formatting rules (bold, emphasis, MD5, remove 'c').

    Args:
        line (str): A line of text potentially containing inline Markdown.

    Returns:
        str: The line with inline Markdown converted to HTML or processed.
    """
    # Bold (**...**) -> <b>...</b>
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    # Emphasis (__...__) -> <em>...</em>
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
    # MD5 ([[...]]) -> hash
    md5_matches = re.findall(r'\[\[(.*?)\]\]', line)
    if md5_matches:
        for match in md5_matches:
            hashed = hashlib.md5(match.encode('utf-8')).hexdigest()
            line = line.replace(f'[[{match}]]', hashed)
    # Remove c/C ((...)) -> ... (without c/C)
    remove_c_matches = re.findall(r'\(\((.*?)\)\)', line)
    if remove_c_matches:
        for match in remove_c_matches:
            processed = re.sub(r'[cC]', '', match)
            line = line.replace(f'(({match}))', processed)

    return line

def process_markdown_file(input_file, output_file):
    """
    Reads the Markdown file, processes it, and writes the HTML output.

    Args:
        input_file (str): Path to the input Markdown file.
        output_file (str): Path to the output HTML file.
    """
    html_lines = []
    in_ul = False
    in_ol = False
    in_p = False
    paragraph_buffer = []

    with open(input_file, 'r') as md_file:
        for line in md_file:
            stripped_line = line.strip()

            # Close previous lists/paragraphs if necessary
            # Check for new list/heading before closing paragraph
            is_heading = re.match(r'^#+ ', stripped_line)
            is_ul_item = stripped_line.startswith('- ')
            is_ol_item = stripped_line.startswith('* ')

            # Close paragraph if current line isn't part of it or is blank
            if in_p and (is_heading or is_ul_item or is_ol_item or not stripped_line):
                if paragraph_buffer:
                     # Apply inline formatting before joining
                    processed_buffer = [convert_inline_formatting(p_line) for p_line in paragraph_buffer]
                    html_lines.append("<p>\n" + "<br/>\n".join(processed_buffer) + "\n</p>\n")
                paragraph_buffer = []
                in_p = False

            # Close UL if the current line is not a UL item
            if in_ul and not is_ul_item:
                html_lines.append("</ul>\n")
                in_ul = False

            # Close OL if the current line is not an OL item
            if in_ol and not is_ol_item:
                html_lines.append("</ol>\n")
                in_ol = False

            # --- Process Current Line ---

            # Headings (Task 1)
            if is_heading:
                level = len(stripped_line.split(' ')[0])
                content = stripped_line[level + 1:]
                # Apply inline formatting to heading content
                content = convert_inline_formatting(content)
                html_lines.append(f"<h{level}>{content}</h{level}>\n")
                continue # Move to next line after processing heading

            # Unordered List (Task 2)
            if is_ul_item:
                if not in_ul:
                    html_lines.append("<ul>\n")
                    in_ul = True
                content = stripped_line[2:]
                 # Apply inline formatting to list item content
                content = convert_inline_formatting(content)
                html_lines.append(f"<li>{content}</li>\n")
                continue # Move to next line

            # Ordered List (Task 3)
            if is_ol_item:
                if not in_ol:
                    html_lines.append("<ol>\n")
                    in_ol = True
                content = stripped_line[2:]
                 # Apply inline formatting to list item content
                content = convert_inline_formatting(content)
                html_lines.append(f"<li>{content}</li>\n")
                continue # Move to next line

            # Paragraphs (Task 4, 5, 6)
            if stripped_line: # Line is not blank, not heading, not list item
                if not in_p:
                    in_p = True
                # Add raw line (without newline) to buffer. Formatting happens when closing <p>
                paragraph_buffer.append(line.rstrip('\n'))
            # else: # Blank line, paragraph boundary handled above

        # --- End of File Cleanup ---
        # Close any open lists or paragraphs
        if in_ul:
            html_lines.append("</ul>\n")
        if in_ol:
            html_lines.append("</ol>\n")
        if in_p and paragraph_buffer:
             # Apply inline formatting before joining
            processed_buffer = [convert_inline_formatting(p_line) for p_line in paragraph_buffer]
            html_lines.append("<p>\n" + "<br/>\n".join(processed_buffer) + "\n</p>\n")


    # Write the generated HTML to the output file
    with open(output_file, 'w') as html_file:
        html_file.writelines(html_lines)


if __name__ == "__main__":
    # Check command-line arguments (Task 0)
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if Markdown file exists (Task 0)
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Process the file
    process_markdown_file(input_file, output_file)

    # Exit successfully (Task 0)
    sys.exit(0)
