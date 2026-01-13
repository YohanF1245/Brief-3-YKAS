import pandera as pa 
from pandera.typing import Series, DataFrame 

class D1Schema(pa.DataFrameModel):
    operation_id: Series[int]
    categorie_personne: Series[str]
    resultat_humain: Series[str]
    nombre: Series[int]
    dont_nombre_blesse: Series[int]

    class Config:
        coerce = True