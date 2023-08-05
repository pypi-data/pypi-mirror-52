# hkvfewspy
python wrapper for data portal

# installation
`pip install hkvportal`

# usage
```
import hkvportal
dp = hkvportal.Service(url, [uid])
```

In de dataportal kan een database worden aangemaakt (`createDatabase`). In een bestaande database mogen entries worden:
- aangemaakt (`setEntry`)
- bijgewerkt (`updateEntry`)
- opgehaald (`getEntry`) of 
- verwijderd (`deleteEntry`)

in the notebook folder zijn een aantal jupyter notebooks met meer voorbeelden.
