# Song sections

Import you chordpro and pdf files in different subfolders for each section

## Example

- songs/sections
  - church songs
    - chordpro
      - <chordprosongfiles.chordpro>
    - pdf
      - <pdfsongfiles.pdf>

## Explanation

It is important to keep this structure because the scripts scrape this subfolder structure and automatically generate pdfs and latex files.

*Important*:

- chordpro files must have the file extension `.chordpro`
- pdf files must have the file extension `.pdf`
