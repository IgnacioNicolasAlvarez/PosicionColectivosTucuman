import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(df ,*args, **kwargs):
    """
    Template for loading data from API
    """
    columns=['codlinea', 'interno', 'latitud', 'longitud', 'orientacion', 'proximaParada']
    df_output = pd.DataFrame(columns=columns)

    for _, row in df.iterrows():
        url = f"https://tucuman.miredbus.com.ar/rest/posicionesBuses/{row['codlinea']}"
        response = requests.get(url)

        response_raw = response.json()

        if 'posiciones' in response_raw and isinstance(response_raw['posiciones'], list):


            data = [{**d, 'codlinea': row['codlinea']} for d in response_raw['posiciones']]


            df_linea = pd.DataFrame(data, columns=columns)
            df_output = pd.concat([df_output, df_linea], ignore_index=True)

    return df_output


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
