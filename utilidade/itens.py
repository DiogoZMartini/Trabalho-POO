from tinydb import Query
from classe import Geral
import random

class Item(Geral):
    def __init__(self, nome, dano, descricao, quantidadeMaxima, efeito, preco, raridade, tipo, valorEfeito=20):
        super().__init__(nome, dano)
        self.descricao = descricao
        self.quantidadeMaxima = quantidadeMaxima
        self.efeito = efeito
        self.preco = preco
        self.raridade = raridade
        self.tipo = tipo
        self.valorEfeito = valorEfeito

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getDescricao(self):
        return self.descricao
    def getQuantidadeMaxima(self):
        return self.quantidadeMaxima
    def getEfeito(self):
        return self.efeito
    def getPreco(self):
        return self.preco
    def getRaridade(self):
        return self.raridade
    def getTipo(self):
        return self.tipo
    def getValorEfeito(self):
        return self.valorEfeito
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setDescricao(self, descricao):
        self.descricao = descricao
    def setQuantidadeMaxima(self, quantidade):
        self.quantidadeMaxima = quantidade
    def setEfeito(self, efeito):
        self.efeito = efeito
    def setPreco(self, preco):
        self.preco = preco
    def setRaridade(self, raridade):
        self.raridade = raridade
    def setTipo(self, tipo):
        self.tipo = tipo
    def setValorEfeito(self, valorEfeito):
        self.valorEfeito = valorEfeito

    def criarItemComRaridade (self,nomeBase, tipoItem, efeitoBase, valorBase):
        raridades = ["Comum", "Raro", "Épico", "Lendário"]
        chances = [70,20,8,2]
        raridadeSorteada = random.choices(raridades, weights=chances, k=1)[0]
        if raridadeSorteada == 'Comum':
            multiplicador = 1.0
        elif raridadeSorteada == "Raro":
            multiplicador = 1.5
        elif raridadeSorteada == "Épico":
            multiplicador = 2.0
        elif raridadeSorteada == "Lendário":
            multiplicador = 3.0
        valorFinal = int(valorBase * multiplicador)
        return {
            "nome": f"{nomeBase} ({raridadeSorteada})",
            "descricao": f"Um item de tipo {tipoItem} e raridade {raridadeSorteada}",
            "quantidadeMaxima": 5 if tipoItem == 'Consumivel' else 1,
            "dano": valorFinal if tipoItem == 'Espada' else 0,
            "efeito": efeitoBase,
            "preco": int(valorBase * multiplicador * 1.2),
            "raridade": raridadeSorteada,
            "tipo": tipoItem,
            "valor_efeito": valorFinal
        }

    def aplicarEfeitoItem(self,item, dadosJogador):
        tipo = item.getTipo()
        efeito = item.getEfeito()
        poderDoEfeito = item.getValorEfeito()
        if tipo == 'Consumivel':
            if efeito == 'Cura':
                vida_atual = dadosJogador['vida']
                vida_maxima = dadosJogador['vidaMaxima']
                if vida_atual >= vida_maxima:
                    print("Vida já está cheia!")
                    return False
                dadosJogador['vida'] = min(vida_maxima, vida_atual + poderDoEfeito)
                print(f"Curou! Vida atual: {dadosJogador['vida']}/{vida_maxima}")
                return True

            elif efeito == 'Segundo Ataque':
                print(f"Buff de segundo ataque ativado com {item.getNome()}!")
                return True

            elif efeito == 'Causa Dano':
                print(f"{item.getNome()} arremessada! Causará {poderDoEfeito} de dano no próximo turno.")
                return True
        return False