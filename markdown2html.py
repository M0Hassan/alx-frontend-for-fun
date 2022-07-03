#!/usr/bin/python3

"""
Markdown script using python.
"""
import sys
import os.path
import re
<<<<<<< HEAD
import hashlib
=======
from time import sleep


def h(line):
    """
    Creates a heading html element.
    <h1..6>...</h1..6}>
    """
    line = line.replace("\n", "")

    line = line.strip()
    parse_space = line.split(" ")

    level = parse_space[0].count("#")

    if (level > 6):
        return(line)

    # Removes closing symbols at end of line.
    if len(parse_space[-1]) == parse_space[-1].count("#"):
        parse_space = parse_space[0:-1]

    # Concatenates the content string.
    content = ""
    for word in parse_space[1:]:
        content += word + " "
    content = content[0:-1]

    return("<h{}>{}</h{}>".format(level, content, level))


def li(line, flags):
    """
    Creates a list item html element.
    <li>...</li>
    """
    line = line.replace("\n", "")
    line = line.strip()
    parse_space = line.split(" ")

    # Concatenates the content string.
    content = ""
    for word in parse_space[1:]:
        content += word + " "
    content = content[0:-1]
    content = "<li>{}</li>\n".format(content)

    # if "-s" in flags:
    #     content = " " + content

    return(content)


def clean_line(line):
    """
    Styling tags with the use of Regular expressions.
    <b>...<\b><em>...<\em>
    [[...]] = md5(...)
    ((...)) = ... with no 'C' or 'c' characters.
    """
    # Replace ** for <b> tags
    line = re.sub(r"\*\*(\S+)", r"<b>\1", line)
    line = re.sub(r"(\S+)\*\*", r"\1</b>", line)

    # Replace __ for <em> tags
    line = re.sub(r"\_\_(\S+)", r"<em>\1", line)
    line = re.sub(r"(\S+)\_\_", r"\1</em>", line)

    # Replace [[<content>]] for md5 hash of content.
    line = re.sub(r"\[\[(.*)\]\]", md5(r"\1".encode()).hexdigest(), line)

    # Replace ((<content>)) for no C characters on content.
    result = re.search(r"(\(\((.*)\)\))", line)
    if result is not None:
        content = result.group(2)
        content = re.sub("[cC]", "", content)
        line = re.sub(r"\(\((.*)\)\)", content, line)

    return(line)


def mark2html(*argv):
    """
    Main method to parse and process markdown to html.
    """
    inputFile = argv[1]
    ouputFile = argv[2]
    flags = argv[3:]

    with open(inputFile, "r") as f:
        markdown = f.readlines()

    html = []

    # Iterate over lines of the read file.
    index = 0
    while index < len(markdown):
        line = clean_line(markdown[index])

        # If Heading.
        if line[0] == "#":
            html.append(h(line))

        # If ordered or unordered list.
        elif line[0] == "-" or line[0] == "*":
            list_type = {"-": "ul", "*": "ol"}
            current_index = index
            ul_string = "<{}>\n".format(list_type[line[0]])
            while (current_index < len(markdown) and
                   markdown[current_index][0] in ["-", "*"]):
                ul_string += li(markdown[current_index], flags)
                current_index += 1
            index = current_index - 1  # Because while ends one after.
            ul_string += "</{}>\n".format(list_type[line[0]])
            html.append(ul_string)

        # If only a newline.
        elif line[0] == "\n":
            line = ""

        # Else there are no special characters at beggining of line.
        else:
            paragraph = "<p>\n"
            new_index = index

            while new_index < len(markdown):
                line = clean_line(markdown[new_index])
                if ((new_index + 1) < len(markdown) and
                        markdown[new_index + 1] is not None):
                    next_line = markdown[new_index + 1]
                else:
                    next_line = "\n"
                if "-s" in flags:
                    line = "    " + line
                paragraph += line.strip() + "\n"
                if next_line[0] in ["*", "#", "-", "\n"]:
                    index = new_index
                    break

                # If next line has no special characters.
                if next_line[0] not in ["#", "-", "\n"]:
                    if "-s" in flags:
                        br = r"        <br />"
                    else:
                        br = r"<br/>"
                    br += "\n"
                    paragraph += br

                new_index += 1

            paragraph += "</p>\n"

            html.append(paragraph)

        index += 1

    # Create html text string with corresponding newlines.
    text = ""
    for line in html:
        if "\n" not in line:
            line += "\n"
        text += line

    if "-v" in flags:
        print(text)

    # Write into <ouputFile> file.
    with open(ouputFile, "w") as f:
        f.write(text)

    exit(0)


def perror(*args, **kwargs):
    """
    Printing to STDERR file descriptor.
    """
    print(*args, file=stderr, **kwargs)


if __name__ == "__main__":
>>>>>>> d742f43859c66b01b954bcaebacc7eba6518b181

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

<<<<<<< HEAD
    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            unordered_start, ordered_start, paragraph = False, False, False
            # bold syntax
            for line in read:
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                # md5
                md5 = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(
                        md5_inside[0].encode()).hexdigest())

                # remove the letter C
                remove_letter_c = re.findall(r'\(\(.+?\)\)', line)
                remove_c_more = re.findall(r'\(\((.+?)\)\)', line)
                if remove_letter_c:
                    remove_c_more = ''.join(
                        c for c in remove_c_more[0] if c not in 'Cc')
                    line = line.replace(remove_letter_c[0], remove_c_more)

                length = len(line)
                headings = line.lstrip('#')
                heading_num = length - len(headings)
                unordered = line.lstrip('-')
                unordered_num = length - len(unordered)
                ordered = line.lstrip('*')
                ordered_num = length - len(ordered)
                # headings, lists
                if 1 <= heading_num <= 6:
                    line = '<h{}>'.format(
                        heading_num) + headings.strip() + '</h{}>\n'.format(
                        heading_num)

                if unordered_num:
                    if not unordered_start:
                        html.write('<ul>\n')
                        unordered_start = True
                    line = '<li>' + unordered.strip() + '</li>\n'
                if unordered_start and not unordered_num:
                    html.write('</ul>\n')
                    unordered_start = False

                if ordered_num:
                    if not ordered_start:
                        html.write('<ol>\n')
                        ordered_start = True
                    line = '<li>' + ordered.strip() + '</li>\n'
                if ordered_start and not ordered_num:
                    html.write('</ol>\n')
                    ordered_start = False

                if not (heading_num or unordered_start or ordered_start):
                    if not paragraph and length > 1:
                        html.write('<p>\n')
                        paragraph = True
                    elif length > 1:
                        html.write('<br/>\n')
                    elif paragraph:
                        html.write('</p>\n')
                        paragraph = False

                if length > 1:
                    html.write(line)

            if unordered_start:
                html.write('</ul>\n')
            if ordered_start:
                html.write('</ol>\n')
            if paragraph:
                html.write('</p>\n')
    exit (0)
=======
    mark2html(*argv)
>>>>>>> d742f43859c66b01b954bcaebacc7eba6518b181
