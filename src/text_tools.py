import csv
import re
import arabic_reshaper
from bidi.algorithm import get_display

# english and digits are written left to right, but punctuation is moved to comply
# with RTL language
def is_digit_or_english_with_punctuation(s):
    return re.match('^[\da-zA-Z\u0660-\u0669]+(?:-[\da-zA-Z\u0660-\u0669])*[!.?,،\'\]]{1,}$',s) is not None \
           or re.match('^[!.?,،\'\]]{1,}[\da-zA-Z\u0660-\u0669]+(?:-[\da-zA-Z\u0660-\u0669])*$',s) is not None \
           or re.match('^[!.?,،\'\]]{1,}[\da-zA-Z\u0660-\u0669]+(?:-[\da-zA-Z\u0660-\u0669])*[!.?,،\'\]]{1,}$',s) is not None

def rearrange_multiple_lines(caption,max_chars,total_chars,language,prefix="",seperator="<cr>",insert_newlines=True,end_with_space=True,basic_formatting=False,space_within_phrases=False):
    is_phrase = False
    if str(caption).startswith('\"') and str(caption).endswith('\"'):
        is_phrase = True
        if space_within_phrases:
            caption = caption.replace('"', '')
    if language == "uarabic":
        reshaped_text = arabic_reshaper.reshape(caption)
        array = reshaped_text.split()
    else:
        array = caption.split()
    counter = 0
    lines = []
    lineCounter = 1
    currentLine = ""
    lastColor = ""
    italic = False
    linePrefix = ""
    lineSuffix = ""
    for word in array:
        # fixing digits and punctuation
        if language == 'hebrew' and not is_phrase:
            word = word.replace('"', '״')
        shortword = re.sub("(<[a-zA-Z0-9:,.]*>)", "", word)
        if shortword != "" and word != seperator:
            if shortword != word:
                newshortword = get_display(shortword)
                word = word.replace(shortword, newshortword)
            elif is_digit_or_english_with_punctuation(word):
                word = 'א' + word + 'א'
                word = get_display(word)
                word = word.replace('א','')
            else:
                word = get_display(word)
            counter += len(shortword) + 1
        # italicize logic - we wrap each word in italic tags from the moment an italic appears until it doesn't
        if basic_formatting:
            if word == "<I>":
                continue
            word = word.replace("<I>", "")
        elif word == "<I>":
            italic = True
            continue
        elif re.match("(^<I>)",word):
            if italic:
                word = word.replace("<I>","")
                italic = False
            else:
                word = word + "<I>"
                italic = True
        elif re.match("(<I>$)",word):
            if italic:
                word = "<I>" + word
            else:
                word = word.replace("<I>","")
                italic = True
        else:
            if italic and re.sub("(<[a-zA-Z0-9:,.]*>)","",word) != "":
                word = "<I>" + word + "<I>"

        # colors logic - we prefix each word with the color tag until the next color tag
        colors =  re.findall("(<clr:[a-zA-Z0-9:,.]*>)",word)
        if colors != []:
            lastColor = colors[-1]
            if re.sub("(<clr:[a-zA-Z0-9:,.]*>)", "", word) == "":
                continue
        elif re.sub("(<[a-zA-Z0-9:,.]*>)","",word) != "":
            word = lastColor+word
        # delays and lens are force-pre/suffixed for now
        if re.match('<delay:[0-9.]*>',word):
            delay = re.findall("(<delay:[0-9.]*>)", word)[0]
            word = word.replace(delay,"")
            if not basic_formatting:
                linePrefix = delay + prefix + linePrefix
            lastColor  = ""
            italic = False
        elif re.match('<len:[0-9.]*>',word):
            len_text = re.findall("(<len:[0-9.]*>)", word)[0]
            word = word.replace(len_text, "")
            if not basic_formatting:
                lineSuffix = len_text + lineSuffix
        if word == "":
            continue
        counter_check = counter
        if not end_with_space:
            counter_check = counter_check - 1
        # we break when passing the limit or encountering a cr.
        # sometimes crs would be used to manually split problematic titles
        if (max_chars is not None and (counter_check)/max_chars) >= 1 or word == seperator:
            lineCounter += 1
            length = len(currentLine)
            if ((not end_with_space) and length != 0 and currentLine[-1] == " "):
                currentLine = currentLine[0:-1]
            if lineSuffix != "":
                lineSuffix = lineSuffix + " "
            currentLine = linePrefix + currentLine + lineSuffix
            lines.append(currentLine)
            linePrefix = ""
            lineSuffix = ""
            currentLine = ""
            counter = 0

        if word != seperator:
            currentLine = word + " " + currentLine
    length = len(currentLine)
    if ((not end_with_space) and length != 0 and currentLine[-1] == " "):
        currentLine = currentLine[0:-1]
    if lineSuffix != "":
        lineSuffix = lineSuffix + " "
    currentLine = linePrefix + currentLine + lineSuffix
    lines.append(currentLine)
    result = ""
    line_seperator = seperator if insert_newlines else ""
    for i,line in enumerate(lines):
        fill = 	""
        # spacing logic
        if total_chars is not None:
            line_no_tags= re.sub("(<[a-zA-Z0-9:,.]*>)","",line)
            fill_count = (total_chars - len(line_no_tags))
            fill = "".zfill(fill_count).replace("0", " ")
        result += fill   + line + line_seperator
    result = prefix + result
    if is_phrase and space_within_phrases:
        result = '"' + result + '"'
    return result

