# ChordPro Configuration

- [Configuration: Overview](https://www.chordpro.org/chordpro/chordpro-configuration-overview/)
- [Preset configurations](https://www.chordpro.org/chordpro/chordpro-configuration-presets/)
  - [default configuration](https://www.chordpro.org/chordpro/pub/chordpro_json.txt)
- [Configuration file contents - Generic](https://www.chordpro.org/chordpro/chordpro-configuration-generic/)

## Ablauf

- [default config generieren lassen](https://www.chordpro.org/chordpro/chordpro-configuration-create-cli/)

    ```bash
    chordpro --print-default-config > myconfig.json
    ```

## Plan und wichtige Notizen:

- https://www.chordpro.org/chordpro/chordpro-configuration-generic/
- https://www.chordpro.org/chordpro/chordpro-configuration-presets/
- https://www.chordpro.org/chordpro/using-chordpro/
- https://www.chordpro.org/chordpro/chordpro-fonts/#why-is-using-font-descriptions-important
- https://www.chordpro.org/chordpro/chordpro-fonts/#examples
- https://www.chordpro.org/chordpro/chordpro-configuration-format-strings/

als erstes default config ausgeben lassen und alles rauslöschen, dass ich nicht verändere.
https://www.chordpro.org/chordpro/chordpro-configuration-create-cli/

## Parameter

Nutze _key um tatsächlichen Key für Print zu nehmen und nicht den aus der Capo Sicht

Schauen wie es sich auswirkt, wenn sowieso das Capo rausgerechnet wird:

```shell
decapo
--decapo

If a song has a capo directive, do not show the capo setting in the output but transpose the chords of the song instead. Useful for musicians that want to play along and do not have capo capabilities, e.g. a bass player.

nutze common um einheitlich verünftige schreibweise zu nehmen (nicht H!!!)
erstelle für mich eine nashville version

transcode
--transcode=notation

Transcode all songs to the named notation system. Supported values are:


common (C, D, E, F, G, A, B)
dutch (same as common)
german (C, … A, Ais/B, H)
latin (Do, Re, Mi, Fa, Sol, …)
scandinavian (C, … A, A#/Bb, H)
solfège (Do, Re, Mi, Fa, So, …)
solfege (same as solfège)
nashville (1, 2, 3, …)
roman (I, II, III, …)
```


ChordPro Dateien über Python checken:

ob key angegeben ist.
capo ist egal, da ich "decapo" nutze (siehe oben)

erstelle eigenen metadaten eintrag "columns" um bei kurzen songs zentriert darzustellen
{columns: 1}


// Columns, default one.
"columns" : 2, (mein standard 2)
```