from iqoptionapi.stable_api import IQ_Option
from dotenv import load_dotenv
from colorama import init, Fore, Back
import os, time, sys
from datetime import datetime

init(convert=True, autoreset=True)
load_dotenv() # Carrega Credencias .env

def stop(lucro, gain, loss):
	if lucro <= float('-' + str(abs(loss))):
		print('Stop Loss batido!')
		sys.exit()
		
	if lucro >= float(abs(gain)):
		print('Stop Gain Batido!')
		sys.exit()

def calcula_intervalo(intevalo):
	if intervalo == 60:
		sleep = 0.5
		minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
		entrar = True if (minutos >= 4.58 and minutos <= 5) or minutos >= 9.58 else False
	elif intervalo == 300:
		sleep = 30
		minutos = float(((datetime.now()).strftime('%M.%S')))
		entrar = True if (minutos >= 29 and minutos <= 30) or minutos >= 60.58 else False

	return sleep, minutos, entrar

def Payout(par):
	API.subscribe_strike_list(par, 1)
	while True:
		d = API.get_digital_current_profit(par, 1)
		if d != False:
			d = round(int(d) / 100, 2)
			break
		time.sleep(1)
	API.unsubscribe_strike_list(par, 1)
	
	return d

def Martingale(valor, payout):
	lucro_esperado = valor * payout
	perca = float(valor)	
		
	while True:
		if round(valor * payout, 2) > round(abs(perca) + lucro_esperado, 2):
			return round(valor, 2)
			break
		valor += 0.01

def direcao_entrada(cores):
	if cores.count('g') > cores.count('r') and cores.count('d') == 0 : 
		direcao = 'put'
	elif cores.count('r') > cores.count('g') and cores.count('d') == 0 : 
		direcao = 'call'
	else:
		direcao = False

	return direcao

def cores_velas(velas):
	for i in range(5):
		velas[i] = 'g' if velas[i]['open'] < velas[i]['close'] else 'r' if velas[i]['open'] > velas[i]['close'] else 'd'

	return f"{velas[0]} {velas[1]} {velas[2]} {velas[3]} {velas[4]}"

duracao=1#minute 1 or 5
montante=30

API=IQ_Option(os.getenv("USER"),os.getenv("PASS"))
check,reason=API.connect()
saldo = API.get_balance()
moeda = API.get_currency()

print(f'''Banca Inicial R${saldo}\nMoeda: {moeda}''')

martingale = int(input('Indique a quantia de martingales: '))
martingale += 1

intervalo = int(input("Digite o Intervalo em minutos: ")) * 60
print(f"Intervalo {intervalo}")
par = input("Indique uma paridade para operar: ")
print(f"Mercado a ser Operado {par}")
montante = int(input("Indique um valor para entrar: "))
print(f"Quantia aplicada R${montante}")

stop_loss = float(input(' Indique o valor de Stop Loss: '))
stop_gain = float(input(' Indique o valor de Stop Gain: '))

valor_entrada_b = float(montante)

print(f"Contratos ativos: {par}")
print(f"Duração: {duracao}m")

lucro = 0
payout = Payout(par)
while True:
	sleep, minutos, entrar = calcula_intervalo(intervalo)

	print('Hora de entrar?',entrar,'/ Minutos:',minutos)
	if entrar:
		print('\n\nIniciando operação!')
		print('Verificando cores..', end='')
		velas = API.get_candles(par, intervalo, 5, time.time())
		
		cores = cores_velas(velas) # define as cores das velas Ex.: g r g
		print(cores)
		direcao = direcao_entrada(cores) #define a posição de compra se for call ou put
		
		if direcao:
			print('DIREÇÃO:', direcao)

			valor_entrada = valor_entrada_b

			for i in range(martingale):
				status,id = API.buy_digital_spot(par, montante, direcao, 1)
			
				if status:
					while True:
						status,valor = API.check_win_digital_v2(id)
						
						if status:
							valor = valor if valor > 0 else float('-' + str(abs(valor_entrada)))
							print('Resultado operação: ', end='')
							print(Back.GREEN + 'WIN /' if valor > 0 else Back.RED + 'LOSS /' , round(valor, 2) ,'/', round(lucro, 2),('/ '+str(i)+ ' GALE' if i > 0 else '' ))
							valor_entrada = Martingale(valor_entrada, payout)
							stop(lucro, stop_gain, stop_loss)
							break

					if valor > 0: break
				else:
					print('\nERRO AO REALIZAR OPERAÇÃO\n\n')
				
	time.sleep(sleep)