import serial
'''
Comunicação bluetooth ente interface gráfica e ESP32

O script em questão implememta a comunicação entre uma GUI e um ESP32 utilizando conexão Bluetooth Low Energy (BLE), permitindo o envio dos
parâmetros PID da interfaçe e com retorno do ESP32 com dados de telemetria durante percurso, tornado possível uma análise visual dos dados

O código se trata apenas de um projeto do produto final, ele ainda não se comunica com a interface ou com o próprio ESP32, mas no futuro
será implementada para envio dos valores e recebimento dos resultados
'''



class com_bluetooth:
  '''
  Classe base base para comunicação com métodos de envio e recebimento de dados via bluetooth
  Gerencia a comunicação serial via Bluetooth entre o Python e o ESP32.
  '''
  '''
  Inicializa a conexão serial
  Parâmetros: porta de comunicação, velocidade de comunicação (baudrate)
  '''
  def __init__(self, porta, baudrate=115200):
        self.ser = serial.Serial(porta, baudrate)
  '''
  Envia uma mensagem via Bluetooth
  Parâmetro: mensagem
  '''
  def enviar(self, mensagem: str):
        self.ser.write((mensagem + '\n').encode())

class protocolo:
  '''
  Classe para padronização doo envio das mensagens ao ESP32, para facilitar comunicação e futura expansão do projeto
  Padroniza os valores obtidos da interfaçe para melhor manipulação e envio para o ESP32
  Padronização: tipo|comando|valor
  '''
  '''
  Cria a mensagem estruturada a ser enviada
  Parâmetros: tipo, variável, valor
  '''
  def montar(self, tipo: str, comando: str, valor: str) -> str:
    return f'{tipo}|{comando}|{valor}' #retorna string com tipo de comando, a variável e o valor
  '''
  Interpreta a mensagem recebida do ESP32, divindindo a string em partes e retornando um dicionário com os valores
  Parâmetro: mensagem
  '''
  def interpretar(self, mensagem: str):
    partes = mensagem.split('|')
    '''
    É esperada uma string de tamanho 3 para ser dividida em três partes (TIPO|COMANDO|VALOR)
    Em caso de erro na mensagem recebida o código continua funcional mas com um aviso de erro
    Em caso de mensagem incompleta o valor é retornado como None
    Em caso de mensagem com excesso de dados os valor adicionais são cortados do dicionário de retorno
    '''
    # Estrutura esperada: 3 partes
    if len(partes) < 3: #mensagem incompleta
      print(f"[AVISO] Mensagem incompleta recebida: '{mensagem}'")

            # Preenche valores faltantes com None
      while len(partes) < 3:
                partes.append(None)

    elif len(partes) > 3: #mensagem com dados a mais
        print(f"[AVISO] Mensagem com excesso de dados: '{mensagem}'")

    tipo, comando, valor = partes[:3] #cria nova lista com os 3 primeiros valores

    return {
            "tipo": tipo,
            "comando": comando,
            "valor": valor
        }