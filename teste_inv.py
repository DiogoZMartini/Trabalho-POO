# run_teste.py
from gerenciador import GerenciadorJogo
from estados.estado_inventario import EstadoInventario
from banco import tabela_jogador
from entidades.jogador import Jogador
from tinydb import Query


def configurar_banco_para_teste():
    nome_do_alvo = "Artorias"
    tabela_jogador.remove(Query().nome == nome_do_alvo)

    tabela_jogador.insert({
        "nome": nome_do_alvo,
        "vida": 70,  # Abaixo de 100 para testar o item de cura funcional
        "vidaMaxima": 100,
        "lvl": 4,
        "recurso": 45,
        "exp": 150,
        "classe": "Guerreiro",
        "dinheiro": 420,
        "inv": [
            {
                "nome": "Poção de Vida Menor (Comum)",
                "descricao": "Uma pequena poção feita com ervas medicinais simples.",
                "quantidadeMaxima": 5,
                "efeito": "Cura",
                "preco": 10,
                "tipo": "Consumivel",
                "raridade": "Comum",
                "img": "assets/img/itens/pocaoDeVida.jpg",
                "uso": "Restaura 20 de Vida",
                "dano": 20
            },
            {
                "nome": "Poção de Vida Maior (Rara)",
                "descricao": "Um poderoso elixir alquímico destilado com lágrimas de fada.",
                "quantidadeMaxima": 5,
                "efeito": "Cura",
                "preco": 45,
                "tipo": "Consumivel",
                "raridade": "Raro",
                "img": "assets/img/itens/pocao_vida_g.png",
                "uso": "Restaura 50 de Vida",
                "dano": 50
            },
            {
                "nome": "Elixir Lendário de Fênix",
                "descricao": "Uma poção mítica capaz de curar as feridas mais profundas instantaneamente.",
                "quantidadeMaxima": 5,
                "efeito": "Cura",
                "preco": 300,
                "tipo": "Consumivel",
                "raridade": "Lendário",
                "img": "assets/img/itens/elixir_fenix.png",
                "uso": "Restaura 100 de Vida",
                "dano": 100
            },
            {
                "nome": "Adaga de Arremesso (Comum)",
                "descricao": "Uma faca balanceada perfeita para ser lançada contra inimigos distantes.",
                "quantidadeMaxima": 5,
                "efeito": "Causa Dano",
                "preco": 15,
                "tipo": "Consumivel",
                "raridade": "Comum",
                "img": "assets/img/itens/adaga_arremesso.png",
                "uso": "Arremessa causando 15 de dano",
                "dano": 15
            },
            {
                "nome": "Bomba de Pólvora (Épica)",
                "descricao": "Um artefato explosivo altamente instável que explode em contato com o alvo.",
                "quantidadeMaxima": 3,
                "efeito": "Causa Dano",
                "preco": 80,
                "tipo": "Consumivel",
                "raridade": "Épico",
                "img": "assets/img/itens/bomba.png",
                "uso": "Explode causando 45 de dano em área",
                "dano": 45
            },
            {
                "nome": "Poção de Velocidade (Rara)",
                "descricao": "Aumenta seus reflexos, permitindo desferir um golpe extra.",
                "quantidadeMaxima": 2,
                "efeito": "Segundo Ataque",
                "preco": 60,
                "tipo": "Consumivel",
                "raridade": "Raro",
                "img": "assets/img/itens/pocao_velocidade.png",
                "uso": "Seu próximo ataque é desferido 2x",
                "dano": 0
            },
            {
                "nome": "Yelmo de Dragão (Lendário)",
                "descricao": "Um capacete forjado nas chamas de um dragão ancião. Concede muita defesa.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 1200,
                "tipo": "Capacete",
                "raridade": "Lendário",
                "img": "assets/img/itens/elmo_dragao.png",
                "uso": "Aumenta muito a resistência a fogo",
                "dano": 0
            }
        ],
        "equipamentos": {
            "Capacete": {
                "nome": "Elmo de Ferro (Comum)",
                "descricao": "Proteção pesada e simples para a cabeça.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 50,
                "tipo": "Capacete",
                "raridade": "Comum",
                "img": "assets/img/itens/elmo_ferro.png",
                "uso": "+3 de armadura",
                "dano": 0
            },
            "Colar": {
                "nome": "Amuleto de Rubi (Raro)",
                "descricao": "Um colar antigo que pulsa com energia vital.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 180,
                "tipo": "Colar",
                "raridade": "Raro",
                "img": "assets/img/itens/colar_rubi.png",
                "uso": "+10 de estamina máxima",
                "dano": 0
            },
            "Arma": {
                "nome": "Espada de Aço (Épica)",
                "descricao": "Uma lâmina afiada e perfeitamente balanceada por ferreiros reais.",
                "quantidadeMaxima": 1,
                "efeito": "Aumenta o Dano",
                "preco": 250,
                "tipo": "Arma",
                "raridade": "Épico",
                "img": "assets/img/itens/espada_aco.png",
                "uso": "+25 de dano físico",
                "dano": 25
            },
            "Armadura": {
                "nome": "Cota de Malha (Comum)",
                "descricao": "Uma armadura feita de anéis de ferro interligados.",
                "quantidadeMaxima": 1,
                "efeito": "Aumenta a Defesa",
                "preco": 120,
                "tipo": "Armadura",
                "raridade": "Comum",
                "img": "assets/img/itens/armadura_malha.png",
                "uso": "+12 de defesa",
                "dano": 0
            },
            "Bota": {
                "nome": "Botas de Couro (Comum)",
                "descricao": "Permite mover-se com mais silêncio e agilidade.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 40,
                "tipo": "Bota",
                "raridade": "Comum",
                "img": "assets/img/itens/botas_couro.png",
                "uso": "+5% de velocidade de movimento",
                "dano": 0
            },
            "Anel": {
                "nome": "Anel do Falcão (Lendário)",
                "descricao": "Um anel que sintoniza a visão do usuário com a precisão de uma ave de rapina.",
                "quantidadeMaxima": 1,
                "efeito": "Nenhum",
                "preco": 500,
                "tipo": "Anel",
                "raridade": "Lendário",
                "img": "assets/img/itens/anel_falcao.png",
                "uso": "+15% de chance de acerto crítico",
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

    # 🎯 ALTERADO: Buscamos os dados recém-inseridos no TinyDB para construir o objeto Jogador real
    resultado = tabela_jogador.search(Query().nome == nome_jogador)
    dados = resultado[0]

    # Instanciando o objeto Jogador completo. O construtor dele criará o Inventario automaticamente!
    objeto_jogador = Jogador(
        nome=dados["nome"],
        dano=5,  # Dano base do personagem sem armas
        vida=dados["vida"],
        lvl=dados["lvl"],
        recurso=dados["recurso"],
        exp=dados["exp"],
        classe=dados["classe"],
        dinheiro=dados["dinheiro"]
    )

    # 🎯 ALTERADO: Passamos o OBJETO do jogador para o seu EstadoInventario, e não mais apenas o nome string.
    # Caso o seu EstadoInventario ainda espere uma string ou crie o jogador lá dentro internamente,
    # certifique-se de adaptá-lo para receber o 'objeto_jogador' e utilizar 'objeto_jogador.getInv()' para desenhar/tratar eventos.
    tela_inventario = EstadoInventario(objeto_jogador)

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