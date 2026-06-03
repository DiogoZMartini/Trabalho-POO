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
        "vida": 60,
        "vidaMaxima": 100,
        "inv": [
            {
                "nome": "Poção de Cura",
                "descricao": "Recupera vida.",
                "quantidadeMaxima": 5,
                "dano": 0,
                "efeito": "Cura",
                "preco": 20,
                "raridade": "Comum",
                "tipo": "Consumivel",
                "valor_efeito": 30
            },
            {
                "nome": "Adaga de Arremesso",
                "descricao": "Causa dano à distância.",
                "quantidadeMaxima": 5,
                "dano": 15,
                "efeito": "Causa Dano",
                "preco": 40,
                "raridade": "Raro",
                "tipo": "Consumivel",
                "valor_efeito": 15
            }
        ]
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