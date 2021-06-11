"""Scan songs in folder
"""

import os
import fnmatch
import re
from pylatexenc.latexencode import unicode_to_latex

class SongScanner:
    def __init__(self,path_input_song_sections):
        self.path_input_song_sections = os.path.normpath(path_input_song_sections)
        
        # print(os.getcwd())
    
    def get_alphanumeric(self,string: str):
        return re.sub('[^A-Za-z0-9]+', '', string)

    def detect_song_sections(self,sections_base_path=None):
        # https://stackoverflow.com/a/59938961 (always use scandir)
        # self.song_sections = [{"name": f.name, "path": f.path} for f in os.scandir(self.path_input_song_sections) if f.is_dir()]

        if not sections_base_path:
            sections_base_path = self.path_input_song_sections
        gen = (f for f in os.scandir(sections_base_path) if f.is_dir())
            
        self.song_sections = []
        for f in gen:
            if f.name.startswith('#'):
                s = os.path.splitext(f.name)[0]
                title = s[s.index(' ') + 1:].strip()
                order = s[1:s.index(' ')].strip()
            else:
                title = os.path.splitext(f.name)[0]
                order = "mmm" # do not use float("inf") because cannot compare str and float; use three "m" as middle to be able to add more later

            title_latex = unicode_to_latex(title)
            title_include_path_and_ref = self.get_alphanumeric(title)            
            
            self.song_sections.append(
                {
                    'name': f.name,
                    'path': f.path,
                    'title': title,
                    'title_latex': title_latex,
                    'title_include_path_and_ref': title_include_path_and_ref,
                    'order': order
                }
            )


    

    def detect_songs_of_sections(self,extension,subfolder=""):
        for section in self.song_sections:
                
            # python list comprehension tips: multiple if statements, multiple lines syntax
            # https://stackoverflow.com/a/15248356
            # https://stackoverflow.com/a/12372259
            section_subfolder_path = os.path.join(section['path'],subfolder)
            if not os.path.exists(section_subfolder_path):
                print(f"Info: Section \"{section['name']}\" does not contain a subfolder \"{subfolder}\".")
                continue

            # songs_of_section_subfolder = [
            #     {
            #         "name": f.name,
            #         "path": f.path
            #     } 
            #     for f in os.scandir(section_subfolder_path)
            #         if f.is_file()
            #         if fnmatch.fnmatch(f,f'*.{extension}')
            # ]

            gen = (f for f in os.scandir(section_subfolder_path) if f.is_file() if fnmatch.fnmatch(f,f'*.{extension}'))
            
            new_songs_of_section = []
            for f in gen:
                # print(f)
                
                # check order information
                if f.name.startswith('#'):
                    s = os.path.splitext(f.name)[0]
                    title = s[s.index(' ') + 1:].strip()
                    order = s[1:s.index(' ')].strip()
                else:
                    title = os.path.splitext(f.name)[0]
                    order = "mmm" # do not use float("inf") because cannot compare str and float; use three "m" as middle to be able to add more later

                title_latex = unicode_to_latex(title)
                title_include_path_and_ref = self.get_alphanumeric(title)

                # check multi titles
                multi_titles_latex = []

                if "|" in title:
                    multi_titles_latex = [unicode_to_latex(x.strip()) for x in title.split('|')]
                
                new_songs_of_section.append(
                    {
                        'name': f.name,
                        'path': f.path,
                        'title': title,
                        'title_latex': title_latex,
                        'multi_titles_latex': multi_titles_latex,
                        'title_include_path_and_ref': title_include_path_and_ref,
                        'order': order
                    }
                )

            if not "songs" in section:
                section["songs"] = {}

            if not extension in section["songs"]:
                section["songs"][extension] = []
            section["songs"][extension].extend(new_songs_of_section)


    def extract_chordpro_metadata(self,extension="cho"):
        # https://stackoverflow.com/questions/40972805/python-capture-contents-inside-curly-braces/40972959
        # https://stackoverflow.com/questions/11310567/python-re-match-string-in-a-file/11310926

        regex = r"\{(.*?)\}"
        for section in self.song_sections:
            
            if not extension in section["songs"]:
                print(f"Info: Section \"{section['name']}\" does not contain songs with the extension \"{extension}\".")
                continue

            for song in section["songs"][extension]:
                with open(song["path"]) as f:
                    # print (re.findall(regex,f.read(),re.MULTILINE))
                    matches = re.findall(regex,f.read())
                    # pp.pprint(matches)
                    # important! key is not real key when using capo
                    # when capo or custom columns key are searched my break condition will almost always never early quit
                    missing_keys = ["title","artist","key","capo","columns_a5"]
                    metadata = {}
                    for match in matches:
                        # print(song["name"], match)
                        # remove found key but iterate over copy (by using slicing syntax): 
                        for i, key in enumerate(missing_keys[:]):
                            if match.startswith(key):
                                metadata[key] = match[len(f"{key}:"):].strip()
                                # print("added: ", song["name"], match)
                                del missing_keys[i]
                                # print(missing_keys)
                                break
                        if not missing_keys: break
                    song["metadata"] = metadata

                    title = ""
                    if 'title' in metadata: title += metadata['title']
                    if 'artist' in metadata: title += f" - {metadata['artist']}"
                    song["title"] = title
                    song["title_latex"] = unicode_to_latex(title)
                    song["title_include_path_and_ref"] = self.get_alphanumeric(title)

