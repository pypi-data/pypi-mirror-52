#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Classe que usa código genético para definir estratégias para jogo da velha.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy import where, array, arange, fliplr
from numpy.random import choice
from random import randint
import matplotlib.pyplot as plt
from math import floor

from .ferramentas import ferramentas as frt
from .ferramentas import ferramentas as frt
from .arvorejogodavelha import ArvoreJogoDaVelha
import time


class JogadorGenetico:
    '''
    Classe que usa código genético para definir estratégias para jogo da velha.
    '''
    def __init__(self, dna, marcacao, arvore, limiar=1.0, x=1, o=-1, vazio=0):
        self._marcacao = marcacao
        self._arvore = arvore
        self._dna = dna
        self._x = x
        self._o = o
        self._vazio = vazio
        self._no_atual = arvore
        self._fim = 0
        self._inicio = 0
        self._limiar = limiar

    @property
    def marcacao(self):
        """
        Retorna o valor representando a marcação do jogador genético.
        """
        return self._marcacao

    def _fim_prematuro(self, tabuleiro):
        """
        Verifica se o tabuleiro já está no estado de jogada finalizável.
        """
        np = tabuleiro[tabuleiro == 0].size
        ps = where(tabuleiro == 0)
        ps = list(zip(ps[0], ps[1]))
        self._inicio += self._fim
        self._fim = self._inicio + np
        posicoes = self._dna[self._inicio:self._fim]
        prob = posicoes[posicoes >= self._limiar * posicoes.max()]
        esc = where(posicoes == posicoes.max())
        escolha = ps[esc[0][0]]
        return escolha

    def avaliar_tabuleiro(self, tabuleiro):
        """
        Condição de contorno. Avalia se uma das condições de contorno
        de finalização de jogadas foi alcançada.
        """
        ps = []

        diag0 = tabuleiro.diagonal()
        soma = diag0.sum()
        if abs(soma) == 2:
            for p in [(0, 0), (1, 1), (2,2)]:
                if tabuleiro[p] == 0:
                    ps.append(p)
                    if soma // abs(soma) == self._marcacao:
                        return [p]

        ft = fliplr(tabuleiro)
        diag1 = ft.diagonal()
        soma = diag1.sum()
        if abs(soma) == 2:
            for p in [(0, 2), (1, 1), (2,0)]:
                if tabuleiro[p] == 0:
                    ps.append(p)
                    if soma // abs(soma) == self._marcacao:
                        return [p]

        for i in range(3):
            c = tabuleiro[:, i]
            soma = c.sum()
            if abs(c.sum()) == 2:
                for p in [(0, i), (1, i), (2, i)]:
                    if tabuleiro[p] == 0:
                        ps.append(p)
                        if soma // abs(soma) == self._marcacao:
                            return [p]

            l = tabuleiro[i, :]
            soma = l.sum()
            if abs(l.sum()) == 2:
                for p in [(i, 0), (i, 1), (i, 2)]:
                    if tabuleiro[p] == 0:
                        ps.append(p)
                        if soma // abs(soma) == self._marcacao:
                            return [p]

        return ps

    def reiniciar(self):
        self._no_atual = self._arvore
        self._fim = 0
        self._inicio = 0

    def jogar_em(self, tabuleiro):
        """
        Retorna uma posição a ser jogada a partir de um estado do tabuleiro.
        """
        tabuleiro = tabuleiro.copy()
        tb = frt.emtupla(tabuleiro)
        if tb == (0, 0, 0, 0, 0, 0, 0, 0, 0):
            nfolhas = len(self._no_atual.folhas)
            self._inicio += self._fim
            self._fim = self._inicio + nfolhas
            #Define as probabilidades de escolher uma folha.
            posicoes = self._dna[self._inicio:self._fim]
            esc = where(posicoes == posicoes.max())[0][0]

            self._no_atual = self._no_atual.folhas[esc]
            folha = frt.emtabela(self._no_atual.no)

            escolher = where(folha != tabuleiro)
            escolher = (escolher[0][0], escolher[1][0])

            return escolher


        encontrado = self._no_atual.ramo_equivalente(tb)

        teste = frt.jogo_finalizado(frt.emtabela(self._no_atual.no))

        if teste[0] is True and encontrado is None:
            return self._fim_prematuro(tabuleiro)

        self._no_atual = encontrado[0]

        nfolhas = len(self._no_atual.folhas)
        if nfolhas == 0:
            return self._fim_prematuro(tabuleiro)

        finalizaveis = self.avaliar_tabuleiro(tabuleiro)
        nfin = len(finalizaveis)
        if nfin == 1:
            tb = tabuleiro.copy()
            tb[finalizaveis[0]] = self._marcacao
            tb = frt.emtupla(tb)
            encontrado = self._no_atual.ramo_equivalente(tb)
            self._no_atual = encontrado[0]
            return finalizaveis[0]

        if nfin >= 2:
            self._inicio += self._fim
            self._fim = self._inicio + nfin
            #Define as probabilidades de escolher uma folha.
            posicoes = self._dna[self._inicio:self._fim]
            esc = where(posicoes == posicoes.max())[0][0]
            tb = tabuleiro.copy()
            tb[finalizaveis[esc]] = self._marcacao
            tb = frt.emtupla(tb)
            encontrado = self._no_atual.ramo_equivalente(tb)
            self._no_atual = encontrado[0]
            return finalizaveis[esc]

        self._inicio += self._fim
        self._fim = self._inicio + nfolhas
        #Define as probabilidades de escolher uma folha.
        posicoes = self._dna[self._inicio:self._fim]

        prob = posicoes[posicoes >= self._limiar * posicoes.max()]

        #Escolhe uma folha de acordo com o mapa de probabilidades
        if prob.size == 1:
            escolha = where(posicoes == prob[0])
        elif prob.size == 0:
            escolha = where(posicoes == posicoes.max())
        else:
            escolha = where(posicoes == choice(prob))

        escolha = escolha[0][0]
        self._no_atual = self._no_atual.folhas[escolha]

        q, fp, fpud, fplr = encontrado[1][1:]

        folha = frt.emtabela(self._no_atual.no)
        folha = frt.girar_oposto(folha, q, fp, fpud, fplr)

        escolher = where(folha != tabuleiro)
        escolher = (escolher[0][0], escolher[1][0])

        return escolher
