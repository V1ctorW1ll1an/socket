import requests


class ApiError(Exception):
    pass


class CovidApi:
    def __init__(self):
        self.base_url = "https://covid19-brazil-api.now.sh/api/report/v1/"

    def pesquisar_dados_por_pais(self, country: str):
        try:
            if not country:
                return {'msg': 'O pais não foi informado'}
            else:
                r = requests.get(f"{self.base_url}/{country}").json()["data"]
                if not r:
                    return {
                        'msg': f'Dados não encontrados para o pais {country}'
                    }
                else:
                    return {
                        "pais": f"{r['country']}",
                        "quantidade_total_casos_confirmados": r['confirmed'],
                        "quantidade_total_recuperados": r['recovered'],
                        "quantidade_total_mortes": r['deaths']
                    }
        except Exception as _:
            raise ApiError(f"Api error!")