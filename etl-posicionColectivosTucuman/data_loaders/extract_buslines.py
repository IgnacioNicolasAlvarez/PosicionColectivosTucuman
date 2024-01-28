import io
import pandas as pd
import requests
import json

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def extract_data(data, cod_grupo_padre=None, df=None):
    if df is None:
        df = pd.DataFrame(columns=['codGrupo', 'codSubGrupo', 'codLinea', 'descripcion'])
        
    if 'subGrupos' in data and data['subGrupos'] is not None:
        for subgrupo in data['subGrupos']:
            if 'lineas' in subgrupo and subgrupo['lineas'] is not None:
                for linea in subgrupo['lineas']:
                    df = pd.concat([df, pd.DataFrame({
                        'codGrupo': [data['codGrupo']],
                        'codSubGrupo': [subgrupo['codGrupo']],
                        'codLinea': [linea['codLinea']],
                        'descripcion': [linea['descripcion']]
                    })], ignore_index=True)
            df = extract_data(subgrupo, cod_grupo_padre if cod_grupo_padre else data['codGrupo'], df)
    
    return df

@data_loader
def load_data_from_api(*args, **kwargs):

    url = 'https://tucuman.miredbus.com.ar/rest/gruposLineas'
    response = requests.get(url)


    response_raw = response.json()

    return extract_data(response_raw["grupos"])


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
