import csv
import re
import arabic_reshaper
from bidi.algorithm import get_display

# english and digits are written left to right, but punctuation is moved to comply
# with RTL language
def is_digit_or_english_with_punctuation(s):
    return re.match('^[\da-zA-Z\u0660-\u0669]+(?:-[\da-zA-Z\u0660-\u0669])*[!.?,،\'\]]{1,}$',s) is not None \
           or re.match('^[!.?,،\'\]]{1,}[\da-zA-Z\u0660-\u0669]+(?:-[\da-zA-Z\u0660-\u0669])*$',s) is not None \
           or re.match('^[!.?,،\'\]]{1,}[\da-zA-Z\u0660-\u0669]+(?:-[\da-zA-Z\u0660-\u0669])*[!.?,،\'\]]{1,}$',s) \
           or re.match('^[\[\]]$',s) is not None

# converts translation into a numbered dictionary
def read_translation_from_csv(csv_path,gender,store,gameos):
    translated_lines = {}
    with open(csv_path, encoding="utf-8-sig") as csvfile:

        csvreader = csv.DictReader(csvfile)
        scene_map = {}
        for line in csvreader:
            translated = line.get('actual translation')
            linux_version = line.get('linux')
            # lazily supporting only this for now
            if gameos == 'linux' and translated == 'DELETE' and linux_version == 'KEEP':
                continue
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
            scene = line.get('scene')
            if scene is not None and scene != '':
                if scene_map.get(scene) is None:
                    scene_map[scene] = {}
                speaker = line.get('speaker')
                scene_map[scene][speaker] = {}
                scene_map[scene][speaker]['start_time'] = line.get('start_time')
                scene_map[scene][speaker]['audiofile'] = line.get('audiofile')
    return translated_lines,scene_map

