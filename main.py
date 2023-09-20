import sys, os
sys.path.insert(1, './')

import re
import requests
from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless

from flask import Flask, jsonify, request
from PIL import Image, ImageDraw, ImageFont


def clean(text) -> str:
    return str(re.sub(r'[^\w\s]', '', str(text))).replace(' ','').strip()

API_KEY = ''

def certificado_nao_consta(cpf, ano):

    imagem = Image.open('nao_consta.png')

    desenhar = ImageDraw.Draw(imagem)
    fonte = ImageFont.truetype('fonte.ttf', 18)

    posicao = (245, 145)
    cor = (120, 120, 120)

    desenhar.text(posicao, cpf, fill=cor, font=fonte)

    imagem.save(os.path.join('comprovantes', f'{cpf}_{ano}.png'))

    imagem.close()



def certificado_a_restituir(cpf, nome, ano, banco, agencia, lote, data_disponibilidade, situacao):

    imagem = Image.open('a_restituir.png')

    desenhar = ImageDraw.Draw(imagem)

    #cpf
    fonte = ImageFont.truetype('fonte.ttf', 16)
    posicao = (20, 70)
    cor = (255, 255, 255)
    desenhar.text(posicao, cpf, fill=cor, font=fonte)

    # nome
    fonte = ImageFont.truetype('fonte.ttf', 12)
    posicao = (20, 95)
    cor = (180, 180, 180)
    desenhar.text(posicao, nome, fill=cor, font=fonte)

    # ano
    fonte = ImageFont.truetype('fonte.ttf', 12)
    posicao = (35, 160)
    cor = (255, 255, 255)
    desenhar.text(posicao, ano, fill=cor, font=fonte)

    # banco
    fonte = ImageFont.truetype('fonte.ttf', 12)
    posicao = (20, 270)
    cor = (255, 255, 255)
    desenhar.text(posicao, banco, fill=cor, font=fonte)


    # agencia
    fonte = ImageFont.truetype('fonte.ttf', 15)
    posicao = (400, 270)
    cor = (255, 255, 255)
    desenhar.text(posicao, agencia, fill=cor, font=fonte)


    # lote
    fonte = ImageFont.truetype('fonte.ttf', 12)
    posicao = (20, 335)
    cor = (255, 255, 255)
    desenhar.text(posicao, lote, fill=cor, font=fonte)


    # data_disponibilidade
    fonte = ImageFont.truetype('fonte.ttf', 12)
    posicao = (400, 335)
    cor = (255, 255, 255)
    desenhar.text(posicao, data_disponibilidade, fill=cor, font=fonte)

    # situacao
    fonte = ImageFont.truetype('fonte.ttf', 12)
    posicao = (20, 360)
    cor = (255, 255, 255)
    desenhar.text(posicao, situacao, fill=cor, font=fonte)


    imagem.save(os.path.join('comprovantes', f'{cpf}_{ano}.png'))

    imagem.close()


def certificado_sem_saldo(cpf, nome, ano):

    imagem = Image.open('sem_saldo.png')

    desenhar = ImageDraw.Draw(imagem)

    #cpf
    fonte = ImageFont.truetype('fonte.ttf', 16)
    posicao = (20, 70)
    cor = (255, 255, 255)
    desenhar.text(posicao, cpf, fill=cor, font=fonte)

    # nome
    fonte = ImageFont.truetype('fonte.ttf', 12)
    posicao = (20, 95)
    cor = (180, 180, 180)
    desenhar.text(posicao, nome, fill=cor, font=fonte)

    # ano
    fonte = ImageFont.truetype('fonte.ttf', 12)
    posicao = (35, 160)
    cor = (255, 255, 255)
    desenhar.text(posicao, ano, fill=cor, font=fonte)

    imagem.save(os.path.join('comprovantes', f'{cpf}_{ano}.png'))

    imagem.close()



def h_captcha():

		solver = hCaptchaProxyless()
		solver.set_key('2936035ef7ebd0f88a38bcba3ab1911d')
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

    cpf = clean(cpf)

    cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    if response['status']:
        # não consta
        if 'Sua declara&ccedil;&atilde;o n&atilde;o consta na base de dados da Receita Federal.' in response['message']['situacao']:
            certificado_nao_consta(cpf, ano)

        if 'Saldo inexistente de imposto a pagar ou a restituir.' in response['message']['situacao']:
            certificado_sem_saldo(cpf, response['message']['nomeContribuinte'], ano)


        if 'Os dados da liberação de sua restituição estão descritos abaixo:' in response['message']['situacao']:
            certificado_a_restituir(cpf, response['message']['nomeContribuinte'], ano, response['message']['dadosBancarios']['banco'], response['message']['dadosBancarios']['agencia'], response['message']['restituicao']['lote'], response['message']['restituicao']['dataDisponibilidade'], response['message']['restituicao']['situacaoRestituicao'])


    return jsonify(response)

if __name__ == '__main__':
    pass
    app.run(debug=True)

    # /api?cpf=012.392.742-03&data_nascimento=03/01/1992&ano=2020

    #certificado_processada('101.863.589-03', 'JOAO VITOR MENDES PORTH', '2022')
