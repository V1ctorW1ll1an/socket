#!/usr/bin/env python3
import json
import socket

from covid_api import CovidApi

from covid_api import CovidApi

HOST = ''
PORT = 65431

###### UDP #######


def start_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((HOST, PORT))
            print("Start server")
            while True:
                data, addr = server_socket.recvfrom(1024)
                print('Connected by', addr)
                decode_data = json.loads(data)
                method = decode_data["method"]
                parameter = decode_data["parameter"]
                covid_api = CovidApi()
                response = covid_api.pesquisar_dados_por_pais(parameter)
                encoded_response = json.dumps(response, ensure_ascii=False).encode("utf-8")

                server_socket.sendto(encoded_response,addr)
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
