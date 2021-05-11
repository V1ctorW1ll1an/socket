#!/usr/bin/env python3
import json
import socket

from covid_api import CovidApi

HOST = ''
PORT = 65432

###### TCP #######


def get_data_from_api_service(method, parameter):
    try:
        if not method:
            return {
                "msg": "O metodo de pesquisa não foi informado!"
            }
        elif not parameter:
            return {
                "msg": "O parametro de pesquisa não foi informado!"
            }
        else:
            covid_api = CovidApi()
            if method == "pesquisar_dados_por_pais":
                return covid_api.pesquisar_dados_por_pais(parameter)
            elif method == "pesquisar_dados_por_uf":
                return covid_api.pesquisar_dados_por_uf(parameter)
            elif method == "pesquisar_dados_por_data":
                return covid_api.pesquisar_dados_por_data(parameter)
    except Exception as e:
        return {
            "msg": f"Ocorreu um erro no metodo {get_data_from_api_service.__name__}: {e.args[-1]}"
        }


def start_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            print("Start server")
            server_socket.listen()
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        decode_data = json.loads(data)
                        # method é o tipo de pesquisa (uf, pais, data)
                        method = decode_data["method"]
                        # parameter (pais ou data ou uf)
                        parameter = decode_data["parameter"]
                        response = get_data_from_api_service(method, parameter)
                        encoded_response = json.dumps(response, ensure_ascii=False).encode("utf-8")

                        conn.sendall(encoded_response)
                        print("Dados enviados ao client!")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    try:
        start_server()

    except KeyboardInterrupt as keyboard_exception:
        print("Operação encerrada pelo usuario!")
    except Exception as e:
        print(e)
