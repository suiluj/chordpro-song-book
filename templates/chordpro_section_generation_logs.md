# Chordpro Logs für "{{section.name}}"

> **Hinweis:** *Unknown directive: columns_a5:* Meldungen sind kein Problem 
---
{%for song in songs%}
## {{song.name}}

```text
{{song.chordpro_output.stderr}}
```
---
{%endfor%}
