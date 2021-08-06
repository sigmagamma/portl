import csv

def rearrange_multiple_lines(s,max_chars):
    array = s.split()
    counter = 0
    lines = []
    lineCounter = 1
    currentLine = ""
    for word in array:
        word = word[::-1]
        counter += len(word) +1
        if counter/max_chars >= 1:
            lineCounter += 1
            lines.append(currentLine)
            currentLine = ""
            counter = 0
        currentLine = word + " " + currentLine
    lines.append(currentLine)
    result = ""
    for line in lines:
        fill_count = 59-len(line)
        fill = 	"".zfill(fill_count).replace("0", " ")
        result += fill   + line + "<cr>"
    return result
def rearrange_single_line(s):
    return s[::-1]

def read_translation_from_csv(csv_path):
    translated_lines = {}
    with open(csv_path, encoding="utf-8-sig") as csvfile:

        csvreader = csv.DictReader(csvfile)
        for line in csvreader:
            original = line['original']
            translation = line['actual translation']
            speaker = line['speaker']
            pair = [original, translation, speaker]
            if translation != "":
                translated_lines[line['number']] = pair
    return translated_lines

def translate(source,dest,translated_lines,multi_line):
    i = 0
    with open(source,
              encoding="utf-16", errors="ignore") as source_file, \
            open(dest, "w",
                 encoding="utf-16") as dest_file:

        for l in source_file:
            i += 1
            translatedLine = translated_lines.get(str(i))
            if translatedLine is not None:
                orig = translatedLine[0]
                translated = translatedLine[1]
                if orig in l:
                    if multi_line:
                        new_line = rearrange_multiple_lines(translated,50)
                    else:
                        new_line = rearrange_single_line(translated)
                    l = l.replace(orig, new_line).replace("<I>", "")
                    #print(l)
            dest_file.write(l)




