import pyautogui
import subprocess
import time

chrome_path = 'C:/Users/Notebook/AppData/Local/Google/Chrome/Application/chrome.exe'


subprocess.Popen([chrome_path])
time.sleep(2)


url = "https://www.restituicao.receita.fazenda.gov.br/"
pyautogui.hotkey('ctrl', 'l')
pyautogui.write(url)
pyautogui.press('enter')

time.sleep(7)

largura_tela, altura_tela = pyautogui.size()

deslocamento = 100


x_meio = largura_tela // 2
y_meio = altura_tela // 2 - deslocamento


pyautogui.click(x_meio, y_meio)

pyautogui.write('48050999840')

x_meio = largura_tela // 2
y_meio = altura_tela // 2

pyautogui.click(x_meio, y_meio)

pyautogui.write('14042003')

deslocamento = 75

x_meio = largura_tela // 2
y_meio = altura_tela // 2 + deslocamento

pyautogui.click(x_meio, y_meio)

time.sleep(1)


for c in range(2):  #range(sub)
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

time.sleep(2)


screenshot = pyautogui.screenshot()
screenshot.save("screenshot.png")
