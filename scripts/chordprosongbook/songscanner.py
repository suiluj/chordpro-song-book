"""Scan songs in folder
"""

import os
import fnmatch
import re

class SongScanner:
    def __init__(self,path_input_song_sections):
        self.path_input_song_sections = os.path.normpath(path_input_song_sections)
        
        # print(os.getcwd())
    
    def detect_song_sections(self):
        # https://stackoverflow.com/a/59938961 (always use scandir)
        self.song_sections = [{"name": f.name, "path": f.path} for f in os.scandir(self.path_input_song_sections) if f.is_dir()]
    

    def detect_chordpro_songs(self):
        for section in self.song_sections:
                
            # python list comprehension tips: multiple if statements, multiple lines syntax
            # https://stackoverflow.com/a/15248356
            # https://stackoverflow.com/a/12372259
            songs_of_section = [
                {
                    "name": f.name,
                    "path": f.path
                } 
                for f in os.scandir(section['path'])
                    if f.is_file()
                    if fnmatch.fnmatch(f,'*.cho')
            ]
            
            section["songs"] = songs_of_section

    def extract_chordpro_metadata(self):
        # https://stackoverflow.com/questions/40972805/python-capture-contents-inside-curly-braces/40972959
        # https://stackoverflow.com/questions/11310567/python-re-match-string-in-a-file/11310926

        regex = r"\{(.*?)\}"
        for section in self.song_sections:
            for song in section["songs"]:
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