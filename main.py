import pyautogui
import subprocess
import time
import sys




pyautogui.hotkey('win', 'r')


url = "https://www.restituicao.receita.fazenda.gov.br/"
pyautogui.write(url)
pyautogui.press('enter')

time.sleep(7)

largura_tela, altura_tela = pyautogui.size()

deslocamento = 100


x_meio = largura_tela // 2
y_meio = altura_tela // 2 - deslocamento


pyautogui.click(x_meio, y_meio)
time.sleep(1)

cpf = ''

pyautogui.write(cpf)

x_meio = largura_tela // 2
y_meio = altura_tela // 2

pyautogui.click(x_meio, y_meio)
time.sleep(1)

dtNasc = ''

pyautogui.write(dtNasc)

deslocamento = 75

x_meio = largura_tela // 2
y_meio = altura_tela // 2 + deslocamento

pyautogui.click(x_meio, y_meio)

time.sleep(1)

currentYear = int(time.strftime('%Y')) + 1
year = 2022
downs = currentYear - year


for c in range(downs):  #range(sub)
    pyautogui.press('down')


pyautogui.press('enter')

for c in range(8):
    pyautogui.press('tab')
pyautogui.press('enter')

time.sleep(2)


deslocamento = 250

x_meio = largura_tela // 2
y_meio = altura_tela // 2 + deslocamento

pyautogui.click(x_meio, y_meio)

time.sleep(3)



screenshot = pyautogui.screenshot()
screenshot.save(f"{cpf}_{year}.png")
pyautogui.hotkey('ctrl', 'w')
time.sleep(65)