def rearrange_single_line(s):
    return s[::-1]

# converts translation into a numbered dictionary
def read_translation_from_csv(csv_path,gender,store):
    translated_lines = {}
    with open(csv_path, encoding="utf-8-sig") as csvfile:

        csvreader = csv.DictReader(csvfile)
        for line in csvreader:
            translated = line.get('actual translation')
            if (gender is not None and gender == 'f'):
                female_version = line.get('female version')
                if female_version:
                    line['actual translation'] = female_version
            not_reversed = line.get('not reversed')
            if not translated and not not_reversed:
                continue
            if store+"_number" in csvreader.fieldnames and line[store+"_number"]:
                line['number'] = line[store+"_number"]
            if line['number'] is not None:
                translated_lines[line['number']] = line
    return translated_lines

def translate(source, dest, translated_lines, is_captions, max_chars_before_break, total_chars_in_line, language, source_encoding, prefix="",insert_newlines=True, filters=None,basic_formatting=False,text_spacings=[]):
    i = 0
    dest_encoding = 'utf-16'
    if source_encoding == 'utf-8':
        dest_encoding = 'utf-8'
    with open(source,
              encoding=source_encoding, errors="ignore") as source_file, \
            open(dest, "w",
                 encoding=dest_encoding) as dest_file:
        j = 0
        upserts = []
        # Collecting possible upserts
        upsert_originals = set()
        while True:
            j = j+1
            upsert = translated_lines.get("upsert_"+str(j))
            if upsert:
                upserts.append(upsert)
                upsert_originals.add(upsert.get('original'))
            else:
                break
        for l in source_file:
            i += 1
            translatedLine = translated_lines.get(str(i))
            if translatedLine is not None:
                orig = translatedLine['original']
                translated = translatedLine.get('actual translation')
                not_reversed = translatedLine.get('not reversed')
                if translated == 'DELETE' or not_reversed == 'DELETE':
                    continue
                if orig in l:
                    if not_reversed:
                        l = l.replace(orig, not_reversed)
                        if filters:
                            for filter in filters:
                                l = l.replace(filter, "")
                    else:
                        if is_captions:
                            new_line = rearrange_multiple_lines(translated,max_chars_before_break,total_chars_in_line,language,prefix,insert_newlines=insert_newlines,end_with_space=True,basic_formatting=basic_formatting)
                        else:
                            spacing_style = translatedLine.get('spacing style')
                            max_chars_before_break = None
                            total_chars_in_line = None
                            space_within_phrases = False
                            if spacing_style is not None:
                                for spacing in text_spacings:
                                    if spacing.get('name') == spacing_style:
                                        max_chars_before_break = spacing.get('max_chars_before_break')
                                        total_chars_in_line = spacing.get('total_chars_in_line')
                                        space_within_phrases = True
                                        break
                            new_line = rearrange_multiple_lines(translated,max_chars_before_break,total_chars_in_line,language,"","\\n",insert_newlines=insert_newlines,end_with_space=False,basic_formatting=basic_formatting,space_within_phrases=space_within_phrases)
                        l = l.replace(orig, new_line)
                        if filters:
                            for filter in filters:
                                l = l.replace(filter, "")
                    print(l)
            else:
                # checking line against remaining upserts
                popped = None
                if l.strip() in upsert_originals:
                    while upserts:
                        upsert = upserts[0]
                        orig = upsert.get('original')
                        not_reversed = upsert.get('not reversed')
                        if orig == l.strip():
                            new_line = l.replace(orig,not_reversed)
                            dest_file.write(new_line)
                            popped = upserts.pop(0)
                            if upsert.get('multi') != 'TRUE':
                                break
                    if popped:
                        continue
            dest_file.write(l)
        # printing out remaining upserts
        for upsert in upserts:
            dest_file.write("\n"+upsert.get('not reversed'))

