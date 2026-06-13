from classe import Geral
from banco import tabela_itens
import random


class Item(Geral):
    def __init__(self, nome, dano, descricao, quantidadeMaxima, efeito, preco, raridade, tipo, img=None,
                 uso=None):
        super().__init__(nome, dano)
        self.descricao = descricao
        self.quantidadeMaxima = quantidadeMaxima
        self.efeito = efeito
        self.preco = preco
        self.raridade = raridade
        self.tipo = tipo
        self.img = img
        self.uso = uso

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
    def getImg(self):
        return self.img
    def getUso(self):
        return self.uso
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
    def setImg(self, img):
        self.img = img
    def setUso(self, uso):
        self.uso = uso

    @classmethod
    def gerarItemAleatorio(cls, lvlInimigo):
        todosItensCatalogo = tabela_itens.all()
        if not todosItensCatalogo:
            return cls.criarItemComRaridade("Poção de Vida", "Consumivel", "Cura", 10 + lvlInimigo * 5)
        dadosItemBanco = random.choice(todosItensCatalogo)
        # Passa o dano/valor original do banco para a sua função de raridade
        itemFinal = cls.criarItemComRaridade(
            nomeBase=dadosItemBanco['nome'],
            tipoItem=dadosItemBanco['tipo'],
            efeitoBase=dadosItemBanco['efeito'],
            valorBase=dadosItemBanco['dano']
        )
        # o preço calculado por lá pode ficar negativo. Aqui garantimos que seja positivo)
        if itemFinal.getPreco() < 0:
            itemFinal.setPreco(abs(itemFinal.getPreco()))
        # Preserva o resto das informações customizadas que você cadastrou no banco
        itemFinal.setDescricao(dadosItemBanco['descricao'])
        itemFinal.setQuantidadeMaxima(dadosItemBanco['quantidadeMaxima'])
        itemFinal.setImg(dadosItemBanco.get('img', None))
        itemFinal.setUso(dadosItemBanco.get('uso', 'Sem uso definido'))
        return itemFinal

    @classmethod
    def criarItemComRaridade(cls, nomeBase, tipoItem, efeitoBase, valorBase):
        raridades = ["Comum", "Raro", "Épico", "Lendário"]
        chances = [70, 20, 8, 2]
        raridadeSorteada = random.choices(raridades, weights=chances, k=1)[0]
        multiplicadores = {"Comum": 1.0, "Raro": 1.5, "Épico": 2.0, "Lendário": 3.0}
        multiplicador = multiplicadores[raridadeSorteada]
        valorFinal = int(valorBase * multiplicador)
        qtdMax = 5 if tipoItem == 'Consumivel' else 1
        return cls(
            nome=f"{nomeBase} ({raridadeSorteada})",
            dano=valorFinal,
            descricao=f"Um item de tipo {tipoItem} e raridade {raridadeSorteada}",
            quantidadeMaxima=qtdMax,
            efeito=efeitoBase,
            preco=int(valorBase * multiplicador * 1.2),
            raridade=raridadeSorteada,
            tipo=tipoItem,
        )

    def aplicarEfeitoItem(self, dadosJogador):
        tipo = self.getTipo()
        efeito = self.getEfeito()
        if tipo == 'Consumivel':
            if efeito == 'Cura':
                poderCura = self.getDano()
                vida_atual = dadosJogador.get('vida', 0)
                vida_maxima = dadosJogador.get('vidaMaxima', 100)
                if vida_atual >= vida_maxima:
                    print("Vida já está cheia!")
                    return False
                dadosJogador['vida'] = min(vida_maxima, vida_atual + poderCura)
                print(f"Curou! Vida atual: {dadosJogador['vida']}/{vida_maxima} (Recuperou {poderCura} PV)")
                return True
            elif efeito == 'Segundo Ataque':
                print(f"Buff de segundo ataque ativado com {self.getNome()}!")
                return True
            elif efeito == 'Causa Dano':
                print(f"{self.getNome()} arremessada! Causará {self.getDano()} de dano no próximo turno.")
                return True
        return False