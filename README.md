# chordpro-song-book

latex chordpro pdf song book

## Disclaimer: Under active development

**Plans/Todo:**

- [x] scan for chopro files in input folder
  - [x] find songs
  - [x] extract metadata
- [ ] Generate individual pdfs from chordpro files
- [ ] scan for other songs (pdf files)
  - [ ] extract metadata
    - [ ] from filename
    - [ ] (perhaps pdf metadata if available)
- [ ] Create Jinja LaTex templates from scan result
  - [ ] include chordpro pdfs
  - [ ] include other pdfs (other songs, misc pdfs)
- [ ] Write songbook LaTeX

## Getting Started

1. clone this repo
2. Install anaconda/miniconda
   - install enviroment from `enviroment.yml`

      ```shell
      conda env create -f environment.yml
      ```

3. Install latex
4. [Install ChordPro cli](https://www.chordpro.org/chordpro/chordpro-installation/)
5. copy your chordpro and pdf files in `data/input/*`
6. run notebooks in `scripts`folder to generate latex document
7. open latex document in you latex editor and export pdf song book
   - use your tex editor (like texstudio) for last changes
   - or use a script which calls `pdflatex` for the main song book tex file
8. Print your PDF song book and have fun! :)

## Used software/tools

- [Anaconda/Miniconda (Python environment)](https://www.anaconda.com/products/individual)
- [ChordPro cli tool (generate PDFs from chorpro files)](https://www.chordpro.org/chordpro/chordpro-file-format-specification/)
- [LaTeX (merge pdf files and create song book as pdf with table of contents)](https://www.latex-project.org/)
- [Jinja (Template Engine -> generate TeX files from python code)](https://palletsprojects.com/p/jinja/)
- [Jupyter Lab (Web IDE for interactive python development)](https://jupyter.org/)
  - I prefer Jupyter Notebooks for easy development with output between a few lines of code
  - You could convert notebooks to *normal* python scripts

## Info, tips, readme

There are `README.md` files with useful links and information in some subfolders of this repo.

## more links/info

- [Alternative: advanced latex song book package (not used in this repo)](https://rath.ca/Misc/Songbook/)
- [latex document classes](https://en.wikibooks.org/wiki/LaTeX/Document_Structure#Document_classes)
  - [differences explained](https://tex.stackexchange.com/a/36989)
