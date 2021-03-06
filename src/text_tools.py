import csv
import re

def is_digit_with_punctuation(s):
    return re.match('^\d+(?:-\d)*[!.?,\']{1,}$',s) is not None
def move_digits_to_end(s):
    for c in s:
        if not c.isdigit() and not c == '-':
            break
        s = s[1:len(s)]+c
    return s
def rearrange_multiple_lines(caption,max_chars,total_chars):
    array = caption.split()
    counter = 0
    lines = []
    lineCounter = 1
    currentLine = ""
    for word in array:
        parts = list(move_digits_to_end(s) if is_digit_with_punctuation(s)
                     else s if s.isdigit() or re.match('(^\d+(?:-\d)*[!.?,\']{0,}$)|(<[a-zA-Z0-9:,]*>{1})',s)
                        else s[::-1] for s in re.split('(^\d+(?:-\d)*[!.?,\']{0,}$)|(<[a-zA-Z0-9:,]*>{1})', word) if s is not None )
        word = ''.join(parts)
#        word = re.sub("(<[a-zA-Z0-9:,]*>)","",word)
        counter += len(re.sub("(<[a-zA-Z0-9:,]*>)","",word)) +1
        if counter/max_chars >= 1:
            lineCounter += 1
            lines.append(currentLine)
            currentLine = ""
            counter = 0
        currentLine = word + " " + currentLine
    lines.append(currentLine)
    result = ""
    for line in lines:
        fill = 	""
        if total_chars is not None:
            fill_count = total_chars - len(line)
            fill = "".zfill(fill_count).replace("0", " ")
        result += fill   + line + "<cr>"
    return result
def rearrange_single_line(s):
    return s[::-1]

# converts translation into a numbered dictionary
def read_translation_from_csv(csv_path):
    translated_lines = {}
    with open(csv_path, encoding="utf-8-sig") as csvfile:

        csvreader = csv.DictReader(csvfile)
        for line in csvreader:
            translated = line['actual translation']
            not_reversed = line.get('not reversed')
            if not translated and not not_reversed:
                continue
            translated_lines[line['number']] = line
    return translated_lines

def translate(source,dest,translated_lines,multi_line,max_chars_before_break,total_chars_in_line,source_encoding):
    i = 0
    with open(source,
              encoding=source_encoding, errors="ignore") as source_file, \
            open(dest, "w",
                 encoding="utf-16") as dest_file:

        for l in source_file:
            i += 1
            translatedLine = translated_lines.get(str(i))
            if translatedLine is not None:
                orig = translatedLine['original']
                translated = translatedLine.get('actual translation')
                not_reversed = translatedLine.get('not reversed')
                if orig in l:
                    if not_reversed:
                        l = l.replace(orig, not_reversed)
                    else:
                        if multi_line:
                            new_line = rearrange_multiple_lines(translated,max_chars_before_break,total_chars_in_line)
                        else:
                            new_line = rearrange_single_line(translated)
                        l = l.replace(orig, new_line)
                        if total_chars_in_line is not None and total_chars_in_line > 0:
                            l = l.replace("<I>", "")
                    print(l)
            dest_file.write(l)

