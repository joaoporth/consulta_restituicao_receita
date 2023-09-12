import sys, os
sys.path.insert(1, './')

import re
import requests
from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless

from flask import Flask, jsonify, request


def clean(text) -> str:
    return str(re.sub(r'[^\w\s]', '', str(text))).replace(' ','').strip()

API_KEY = ''


def h_captcha():

		solver = hCaptchaProxyless()
		solver.set_key(API_KEY)
		solver.set_website_url('https://www.restituicao.receita.fazenda.gov.br/')
		solver.set_website_key('1e7b8462-5e38-4418-9998-74210d909134')

		return solver.solve_and_return_solution()


app = Flask(__name__)



class ApiConsulta():
    def __init__(self, cpf:str, data_nascimento:str, ano:str) -> None:
        self.status = False
        self.message = None

        data_nascimento = ''.join(data_nascimento.split('/')[::-1])
        cpf = clean(cpf)

        session = requests.Session()

        cap = h_captcha()

        #print(cap)

        if cap != 0:

            headers = {
                'Accept': '*/*',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': 'https://www.restituicao.receita.fazenda.gov.br/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
                'X-Firebase-AppCheck': '',
                'aplicativo': 'RESTITUICAO',
                'h-captcha-response': cap,
                'origem': 'web',
                'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'servico': 'consultar_restituicao',
                'so': 'WE',
                'token': '',
                'token_esuite': '',
                'token_fcm': '',
                'versao_app': '1.0',
            }

            response = session.get(
                f'https://www.restituicao.receita.fazenda.gov.br/servicos-rfb-apprfb-restituicao/apprfb-restituicao/consulta-restituicao/{cpf}/{ano}/{data_nascimento}',
                headers=headers,
            )

            #print(response.text)

            if response.text in ['hCaptcha expirado ou inválido.', 'Prezado usuário, o seu acesso foi bloqueado por possuir atributos que o caracteriza como um acesso automatizado. Favor tentar novamente']:
                self.message = response.text.strip()
                return

            try:
                self.message = response.json()
                self.status = True


            except:
                self.message = response.text.strip()

        else:
            self.message = 'Captcha unsolved'

def consulta(cpf:str, data_nascimento:str, ano:str) -> dict:

    get = ApiConsulta(cpf, data_nascimento, ano)

    data = {
        'status': get.status,
        'message': get.message,
    }

    return data



# Rota que retorna um JSON simples
@app.route('/api', methods=['GET'])
def get_json():

    cpf = request.args.get('cpf')
    data_nascimento = request.args.get('data_nascimento')
    ano = request.args.get('ano')

    print()
    print('[+] consultando',cpf, data_nascimento, ano)

    response = consulta(cpf, data_nascimento, ano)

    print(response)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

    # /api?cpf=012.392.742-03&data_nascimento=03/01/1992&ano=2020

