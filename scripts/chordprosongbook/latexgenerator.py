# pylint: disable=anomalous-backslash-in-string
"""
Generate LaTeX from ninja templates
"""

import os
import jinja2


try:
   import cPickle as pickle
except:
   import pickle



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
    
    def generate_song_sections(self):
        template = self.latex_jinja_env.get_template('song-section.tex')

        for section in self.song_sections:
            # pp.pprint(section)
            #print(section['name'])
            #pp.pprint(section['songs'])
            
            section_chapter_title = section['name'].replace('&', '\&') # in case section title contains "&" (perhaps also in song file name titles need in special cases) 
            
            document = template.render(section_name=section_chapter_title,songs=section['songs'])
            output_file_name = f"{section['latex_include_section_name']}.tex"
            with open(os.path.join(self.path_song_sections_latex,output_file_name),'w') as output:
                output.write(document)