class TextTools:
    def __init__(self, source, dest, translated_lines, is_captions, max_chars_before_break,
                 total_chars_in_line, language, source_encoding, prefix="",insert_newlines=True,
                 filters=None,basic_formatting=False,text_spacings=[],song_mode=False):
        self.source = source
        self.dest = dest
        self.translated_lines = translated_lines
        self.is_captions = is_captions
        self.max_chars_before_break = max_chars_before_break
        self.total_chars_in_line = total_chars_in_line
        self.language = language
        self.source_encoding = source_encoding
        self.prefix = prefix
        self.insert_newlines = insert_newlines
        self.filters = filters
        self.basic_formatting = basic_formatting
        self.text_spacings = text_spacings
        self.song_mode = song_mode

    # logic for manipulating lines
    def rearrange_multiple_lines(self,caption,max_chars,total_chars,language,prefix="",seperator="<cr>",insert_newlines=True,end_with_space=True,basic_formatting=False,space_within_phrases=False,song_mode=False,disable_phrase_logic=False):
        is_phrase = False
        if ( not disable_phrase_logic ) and str(caption).startswith('\"') and (str(caption).endswith('\"') or (str(caption).endswith('\",'))):
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
        time_text = ""
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
            elif song_mode:
                times = re.findall('\[[0-9.]*]', word)
                if len(times) > 0:
                    time_text = times[0]
                    word = word.replace(time_text, "")
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

            if word != seperator or insert_newlines is False:
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
                line_no_tags = re.sub("(<[a-zA-Z0-9:,.]*>)","",line)

                fill_count = (total_chars - len(line_no_tags))
                fill = "".zfill(fill_count).replace("0", " ")
            result += time_text + fill   + line + line_seperator
        result = prefix + result
        if is_phrase and space_within_phrases:
            result = '"' + result + '"'
        return result


    # calculating parameters for line manipulation and running line manipulation
    def handle_line(self, translated_line, source_line,extra_prefix="",extra_suffix=""):
        replace_index = translated_line.get('replace_index')
        if replace_index is None or replace_index == '':
            replace_index = 0
        else:
            replace_index = int(replace_index)
        orig = translated_line['original']
        translated = translated_line.get('actual translation')
        not_reversed = translated_line.get('not reversed')
        if translated == 'DELETE' or not_reversed == 'DELETE':
            return
        if translated == 'EMPTY' or not_reversed == 'EMPTY':
            source_line = source_line.replace(orig, "")
            return source_line
        if orig in source_line:
            if not_reversed:
                if replace_index != 0:
                    source_line = source_line[0:replace_index] + source_line[replace_index:].replace(orig,not_reversed)
                else:
                    source_line = source_line.replace(orig, not_reversed)
                if self.filters:
                    for filter in self.filters:
                        source_line = source_line.replace(filter, "")
            else:
                if self.is_captions:
                    new_line = self.rearrange_multiple_lines(translated, self.max_chars_before_break,
                                                             self.total_chars_in_line, self.language,
                                                            self.prefix, insert_newlines=self.insert_newlines,
                                                             end_with_space=True,
                                                            basic_formatting=self.basic_formatting)
                    speaker = translated_line.get('speaker')
                    original_speaker = translated_line.get('original_speaker')
                    if original_speaker and speaker:
                        source_line = source_line.replace(original_speaker, speaker)
                else:
                    spacing_style = translated_line.get('spacing style')
                    disable_phrase_logic = False
                    if translated_line.get('disable_phrase_logic') == "TRUE":
                        disable_phrase_logic = True
                    max_chars_before_break = None
                    total_chars_in_line = None
                    space_within_phrases = False
                    insert_newlines = self.insert_newlines
                    if translated_line.get('insert newline') == "FALSE":
                        insert_newlines = False
                    if translated_line.get('insert newline') == "TRUE":
                        insert_newlines = True
                    if spacing_style is not None:
                      if "," in spacing_style:
                        spacings = str(spacing_style).split(",")
                        max_chars_before_break = int(spacings[0])
                        total_chars_in_line = int(spacings[1])
                      else:
                        for spacing in self.text_spacings:
                            if spacing.get('name') == spacing_style:
                                max_chars_before_break = spacing.get('max_chars_before_break')
                                total_chars_in_line = spacing.get('total_chars_in_line')
                                break
                    new_line = self.rearrange_multiple_lines(translated, max_chars_before_break, total_chars_in_line, self.language,
                                                        "", "\\n", insert_newlines=insert_newlines, end_with_space=False,
                                                        basic_formatting=self.basic_formatting,
                                                        space_within_phrases=space_within_phrases, song_mode=self.song_mode,disable_phrase_logic=disable_phrase_logic)

                if replace_index != 0:
                    source_line = extra_prefix + source_line[0:replace_index] + source_line[replace_index:].replace(orig,new_line) + extra_suffix
                else:
                    source_line = extra_prefix + source_line.replace(orig, new_line) + extra_suffix
                if self.filters:
                    for filter in self.filters:
                        source_line = source_line.replace(filter, "")
            print(source_line)
            return source_line

    # translate a file
    def translate(self):
        i = 0
        dest_encoding = 'utf-16'
        if self.source_encoding == 'utf-8':
            dest_encoding = 'utf-8'
        with open(self.source,
                  encoding=self.source_encoding, errors="ignore") as source_file, \
                open(self.dest, "w",
                     encoding=dest_encoding) as dest_file:
            j = 0
            upserts = []
            # Collecting possible upserts
            upsert_lines = set()
            while True:
                j = j+1
                upsert = self.translated_lines.get("upsert_"+str(j))
                if upsert:
                    linetext = upsert.get('linetext')
                    if linetext is not None:
                        linetext = linetext.strip()
                        upsert['linetext'] = linetext
                    upserts.append(upsert)
                    upsert_lines.add(linetext)
                else:
                    break
            for source_line in source_file:
                i += 1
                replaced_with_upserts = False
                translated_line = self.translated_lines.get(str(i))
                if translated_line is not None:
                    source_line = self.handle_line(translated_line,source_line)
                else:
                    # checking line against remaining upserts
                    popped = None
                    source_line_stripped = source_line.strip().replace("\t","        ")
                    if source_line_stripped in upsert_lines:
                        replaced_with_upserts = True
                        while upserts:
                            upsert = upserts[0]
                            line_text = upsert.get('linetext')
                            if line_text == source_line_stripped:
                                extra_prefix = upsert.get('speaker')
                                extra_suffix = ""
                                if extra_prefix == None:
                                    extra_prefix = ""
                                else:
                                    extra_prefix = '\t\t"'+extra_prefix +'"\t\t"'
                                    extra_suffix = '"'
                                upsert_line = self.handle_line(upsert,source_line_stripped,extra_prefix=extra_prefix,extra_suffix=extra_suffix)

                                upsert_line = upsert_line + "\n"
                                dest_file.write(upsert_line)
                                popped = upserts.pop(0)
                                if upsert.get('multi') != 'TRUE':
                                    break
                        if popped:
                            continue
                if source_line is not None and not replaced_with_upserts:
                    dest_file.write(source_line)
            # printing out remaining upserts
            for upsert in upserts:
                dest_file.write("\n"+upsert.get('not reversed'))

