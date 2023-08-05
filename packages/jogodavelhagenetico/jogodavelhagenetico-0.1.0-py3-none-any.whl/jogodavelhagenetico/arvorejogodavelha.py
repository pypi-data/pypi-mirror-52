#!/usr/bin/env python3.6
#-*- Coding: UTF-8 -*-
"""
Arvore de possibilidades do jogo da velha.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from .ferramentas import ferramentas as frt


class ArvoreJogoDaVelha:
    """
    Arvore de possibilidades do jogo da velha com
    remoção de elementos simétricos.
    """
    def __init__(self):
        """
        Arvore de possibilidades do jogo da velha com
        remoção de elementos simétricos.
        """
        self._no = None
        self._mae = None
        self._folhas = []
        self._jogador = None
        self.ganhador = None
        self._altura = 0

    @property
    def mae(self):
        '''
        Retorna o nó mãe.
        '''
        return self._mae

    @mae.setter
    def mae(self, mae):
        '''
        Define o nó mãe.
        '''
        if self._mae is None:
            self._mae = mae
    @property
    def jogador(self):
        '''
        Retorna o valor do jogador no nó.
        '''
        return self._jogador

    @jogador.setter
    def jogador(self, jogador):
        '''
        Define o valor do jogador no nó.
        '''
        if self._jogador is None:
            self._jogador = jogador

    @property
    def no(self):
        '''
        Retorna o valor do no.
        '''
        return self._no

    @no.setter
    def no(self, no):
        '''
        Define o valor do nó.
        '''
        if self._no is None:
            self._no = no

    @property
    def folhas(self):
        '''
        retorna a lista de folhas.
        '''
        return self._folhas

    @folhas.setter
    def folhas(self, folha):
        '''
        Adicionar uma nova folha ao ramo.
        '''
        self._folhas.append(folha)

    def folha_em_no(self, folha, no):
        """
        Verifica se uma dada folha está no ramo de um nó.
        """
        for f in no.folhas:
            if folha == f.no:
                return True
        return False

    def ramo_equivalente(self, folha):
        """
        Verifica e retorna, se existir, um nó equivalente nos ramos
        de folhas correntes do nó atual.
        """
        for f in self.folhas:
            equ = self.equivalente(f.no, folha)
            if equ[0] is True:
                return f, equ
        return None

    def equivalente(self, folha1, folha2):
        '''
        Verifica se duas folhas são equivalentes.
        Entrada:
            folha1: tupla representando uma jogada
            folha2: tupla representando uma jogada
        Saída:
            Boleano: Verdadeiro para encontrado, Falso para o contrário
            inteiro: grau de rotação
            Boleano: Rotação flip
            Boleano: Rotação flipud
            Boleano: Rotação fliplr
        '''
        if folha1 == folha2:
            return True, 0, False, False, False


        for q in range(1, 9):
            tb = frt.emtabela(folha2)
            tmp = frt.emtupla(frt.girar(tb, q, False, False, False))
            tbflip = frt.emtupla(frt.girar(tb, q, False, False, True))
            tbflipud = frt.emtupla(frt.girar(tb, q, False, True, False))
            tbfliplr = frt.emtupla(frt.girar(tb, q, True, False, False))

            a = tmp == folha1
            if a == True:
                return True, q , False, False, False

            b = tbflip == folha1

            if b == True:
                return True, q , b, False, False

            c = tbflipud == folha1

            if c == True:
                return True, q , b, c, False

            d = tbfliplr == folha1

            if d == True:
                return True, q , b, c, d

        return False, 0, False, False, False

    def buscar_profundidade(self, folha):
        """
        Realiza a busca em profundidade por um nó que tem equivalencia a folha
        de entrada.
        """
        if self._no == folha:
            return self

        for no in self.folhas:
            if self.folha_em_no(folha, no):
                return no, (True, 0, False, False, False)

            encontrado = self.equivalente(no.no, folha)
            if encontrado[0] == True:
                return no, encontrado
            no.buscar_profundidade(folha)


    def buscar_folha(self, folha):
        """
        Realiza a busca em largura  por um nó que tem equivalencia a folha
        de entrada.
        """
        if self._no == folha:
            return self

        visitar = self.folhas
        while len(visitar) > 0:
            visitado = visitar[0]
            visitar.pop(0)
            encontrado = self.equivalente(visitado.no, folha)
            if encontrado[0] == True:
                return visitado, encontrado
            visitar += visitado.folhas
        return None
