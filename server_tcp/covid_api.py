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

    def pesquisar_dados_por_uf(self, uf: str):
        try:
            if not uf:
                return {'msg': 'A UF não foi informada!'}
            else:
                r = requests.get(f"{self.base_url}/brazil/uf/{uf}").json()
                if "error" in r:
                    return {
                        'msg': f'Dados não foram encontrados para a UF {uf}'
                    }
                else:
                    return {
                        "estado": f"{r['state']}",
                        "quantidade_total_casos": r['cases'],
                        "quantidade_suspeitos": r['suspects'],
                        "quantidade_total_mortes": r['deaths']
                    }
        except Exception as _:
            raise ApiError(f"Api error!")

    def pesquisar_dados_por_data(self, data: str):
        try:
            if not data:
                return {'msg': 'A data não foi informada!'}
            else:
                r = requests.get(
                    f"{self.base_url}/brazil/{data}").json()["data"]
                if not r:
                    return {
                        'msg':
                        'Não foram encontrados dados referentes a data informada!'
                    }
                else:
                    covid_list = []
                    for covid_info in r:
                        covid_list.append({
                            "estado":
                            f"{covid_info['state']}",
                            "quantidade_total_casos":
                            covid_info['cases'],
                            "quantidade_suspeitos":
                            covid_info['suspects'],
                            "quantidade_total_mortes":
                            covid_info['deaths']
                        })
                    return covid_list
        except Exception as _:
            raise ApiError(f"Api error!")
