from gerenciador import GerenciadorJogo
from estados.template import Exemplo
def main():
    dicionarioEstados = {  # Cria um dicionário para mapear nomes em texto para as telas reais.
        "Exemplo": Exemplo()  # Instancia a tela de exemplo sob a etiqueta "Exemplo".
    }

    jogo = GerenciadorJogo(800,600, "Nome do jogo", dicionarioEstados, "Exemplo") #Cria a instância principal do jogo largura (800 px), altura (600 px), título da janela, o dicionário de telas e qual tela começa ativa.
    jogo.rodar()

if __name__ == "__main__":
    main()