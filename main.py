from gerenciador import GerenciadorJogo
from estados.estado_template import Exemplo
from estados.menuprincipal import MenuPrincipal
from estados.estado_template import Exemplo
from estados.teste import Teste
def main():
    dicionarioEstados = {  # Cria um dicionário para mapear nomes em texto para as telas reais.
        "Menuprincipal": MenuPrincipal(),  # Instancia a tela de exemplo sob a etiqueta "Exemplo".
        "Exemplo": Exemplo(),
        "teste": Teste()
    }

    jogo = GerenciadorJogo(800,600, "Nome do jogo", dicionarioEstados, "Menuprincipal") #Cria a instância principal do jogo largura (800 px), altura (600 px), título da janela, o dicionário de telas e qual tela começa ativa.
    jogo.rodar()

if __name__ == "__main__":
    main()