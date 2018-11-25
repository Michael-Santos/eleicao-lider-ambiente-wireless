##############################################
# Eleição de líder em ambientes sem fio
# Intergrantes: 
#   Michael dos Santos
#   Washington Paes Marques da Silva
##############################################

import treading
import socket


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
def receiver(idPross, portaPross):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('', PORTAS_PROCESSOS[portaPross])
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
idNo = input("ID do nó: ")
capacidade = input("Capacidade: ")
capacidade = [capacidade]

# Obtém os vizinhos
vizinhos = configurarVizinhos(idNo)

# Configura o servidor UDP para esse nó
t1 = threading.Thread(target=receiver, args=(idNo, capacidade, vizinhos))
t1.start()

# Execução
whlile(True):
	input()
	idEleicao = input("ID Eleição: ")
	mensagem = {"tipo": "eleicao", "remetente": idNo, "idEleicao": idEleicao, "pai": }










