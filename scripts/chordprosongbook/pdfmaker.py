"""
Generate PDFs from chordpro files
Rename PDF songs for latex imports
"""

import os
import subprocess
import shutil
import re
import logging
import jinja2
import io

logger = logging.getLogger(__name__)

try:
   import cPickle as pickle #noqa
except:
   import pickle

key_info_list = [ # https://www.piano-keyboard-guide.com/music-theory-lesson-major-keys-key-signatures-scales-in-circle-of-fifths-order/
    {'key_major_minor': ['C','Am'], 'sharp': True},
    {'key_major_minor': ['Db','Bbm'], 'sharp': False},
    {'key_major_minor': ['D','Bm'], 'sharp': True},
    {'key_major_minor': ['Eb','Cm'], 'sharp': False},
    {'key_major_minor': ['E','C#m'], 'sharp': True},
    {'key_major_minor': ['F','Dm'], 'sharp': False},
    {'key_major_minor': ['Gb','F#','Ebm','D#m'], 'sharp': False},
    {'key_major_minor': ['G','Em'], 'sharp': True},
    {'key_major_minor': ['Ab','Fm'], 'sharp': False},
    {'key_major_minor': ['A','F#m'], 'sharp': True},
    {'key_major_minor': ['Bb','Gm'], 'sharp': False},
    {'key_major_minor': ['B','G#m'], 'sharp': True}
] # or better format to later get the correct transpose direction

