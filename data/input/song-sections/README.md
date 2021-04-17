# Song sections

Scripts will generate a song book from chordpro song files and pdf song files which will be included in a latex document.

## Example folder structure

- data/input/songs-sections
  - church songs (will be name of section in songbook)
    - chordpro-songs
      - <chordprosongfiles.cho>
    - pdf-songs
      - <pdfsongfiles.pdf>

## Explanation

It is important to keep this structure because the scripts scrape this subfolder structure and automatically generate pdfs and latex files.

*Important*:

- chordpro files must have the file extension `.cho`
- pdf files must have the file extension `.pdf`
