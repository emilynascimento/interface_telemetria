from dados import ProcessadorDados
from interface import AppTelemetria 
from comunicacao import com_bluetooth, protocolo

class ControladorPrincipal:
    """
    Faz a ponte entre a AppTelemetria e a com_bluetooth.
    """
    def __init__(self):
        # 1. Instancia o protocolo e o processador de dados
        self.protocolo = protocolo()
        self.processador = ProcessadorDados()
        self.bluetooth = None
        
        # 2. Instancia a interface passando o controlador (self) para ela
        self.interface = AppTelemetria(controlador=self)

    def iniciar_app(self):
        """
        Inicia a interface e o loop de checagem da porta serial.
        """
        # Configura o Tkinter para checar novos dados a cada 100ms sem congelar a tela
        self.interface.after(100, self._checar_dados_serial)
        self.interface.mainloop()

    # --- Métodos referentes a botões da interface ---

    def conectar_bluetooth(self):
        """
        Lê a COM da interface e conecta.
        """
        porta = self.interface.combo_dispositivos.get()
        if porta and porta != "Buscando...":
            try:
                # O timeout=0.1 evita que o Tkinter congele esperando dados
                self.bluetooth = com_bluetooth(porta, 115200)
                self.bluetooth.ser.timeout = 0.1 
                print(f"Conectado com sucesso na {porta}!")
            except Exception as e:
                print(f"Falha ao conectar: {e}")

    def enviar_parametros_angulares(self):
        """
        Pega os dados das caixas Angular_Kp e Angular_Kd e envia.
        """
        try:
            kp = self.interface.entradas_pid["Angular_Kp"].get()
            kd = self.interface.entradas_pid["Angular_Kd"].get()
            
            # Usa a classe protocolo para montar a string
            mensagem = self.protocolo.montar("SET", "PID_ANG", f"{kp},{kd}")
            
            if self.bluetooth:
                self.bluetooth.enviar(mensagem)
                print(f"Enviado: {mensagem}")
            else:
                print("Erro: Bluetooth não conectado.")
        except KeyError:
            print("Caixas de texto não encontradas.")

    # --- Loop de Leitura em Segundo Plano ---

    def _checar_dados_serial(self):
        """
        Roda a cada 100ms para ler o que o ESP32 enviou.
        """
        if self.bluetooth and self.bluetooth.ser.in_waiting > 0:
            try:
                # Lê a linha enviada pelo ESP32
                dado_cru = self.bluetooth.ser.readline().decode('utf-8').strip()
                if dado_cru:
                    dado_interpretado = self.protocolo.interpretar(dado_cru)
                    # Envia para armazenamento
                    self.processador.processar_dado_interpretado(dado_interpretado)
                    
                    # tempos, y1, y2 = self.processador.obter_dados_plotagem()
                    # self.interface.atualizar_graficos(tempos, y1)
            except Exception as e:
                print(f"Erro na leitura serial: {e}")
                
        # Agenda a função novamente para rodar daqui a 100ms
        self.interface.after(100, self._checar_dados_serial)