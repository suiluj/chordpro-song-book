"""
Generate PDFs from chordpro files
Rename PDF songs for latex imports
"""

import os
import subprocess
import shutil

try:
   import cPickle as pickle #noqa
except:
   import pickle

class PdfMaker:
    def __init__(self,song_sections,path_song_sections_pdf_includes):
        self.song_sections = song_sections
        self.path_song_sections_pdf_includes = os.path.normpath(path_song_sections_pdf_includes)

        for section in self.song_sections:
            section['latex_include_section_name'] = section['name'].replace(',', '').replace(' ', '-').replace('&', '')
        
        self.config_path_a5 = os.path.normpath('../settings/chordpro-configs/a5-2column.json')
        self.config_force_one_column_path = os.path.normpath('../settings/chordpro-configs/force_one_column.json')
        self.pdf_setting = {
            "paper_size": "a5"
        }
        # print(os.getcwd())
    
    def generate_chordpro_song_pdfs(self):

        for section in self.song_sections:
            # print(section['name'])
            section_output_dir_path = os.path.join(self.path_song_sections_pdf_includes,section['latex_include_section_name'],"chordpro-songs")
            section['section_output_dir_path'] = section_output_dir_path
            if not os.path.exists(section_output_dir_path):
                os.makedirs(section_output_dir_path)
            
            for song in section['songs']['chordpro-songs']:
                # if song['name'] == "Marmor Stein Und Eisen Bricht.cho":
                    # print(song)
                chordpro_file_path = song['path']
                pdf_file_path = os.path.join(section_output_dir_path,os.path.splitext(song['name'])[0] + '.pdf')
                
                command = ['chordpro']
                
                if self.pdf_setting["paper_size"] == "a5":
                    command.append(f"--config={self.config_path_a5}")
                if "columns_a5" in song["metadata"] and song["metadata"]["columns_a5"] == '1':
                    command.append(f"--config={self.config_force_one_column_path}")
                
                command.extend([f"--output={pdf_file_path}",chordpro_file_path])
                            
                result = subprocess.run(command,capture_output=True)
                song['chordpro_output'] = {'returncode': result.returncode, 'stdout': result.stdout.decode(),'stderr': result.stderr.decode()}
                song['generated_pdf_include_path'] = pdf_file_path

    def copy_and_rename_pdf_songs(self):
        for section in self.song_sections:
            if not "pdf-songs" in section["songs"]:
                print(f"Info: Section \"{section['name']}\" does not contain pdf songs.")
                continue
            section_output_dir_path = os.path.join(self.path_song_sections_pdf_includes,section['latex_include_section_name'],"pdf-songs")
            section['section_output_dir_path'] = section_output_dir_path
            if not os.path.exists(section_output_dir_path):
                os.makedirs(section_output_dir_path)
            
            for song in section['songs']['pdf-songs']:
                # if song['name'] == "Marmor Stein Und Eisen Bricht.cho":
                    # print(song)
                original_pdf_file_path = song['path']
                pdf_file_path = os.path.join(section_output_dir_path,os.path.splitext(song['name'])[0] + '.pdf')

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

    def merge_and_order_chordpro_and_pdf_songs(self):
        print('coming soon')

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
        
                
            