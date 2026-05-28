class Geral:
    def __init__(self, nome, dano):
        self.nome = nome
        self.dano = dano

    def getNome(self):
        return self.nome
    def getDano(self):
        return self.dano
    def setNome(self, nome):
        self.nome = nome
    def setDano(self, dano):
        self.dano = dano

class Item(Geral):
    def __init__(self, nome, dano, descricao, quantidade, efeito, preco, raridade, tipo):
        super().__init__(nome, dano)
        self.descricao = descricao
        self.quantidade = quantidade
        self.efeito = efeito
        self.preco = preco
        self.raridade = raridade
        self.tipo = tipo

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getDescricao(self):
        return self.descricao
    def getQuantidade(self):
        return self.quantidade
    def getEfeito(self):
        return self.efeito
    def getPreco(self):
        return self.preco
    def getRaridade(self):
        return self.raridade
    def getTipo(self):
        return self.tipo
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setDescricao(self, descricao):
        self.descricao = descricao
    def setQuantidade(self, quantidade):
        self.quantidade = quantidade
    def setEfeito(self, efeito):
        self.efeito = efeito
    def setPreco(self, preco):
        self.preco = preco
    def setRaridade(self, raridade):
        self.raridade = raridade
    def setTipo(self, tipo):
        self.tipo = tipo

    def aleatorizarRaridade(self):
        pass


class Persongaem(Geral):
    def __init__(self, nome, dano, vida, lvl, recurso):
        super().__init__(nome, dano)
        self.vida = vida
        self.lvl = lvl
        self.recurso = recurso

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return self.vida
    def getLvl(self):
        return self.lvl
    def getRecurso(self):
        return self.recurso
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setVida(self, vida):
        self.vida = vida
    def setLvl(self, lvl):
        self.lvl = lvl
    def setRecurso(self, recurso):
        self.recurso = recurso

    def ataque(self, dano):
        pass
    def ataqueSpe(self, dano):
        pass
    def curarVida(self, dano):
        pass
    def tomarDano(self, dano):
        pass

class Jogador(Persongaem):
    def __init__(self, nome, dano, vida, lvl, recurso, exp, classe, dinheiro):
        super().__init__(nome, dano, vida, lvl, recurso)
        self.exp = exp
        self.classe = classe
        self.inv = []
        self.dinheiro = dinheiro

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return super().getVida()
    def getLvl(self):
        return super().getLvl()
    def getRecurso(self):
        return super().getRecurso()
    def getExp(self):
        return self.exp
    def getClasse(self):
        return self.classe
    def getInv(self):
        return self.inv
    def getDinheiro(self):
        return self.dinheiro
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setVida(self, vida):
        super().setVida(vida)
    def setLvl(self, lvl):
        super().setLvl(lvl)
    def setRecurso(self, recurso):
        super().setRecurso(recurso)
    def setExp(self, exp):
        self.exp = exp
    def setClasse(self, classe):
        self.classe = classe
    def setInv(self, inv):
        self.inv = inv
    def setDinheiro(self, dinheiro):
        self.dinheiro = dinheiro

    def ataque(self, dano):
        super().ataque(dano)
    def ataqueSpe(self, dano):
        super().ataqueSpe(dano)
    def curarVida(self, dano):
        super().curarVida(dano)
    def tomarDano(self, dano):
        super().tomarDano(dano)
    def removerItem(self, item):
        self.inv.remove(item)
    def addItem(self, item):
        self.inv.append(item)
    def usarItem(self, item):
        pass

class Inimigo (Persongaem):
    def __init__(self, nome, dano, vida, lvl, recurso, dropExp, dropDinheiro):
        super().__init__(nome, dano, vida, lvl, recurso)
        self.dropExp = dropExp
        self.dropItem = []
        self.dropDinheiro = dropDinheiro

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return super().getVida()
    def getLvl(self):
        return super().getLvl()
    def getRecurso(self):
        return super().getRecurso()
    def getDropExp(self):
        return self.dropExp
    def getDropItem(self):
        return self.dropItem
    def getDropDinheiro(self):
        return self.dropDinheiro
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setVida(self, vida):
        super().setVida(vida)
    def setLvl(self, lvl):
        super().setLvl(lvl)
    def setRecurso(self, recurso):
        super().setRecurso(recurso)
    def setDropExp(self, dropexp):
        self.dropExp = dropexp
    def setDropItem(self, dropitem):
        self.dropItem = dropitem
    def setDropDinheiro(self, dropdinheiro):
        self.dropDinheiro = dropdinheiro

    def ataque(self, dano):
        super().ataque(dano)
    def ataqueSpe(self, dano):
        super().ataqueSpe(dano)
    def curarVida(self, dano):
        super().curarVida(dano)
    def tomarDano(self, dano):
        super().tomarDano(dano)
    def expDropado(self):
        pass
    def expDropItem(self):
        pass
    def expDropDinheiro(self):
        pass

class Mercador(Inimigo):
    def __init__(self, nome, dano, vida, lvl, recurso, dropExp, dropdinheiro):
        super().__init__(nome, dano, vida, lvl, recurso, dropExp, dropdinheiro)
        self.mercadoria = []

    def getNome(self):
        return super().getNome()
    def getDano(self):
        return super().getDano()
    def getVida(self):
        return super().getVida()
    def getLvl(self):
        return super().getLvl()
    def getRecurso(self):
        return super().getRecurso()
    def getDropExp(self):
        return super().getDropExp()
    def getDropItem(self):
        return super().getDropItem()
    def getDropDinheiro(self):
        return super().getDropDinheiro()
    def getMercadoria(self):
        return self.mercadoria
    def setNome(self, nome):
        super().setNome(nome)
    def setDano(self, dano):
        super().setDano(dano)
    def setVida(self, vida):
        super().setVida(vida)
    def setLvl(self, lvl):
        super().setLvl(lvl)
    def setRecurso(self, recurso):
        super().setRecurso(recurso)
    def setDropExp(self, dropexp):
        super().setDropExp(dropexp)
    def setDropItem(self, dropitem):
        super().setDropItem(dropitem)
    def setDropDinheiro(self, dropdinheiro):
        super().setDropDinheiro(dropdinheiro)
    def setMercadoria(self, mercadoria):
        self.mercadoria = mercadoria

    def ataque(self, dano):
        super().ataque(dano)
    def ataqueSpe(self, dano):
        super().ataqueSpe(dano)
    def curarVida(self, dano):
        super().curarVida(dano)
    def tomarDano(self, dano):
        super().tomarDano(dano)
    def expDropado(self):
        super().expDropado()
    def expDropItem(self):
        super().expDropItem()
    def expDropDinheiro(self):
        super().expDropDinheiro()
    def comparItem(self, item, dinheiro, inv, mercadoria):
        pass
    def venderItem(self, item, dinheiro, inv, mercadoria):
        pass






