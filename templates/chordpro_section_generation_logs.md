# Chordpro Logs für "{{section.name}}"

> **Hinweise:**
> Im Ordner [Aktuelle PDF Versionen zum checken](https://cloud.junges-ermland.de/index.php/f/34378) kannst du dir deinen Abschnitt anschauen.

---
{%for song in songs%}

## Errors für "{{song.name}}"

```text
{{song.chordpro_output.stderr_filtered}}
```

---
{%endfor%}
