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
                "nome": "Poção de Cura",
                "descricao": "Recupera 30 de vida instantaneamente.",
                "quantidadeMaxima": 5,
                "dano": 0,
                "efeito": "Cura",
                "preco": 20,
                "raridade": "Comum",
                "tipo": "Consumivel",
                "valor_efeito": 30,
                'img': "assets/img/itens/pocaoDeVida.jpg"
            },
            {
                "nome": "Yelmo Lendário de Dragão",
                "descricao": "Um capacete forjado nas chamas de um dragão ancião. Concede muita defesa.",
                "quantidadeMaxima": 1,
                "dano": 0,
                "efeito": "Nenhum",
                "preco": 1200,
                "raridade": "Lendário",
                "tipo": "Capacete"
            }
        ],
        "equipamentos": {
            "capacete": {
                "nome": "Elmo de Ferro",
                "descricao": "Proteção pesada para a cabeça.",
                "quantidadeMaxima": 1,
                "dano": 0,
                "efeito": "Nenhum",
                "preco": 150,
                "raridade": "Comum",
                "tipo": "Capacete"
            },
            "colar": {
                "nome": "Amuleto de Rubi",
                "descricao": "Aumenta ligeiramente a sua estamina.",
                "quantidadeMaxima": 1,
                "dano": 0,
                "efeito": "Nenhum",
                "preco": 300,
                "raridade": "Raro",
                "tipo": "Colar"
            },
            "arma": {
                "nome": "Espada Longa",
                "descricao": "Uma espada de aço afiada.",
                "quantidadeMaxima": 1,
                "dano": 35,
                "efeito": "Nenhum",
                "preco": 250,
                "raridade": "Comum",
                "tipo": "Arma"
            },
            "armadura": {
                "nome": "Cota de Malha",
                "descricao": "Armadura flexível feita de anéis de metal.",
                "quantidadeMaxima": 1,
                "dano": 0,
                "efeito": "Nenhum",
                "preco": 450,
                "raridade": "Raro",
                "tipo": "Armadura"
            },
            "bota": {
                "nome": "Botas de Couro",
                "descricao": "Permite mover-se com mais silêncio.",
                "quantidadeMaxima": 1,
                "dano": 0,
                "efeito": "Nenhum",
                "preco": 80,
                "raridade": "Comum",
                "tipo": "Bota"
            },
            "anel": {
                "nome": "Anel do Falcão",
                "descricao": "Aumenta a precisão de ataques críticos.",
                "quantidadeMaxima": 1,
                "dano": 0,
                "efeito": "Nenhum",
                "preco": 500,
                "raridade": "Lendário",
                "tipo": "Anel"
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

    # 4. Inicializa e roda o jogo através do SEU GerenciadorJogo
    print("Inicializando teste com o seu GerenciadorJogo e EstadoInventario...")
    jogo = GerenciadorJogo(
        largura=800,
        altura=600,
        titulo="Testando Estado de Inventario",
        estado=dicionario_estados,
        estado_inicial="Inventario"
    )

    jogo.rodar()