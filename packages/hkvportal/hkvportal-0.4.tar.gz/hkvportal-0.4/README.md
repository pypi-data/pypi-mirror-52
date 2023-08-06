# hkvfewspy
python wrapper for data portal

# installation
`pip install hkvportal`

# usage
```
import hkvportal
dp = hkvportal.Service(url, uid)
```

In de dataportal kan een database worden aangemaakt (`create_database`). In een bestaande database mogen entries worden:
- aangemaakt (`new_entry`)
- bijgewerkt (`update_entry`)
- opgehaald (`get_entry`) of 
- verwijderd (`delete_entry`)

in the notebook folder zijn een aantal jupyter notebooks te vinden met voorbeelden van de beschikbare functies en welke typen data er in de dataportal geupload kunnen worden en hoe deze weer uit te lezen.
- [overview functions hkvportal](https://nbviewer.jupyter.org/github/HKV-products-services/hkvportal/blob/master/notebooks/overview%20functions.ipynb)
- [overview writing data in portal](https://nbviewer.jupyter.org/github/HKV-products-services/hkvportal/blob/master/notebooks/overview%20set%20content-types.ipynb)
- [overview reading data from portal](https://nbviewer.jupyter.org/github/HKV-products-services/hkvportal/blob/master/notebooks/overview%20get%20content-types.ipynb)
