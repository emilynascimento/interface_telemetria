class ProcessadorDados:
    """
    Processa os dados gerados pelo 'protocolo.interpretar()'
    e armazena as listas numéricas para plotagem.
    """
    def __init__(self):
        # Arrays que alimentarão os gráficos
        self.tempos = []
        self.valores_y1 = [] # Para o gráfico 1
        self.valores_y2 = [] # Para o gráfico 2

    def processar_dado_interpretado(self, dicionario: dict):
        """
        Recebe os dados interpretados.
        """
        pass

    def obter_dados_plotagem(self):
        """
        Retorna os dados prontos para plotagem.
        """
        return self.tempos, self.valores_y1, self.valores_y2

    def limpar_dados(self):
        """
        Limpa os dados armazenados.
        """
        self.tempos.clear()
        self.valores_y1.clear()
        self.valores_y2.clear()