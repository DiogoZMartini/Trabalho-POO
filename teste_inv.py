# run_teste.py
from gerenciador import GerenciadorJogo
from estados.estado_inventario import EstadoInventario
from banco import tabela_jogador
from tinydb import Query

def configurar_banco_para_teste():
    nome_do_alvo = "Artorias"
    tabela_jogador.remove(Query().nome == nome_do_alvo)
    tabela_jogador.insert({
        "nome": nome_do_alvo,
        "vida": 100,
        "vidaMaxima": 100,
        "inv": [
            {
                "nome": "Poção de Vida",
                "descricao": "Uma poção de cura ao utilizar cura pontos de vida",
                "quantidadeMaxima": 5,
                "efeito": "Cura",
                "preco": 12,
                "tipo": "Consumivel",
                "raridade": "Comum",
                "img": "assets/img/itens/pocaoDeVida.jpg",
                "uso": "Cura 20 de vida",
                "dano": 0
            },
            {
                "nome": "Poção de Velocidade",
                "descricao": "Uma poção que faz o seu próximo ataque atingir o alvo uma vez adicional",
                "quantidadeMaxima": 2,
                "efeito": "Segundo Ataque",
                "preco": 50,
                "tipo": "Consumivel",
                "raridade": "Comum",
                "img": None,
                "uso": "Seu proximo ataque é usado 2x",
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
                "img": None,
                "uso": "Causa 20 de dano ao inimigo",
                "dano": 20
            },
            {
                "nome": "Yelmo Lendário de Dragão",
                "descricao": "Um capacete forjado nas chamas de um dragão ancião. Concede muita defesa.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 1200,
                "tipo": "Capacete",
                "raridade": "Lendário",
                "img": None,
                "uso": "+10 de defesa",
                "dano": 0
            }
        ],
        "equipamentos": {
            "capacete": {
                "nome": "Elmo de Ferro",
                "descricao": "Proteção pesada para a cabeça.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 150,
                "tipo": "Capacete",
                "raridade": "Comum",
                "img": None,
                "uso": "+3 de defesa",
                "dano": 0
            },
            "colar": {
                "nome": "Amuleto de Rubi",
                "descricao": "Aumenta ligeiramente a sua estamina.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 300,
                "tipo": "Colar",
                "raridade": "Raro",
                "img": None,
                "uso": "+1 de dano",
                "dano": 0
            },
            "arma": {
                "nome": "Espada de Madeira",
                "descricao": "Uma espada de madeira",
                "quantidadeMaxima": 1,
                "efeito": "Aumenta o Dano",
                "preco": 14,
                "tipo": "Arma",
                "raridade": "Comum",
                "img": None,
                "uso": "+5 de dano",
                "dano": 5
            },
            "armadura": {
                "nome": "Armadura de Couro", # <--- Agora no lugar certo!
                "descricao": "Uma armadura de coiro",
                "quantidadeMaxima": 1,
                "efeito": "Aumenta a Defesa",
                "preco": 20,
                "tipo": "Armadura",
                "raridade": "Comum",
                "img": None,
                "uso": "+5 de defesa",
                "dano": -5
            },
            "bota": {
                "nome": "Botas de Couro",
                "descricao": "Permite mover-se com mais silêncio.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 80,
                "tipo": "Bota",
                "raridade": "Comum",
                "img": None,
                "uso": "+2 de defesa",
                "dano": 0
            },
            "anel": {
                "nome": "Anel do Falcão",
                "descricao": "Aumenta a precisão de ataques críticos.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 500,
                "tipo": "Anel",
                "raridade": "Lendário",
                "img": None,
                "uso": "+3 de dano",
                "dano": 0
            }
        }
    })

    return nome_do_alvo

class EstadoTesteDestino:
    def abrir(self): print("Sucesso: Mudou para o próximo estado!")
    def fechar(self): pass
    def tratarEventos(self, eventos): pass
    def atualizar(self, dt): pass
    def desenhar(self, tela): tela.fill((40, 120, 40))


if __name__ == "__main__":
    nome_jogador = configurar_banco_para_teste()
    tela_inventario = EstadoInventario(nome_jogador)
    dicionario_estados = {
        "Inventario": tela_inventario,
        "Teste": EstadoTesteDestino()
    }

    print("Inicializando teste com o seu GerenciadorJogo e EstadoInventario...")
    jogo = GerenciadorJogo(
        largura=800,
        altura=600,
        titulo="Testando Estado de Inventario",
        estado=dicionario_estados,
        estado_inicial="Inventario"
    )

    jogo.rodar()