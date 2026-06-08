from gerenciador import GerenciadorJogo
from estados.estado_template import Exemplo
from estados.menuprincipal import MenuPrincipal
from estados.estado_template import Exemplo
from estados.estado_saves import Saves
from estados.estado_NG import NewGame
from estados.estado_classes import Classes
from estados.menupause import MenuPause
def main():
    dicionarioEstados = {  # Cria um dicionário para mapear nomes em texto para as telas reais.
        "Exemplo": Exemplo(),# Instancia a tela de exemplo sob a etiqueta "Exemplo".
        "Menuprincipal": MenuPrincipal(),  
        "Saves": Saves(),
        "Newgame": NewGame(),
        "Classes": Classes(),
        "Menupause": MenuPause()
    }

    jogo = GerenciadorJogo(800,600, "Nome do jogo", dicionarioEstados, "Menuprincipal") #Cria a instância principal do jogo largura (800 px), altura (600 px), título da janela, o dicionário de telas e qual tela começa ativa.
    jogo.rodar()

if __name__ == "__main__":
    main()