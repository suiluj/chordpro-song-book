# pylint: disable=anomalous-backslash-in-string
"""
Generate LaTeX from ninja templates
"""

import os
import jinja2
import fnmatch
from pylatexenc.latexencode import unicode_to_latex

try:
   import cPickle as pickle #noqa
except:
   import pickle

# include pdf toc ref: https://tex.stackexchange.com/a/15995

class LatexGenerator:
    def __init__(self,path_song_sections_pdf_includes,path_song_sections_latex,path_template_folder):
        self.path_song_sections_pdf_includes = os.path.normpath(path_song_sections_pdf_includes)
        self.path_song_sections_latex = os.path.normpath(path_song_sections_latex)


        song_sections_info_dict_pickle_path = os.path.join(self.path_song_sections_pdf_includes,'song_sections_data.pickle')
        with open(song_sections_info_dict_pickle_path, 'rb') as handle:
            self.song_sections = pickle.load(handle)

        self.path_template_folder = path_template_folder

        self.latex_jinja_env = jinja2.Environment(
            block_start_string = '\BLOCK{',
            block_end_string = '}',
            variable_start_string = '\VAR{',
            variable_end_string = '}',
            comment_start_string = '\#{',
            comment_end_string = '}',
            line_statement_prefix = '%-',
            line_comment_prefix = '%#',
            trim_blocks = True,
            autoescape = False,
            loader = jinja2.FileSystemLoader(os.path.abspath(self.path_template_folder))
        )
    
    # def escape_characters_for_latex_strings(self,string):
    #     # https://tex.stackexchange.com/a/34586
    #     # & % $ # _ { } ~ ^ \
    #     escaped_string = string .replace('\\', '\\textbackslash') \
    #                             .replace('&', '\&') \
    #                             .replace('%', '\%') \
    #                             .replace('$', '\$') \
    #                             .replace('#', '\#') \
    #                             .replace('_', '\_') \
    #                             .replace('{', '\{') \
    #                             .replace('}', '\}') \
    #                             .replace('~', '\\textasciitilde') \
    #                             .replace('^', '\\textasciicircum') 
                                
    #     return escaped_string
                    

    def generate_song_sections(self):
        template = self.latex_jinja_env.get_template('song-section.tex')

        for section in self.song_sections:
            # pp.pprint(section)
            #print(section['name'])
            #pp.pprint(section['songs'])
            
            section_chapter_title = unicode_to_latex(section['name']) # in case section title contains "&" (perhaps also in song file name titles need in special cases) 
            
            for song in section['merged_songs']:
                song['latex_title'] = unicode_to_latex(song['latex_title'])
                # song['latex_toc_ref'] escape special characters... but just do not use ref in template at the moment
                # use this: https://stackoverflow.com/a/5843560

            document = template.render(section_name=section_chapter_title,songs=section['merged_songs'])
            output_file_name = f"{section['latex_include_section_name']}.tex"
            with open(os.path.join(self.path_song_sections_latex,output_file_name),'w') as output:
                output.write(document)

    def remove_previous_actions(self):
        old_sections = [{"name": f.name, "path": f.path} for f in os.scandir(self.path_song_sections_latex) if f.is_dir()]

        old_sections = [
                {
                    "name": f.name,
                    "path": f.path
                } 
                for f in os.scandir(self.path_song_sections_latex)
                    if f.is_file()
                    if fnmatch.fnmatch(f,'*.tex')
            ]
        if not old_sections:
            print('No latex sections to remove...')
        else:
            for section in old_sections:
                os.remove(section['path'])
                print(f"Removed latex section: {section['name']}")
