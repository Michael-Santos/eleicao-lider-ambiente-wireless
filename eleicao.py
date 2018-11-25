##############################################
# Eleição de líder em ambientes sem fio
# Intergrantes: 
#   Michael dos Santos
#   Washington Paes Marques da Silva
##############################################

import threading
import socket
import json
import time


##############################################
# Dfinição topologia
##############################################

# Vizinhos de cada nó
VIZINHOS1  = [3, 4]
VIZINHOS2  = [5] 
VIZINHOS3  = [1, 4, 9]
VIZINHOS4  = [1, 3, 7, 10]
VIZINHOS5  = [2, 6, 7]
VIZINHOS6  = [5]								
VIZINHOS7  = [4, 5, 8]
VIZINHOS8  = [7, 10]
VIZINHOS9  = [3]
VIZINHOS10 = [4, 8] 

# Configura os endereços de cada interface do roteador
def configurarVizinhos(idRoteador):
	switcher = {
		1: VIZINHOS1,
		2: VIZINHOS2,
		3: VIZINHOS3,
		4: VIZINHOS4,
		5: VIZINHOS5,
		6: VIZINHOS6,
		7: VIZINHOS7,
		8: VIZINHOS8,
		9: VIZINHOS9,
		10: VIZINHOS10
	}

	vizinhos = switcher.get(idRoteador, [])
	return(vizinhos)


##############################################
# Execução da eleição
##############################################

# Executa a eleição do coordenador
def eleicaoCoordenador(mensagemJson, idNo, capacidade, idNoPai, vizinhos, vizinhosEsperandoResposta, idEleicaoAtual):
	mensagem = json.loads(mensagemJson.decode('utf-8'))

	if idEleicaoAtual[0] is not None:
		if int(idEleicaoAtual[0]) > int(mensagem["idEleicao"]):
			print("Pacote dropado")
			return
			# dropa pacotes e reinicia estruturas
	else:
		idEleicaoAtual[0] = mensagem["idEleicao"] 


	# Verifica qual é o tipo da mensagem
	if mensagem["tipo"] == "eleicao":
		# Caso já tenha pai é enviado ok, caso contráio é enviado a eleição para os outros vizinhos, exceto o pai
		if idNoPai[0] is not None:
			remetenteMensagemRecebida = mensagem["remetente"]
			print(vizinhosEsperandoResposta)
			mensagem = {"tipo": "ok", "remetente": idNo, "idEleicao": mensagem["idEleicao"], "pai": mensagem["pai"]}
			jsonMensagem = json.dumps(mensagem)
			sender(jsonMensagem, 10000+mensagem["remetente"])
			vizinhosEsperandoResposta.remove(remetenteMensagemRecebida)

		else:
			idNoPai[0] = mensagem["remetente"]
			vizinhosEsperandoResposta.remove(mensagem["remetente"])
			mensagem = {"tipo": "eleicao", "remetente": idNo, "idEleicao": mensagem["idEleicao"], "pai": mensagem["pai"]}
			jsonMensagem = json.dumps(mensagem)

			for vizinho in vizinhosEsperandoResposta:
				sender(jsonMensagem, 10000+vizinho)


	# Caso ainda tenha o vizinho no vetor vizinhosEsperandoResposta ele é removido
	elif mensagem["tipo"] == "ok":
		if mensagem["remetente"] in vizinhosEsperandoResposta:
			vizinhosEsperandoResposta.remove[mensagem["remetente"]]
	elif mensagem["tipo"] == "recurso":
		print("tipo recurso")
		#mensagem = {"tipo": "recurso", "remetente": idNo, "idEleicao": mensagem["idEleicao"], "pai": mensagem["pai"]}


	# Quando não houver mais vizinhos para iterar é enviado a quantidade de recurso para o nó pai
	if not vizinhosEsperandoResposta:
		mensagem = {"tipo": "recurso", "remetente": idNo, "idEleicao": mensagem["idEleicao"], "pai": mensagem["pai"], "recurso": capacidade[0]}
		jsonMensagem = json.dumps(mensagem)
		sender(jsonMensagem, 10000+idNoPai[0])

	time.sleep(2)


##############################################
# Envio o recebimento de mensagem
##############################################

# Recebe mensagens via socket UDP
def receiver(idNo, capacidade, idNoPai, vizinhos, vizinhosEsperandoResposta, idEleicaoAtual):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('', 10000 + idNo)
	sock.bind(server_address)

	while(True):
		data, address = sock.recvfrom(4096)
		eleicaoCoordenador(data, idNo, capacidade, idNoPai, vizinhos, vizinhosEsperandoResposta, idEleicaoAtual)

# Envia mensagens
def sender(mensagem, portaPross):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('', portaPross)
	sent = sock.sendto(mensagem.encode('utf-8'), server_address)

##############################################
# Programa principal
##############################################

# Recebe id do nó e a sua capacidade
idNo = int(input("ID do nó: "))
capacidade = [int(input("Capacidade: "))]
idNoPai = [None]
idEleicaoAtual = [None]

# Obtém os vizinhos
vizinhos = configurarVizinhos(int(idNo))
vizinhosEsperandoResposta = vizinhos.copy()

# Configura o servidor UDP para esse nó
t1 = threading.Thread(target=receiver, args=(idNo, capacidade, idNoPai, vizinhos, vizinhosEsperandoResposta, idEleicaoAtual))
t1.start()

# Inicia uma nova eleição recebendo um id de eleição e enviado uma mensagem de eleição aos seus vizinhos
while(True): 
	input()
	idEleicao = input("ID Eleição: ")
	mensagem = {"tipo": "eleicao", "remetente": idNo, "idEleicao": idEleicao.zfill(3) + str(idNo).zfill(3), "pai": idNo}
	jsonMensagem = json.dumps(mensagem)

	for vizinho in vizinhos:
		sender(jsonMensagem, 10000+vizinho)










