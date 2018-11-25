##############################################
# Eleição de líder em ambientes sem fio
# Intergrantes: 
#   Michael dos Santos
#   Washington Paes Marques da Silva
##############################################

import threading
import socket
import json


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
# Envio o recebimento de mensagem
##############################################

# Recebe mensagens via socket UDP
def receiver(idNo, capacidade, idNoPai, vizinhos, vizinhosEsperandoResposta):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('', 10000 + idNo)
	sock.bind(server_address)

	while(True):
		data, address = sock.recvfrom(4096)

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
t1 = threading.Thread(target=receiver, args=(idNo, capacidade, idNoPai, vizinhos, vizinhosEsperandoResposta))
t1.start()

# Inicia uma nova eleição recebendo um id de eleição e enviado uma mensagem de eleição aos seus vizinhos
while(True): 
	input()
	idEleicao = input("ID Eleição: ")
	mensagem = {"tipo": "eleicao", "remetente": idNo, "idEleicao": idEleicao.zfill(3) + str(idNo).zfill(3), "pai": idNo}
	jsonMensagem = json.dumps(mensagem)

	for vizinho in vizinhos:
		sender(jsonMensagem, 10000+vizinho)










