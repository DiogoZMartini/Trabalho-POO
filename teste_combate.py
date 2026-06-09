# run_teste.py
import os
import pygame
from gerenciador import GerenciadorJogo
from componentes.inventario import Inventario
from banco import tabela_jogador, inicializacaoDeCatalogos
from tinydb import Query

class EstadoInventarioAdaptador:

    def __init__(self, nome_jogador, modo="combate"):
        self.inventario = Inventario(nome_jogador, modo)
        self.concluido = False
        self.proximo_estado = "Teste"

    def abrir(self):
        self.inventario.carregarInventario()
        self.concluido = False

    def fechar(self):
        pass

    def tratarEventos(self, eventos):
        self.inventario.tratarEventos(eventos)
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.concluido = True

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        tela.fill((20, 20, 20))
        self.inventario.desenhar(tela)


class EstadoTesteDestino:
    def abrir(self):
        print("Sucesso: Transição de estado realizada!")

    def fechar(self):
        pass

    def tratarEventos(self, eventos):
        pass

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        tela.fill((40, 120, 40))


def configurar_banco_para_teste():
    inicializacaoDeCatalogos()

    nome_do_alvo = "Artorias"
    tabela_jogador.remove(Query().nome == nome_do_alvo)
    tabela_jogador.insert({
        "nome": nome_do_alvo,
        "vida": 85,
        "vidaMaxima": 100,
        "lvl": 12,
        "dinheiro": 1350,
        "inv": [
            {
                "nome": "Poção de Vida",
                "descricao": "Uma poção de cura ao utilizar cura pontos de vida",
                "quantidadeMaxima": 5,
                "efeito": "Cura",
                "preco": 12,
                "tipo": "Consumivel",
                "raridade": "Comum",
                "uso": "Cura 20 de vida",
                "dano": 0
            },
            {
                "nome": "Poção de dano",
                "descricao": "Uma poção instável que ao jogar no inimigo causando dano",
                "quantidadeMaxima": 1,
                "efeito": "Causa Dano",
                "preco": 25,
                "tipo": "Consumivel",
                "raridade": "Comum",
                "uso": "Causa 20 de dano ao inimigo",
                "dano": 20
            }
        ],
        "equipamentos": {
            "capacete": None,
            "colar": None,
            "arma": {
                "nome": "Espada de Madeira",
                "descricao": "Uma espada de madeira de treino.",
                "quantidadeMaxima": 1,
                "efeito": "Aumenta o Dano",
                "preco": 14,
                "tipo": "Arma",
                "raridade": "Comum",
                "uso": "+5 de dano",
                "dano": 5
            },
            "armadura": None,
            "bota": None,
            "anel": None
        }
    })
    return nome_do_alvo


if __name__ == "__main__":
    nome_jogador = configurar_banco_para_teste()
    tela_inventario_estado = EstadoInventarioAdaptador(nome_jogador, modo="combate")
    dicionario_estados = {
        "Inventario": tela_inventario_estado,
        "Teste": EstadoTesteDestino()
    }
    print("Inicializando teste com o seu GerenciadorJogo em modo 'combate'...")
    jogo = GerenciadorJogo(
        largura=800,
        altura=600,
        titulo="Testando Interface de Combate - Estilo Clássico",
        estado=dicionario_estados,
        estado_inicial="Inventario"
    )

    jogo.rodar()