class PdfMaker:
    def __init__(self,song_sections,path_song_sections_pdf_includes):
        self.song_sections = song_sections
        self.path_song_sections_pdf_includes = os.path.normpath(path_song_sections_pdf_includes)
        
        self.config_path_a5 = os.path.normpath('../settings/chordpro-configs/a5-2column.json')
        self.config_force_one_column_path = os.path.normpath('../settings/chordpro-configs/force_one_column.json')
        self.config_hide_capo_info_path = os.path.normpath('../settings/chordpro-configs/hide_capo_info.json')
        self.config_capo_key_in_brackets_path = os.path.normpath('../settings/chordpro-configs/capo_key_in_brackets.json')
        self.pdf_setting = {
            "paper_size": "a5"
        }
        # print(os.getcwd())

    def get_alphanumeric(self,string: str):
        return re.sub('[^A-Za-z0-9]+', '', string)
    
    def generate_chordpro_song_pdfs(self,extension="cho",decapo=False):

        for section in self.song_sections:
            # print(section['name'])
            section_output_dir_path = os.path.join(self.path_song_sections_pdf_includes,section['title_include_path_and_ref'],extension)
            section['section_output_dir_path'] = section_output_dir_path
            if not os.path.exists(section_output_dir_path):
                os.makedirs(section_output_dir_path)
            
            for song in section['songs'][extension]:
                # if song['name'] == "Marmor Stein Und Eisen Bricht.cho":
                    # print(song)
                chordpro_file_path = song['path']
                # rename pdf file like this: https://stackoverflow.com/a/5843547
                pdf_file_path = os.path.join(section_output_dir_path,song['title_include_path_and_ref'] + '.pdf')
                
                command = ['chordpro']
                
                if self.pdf_setting["paper_size"] == "a5":
                    command.append(f"--config={self.config_path_a5}")
                if "columns_a5" in song["metadata"] and song["metadata"]["columns_a5"] == '1':
                    command.append(f"--config={self.config_force_one_column_path}")
                
                if 'capo' in song['metadata'] and 'key' in song['metadata']:
                    if decapo:
                        # command.append("--decapo") # do not use decapo but custom --transpose (depending on destination key flat or sharp)
                        # also print or not print capo information
                        # and print Capo-Key when printing Key of Capo (or actual key always? still to decide)
                        key = song['metadata']['key']
                        capo = int(song['metadata']['capo'])
                        
                        # compare lowercase strings
                        for i, key_info in enumerate(key_info_list):
                            if key.lower() in [k.lower() for k in key_info['key_major_minor']]:
                                from_key_index = i
                                logger.debug(f"from_key_index: {from_key_index} | capo: {capo}")
                                destination_key_index = (from_key_index + capo) % 12
                                logger.debug(f"destination_key_index: {destination_key_index}")
                                if key_info_list[destination_key_index]['sharp']:
                                    transpose = capo
                                else:
                                    transpose = capo - 12
                                logger.debug(f"transpose: {transpose}")

                                command.append(f"--config={self.config_hide_capo_info_path}")
                                command.append(f"--transpose={transpose}")
                    else:
                        command.append(f"--config={self.config_capo_key_in_brackets_path}")

                        

                command.extend([f"--output={pdf_file_path}",chordpro_file_path])
                            
                result = subprocess.run(command,capture_output=True)
                song['chordpro_output'] = {'returncode': result.returncode, 'stdout': result.stdout.decode(),'stderr': result.stderr.decode()}
                song['generated_pdf_include_path'] = pdf_file_path

    def filter_chordpro_generation_logs_stderr(self,section,extension):

        exclude_logs = [
            "Config error: unknown item pdf.fonts.comment.frame",
            "columns_a5"
        ]

        for song in section['songs'][extension]:
            stderr = song['chordpro_output']['stderr']
            stderr_filtered = ""
            with io.StringIO(stderr) as fi:
                for line in fi:
                    print_log_line = True
                    for exclude_log in exclude_logs:

                        if exclude_log in line:
                            print_log_line = False
                            continue
                    if print_log_line:
                        stderr_filtered += line + "\n"
                    

            song['chordpro_output']['stderr_filtered'] = stderr_filtered

    def create_chordpro_generation_logs(self,extension="cho"):
        path_template_folder = os.path.normpath('../templates/')
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.abspath(path_template_folder))
        )
        template = env.get_template('chordpro_section_generation_logs.md')

        # document = template.render(section=self.song_sections[0])
        # output_file_name = f"Chordpro Logs {self.song_sections[0]['name']}.md"
        # with open(os.path.join(self.song_sections[0]['section_output_dir_path'],output_file_name),'w') as output:
        #     output.write(document)
            
        for section in self.song_sections:
            self.filter_chordpro_generation_logs_stderr(section,extension)
            
            # print(section['section_output_dir_path'])
            # chordpro_output_of_section = [song['chordpro_output']  for song in section['songs'][extension]]
            # print(chordpro_output_of_section)

            document = template.render(section=section,songs=section['songs'][extension])
            output_file_name = "README.md"
            with open(os.path.join(section['path'],output_file_name),'w') as output:
                output.write(document)


        


    def copy_and_rename_pdf_songs(self):
        for section in self.song_sections:
            if not "pdf-songs" in section["songs"]:
                print(f"Info: Section \"{section['name']}\" does not contain pdf songs.")
                continue
            section_output_dir_path = os.path.join(self.path_song_sections_pdf_includes,section['title_include_path_and_ref'],"pdf-songs")
            section['section_output_dir_path'] = section_output_dir_path
            if not os.path.exists(section_output_dir_path):
                os.makedirs(section_output_dir_path)
            
            for song in section['songs']['pdf-songs']:
                # if song['name'] == "Marmor Stein Und Eisen Bricht.cho":
                    # print(song)
                original_pdf_file_path = song['path']
                # rename pdf file like this: https://stackoverflow.com/a/5843547
                pdf_file_path = os.path.join(section_output_dir_path,song['title_include_path_and_ref'] + '.pdf')

                shutil.copyfile(original_pdf_file_path,pdf_file_path)
                
                # command = ['chordpro']
                
                # if self.pdf_setting["paper_size"] == "a5":
                #     command.append(f"--config={self.config_path_a5}")
                # if "columns_a5" in song["metadata"] and song["metadata"]["columns_a5"] == '1':
                #     command.append(f"--config={self.config_force_one_column_path}")
                
                # command.extend([f"--output={pdf_file_path}",original_pdf_file_path])
                            
                # result = subprocess.run(command,capture_output=True)
                # song['chordpro_output'] = {'returncode': result.returncode, 'stdout': result.stdout.decode(),'stderr': result.stderr.decode()}
                song['generated_pdf_include_path'] = pdf_file_path


    def save_configuration(self):

        song_sections_info_dict_pickle_path = os.path.join(self.path_song_sections_pdf_includes,'song_sections_data.pickle')

        with open(song_sections_info_dict_pickle_path, 'wb') as handle:
            pickle.dump(self.song_sections, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def remove_previous_actions(self):
        old_sections = [{"name": f.name, "path": f.path} for f in os.scandir(self.path_song_sections_pdf_includes) if f.is_dir()]
        if not old_sections:
            print('No sections to remove...')
        else:
            for section in old_sections:
                shutil.rmtree(section['path'])
                print(f"Removed folder for section: {section['name']}")
        
        path_config = os.path.join(self.path_song_sections_pdf_includes,'song_sections_data.pickle')
        if os.path.isfile(path_config):
            os.remove(path_config)
            print('Removed old configuration')
        else:
            print('There was not an old configuration.')

        
                
            