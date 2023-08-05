#!/usr/bin/env python3.6
#-*- Coding: UTF-8 -*-
"""
Gerador de Arvore de possibilidades do jogo da velha com
remoção de elementos simétricos.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
import pickle
import os
from numpy import array
from numpy import flip, flipud, fliplr, array, rot90

from .arvorejogodavelha import ArvoreJogoDaVelha
from .ferramentas import ferramentas as frt


class GeradorDeArvore:
    """
    Gerador de Arvore de possibilidades do jogo da velha com
    remoção de elementos simétricos.
    """

    def __init__(self, primeiro=1, segundo=-1, vazio=0):
        self._raiz = ArvoreJogoDaVelha()
        self._primeiro = primeiro
        self._segundo = segundo
        self._vazio = vazio

        tabuleiro = array(3 * [3 * [self._vazio]])
        self._raiz.no = tuple(frt.emlista(tabuleiro))
        self._raiz.jogador = self._primeiro

    def carregar(self, caminho):
        """
        Carrega uma árvore previamente salva.
        """
        diretorio = "/".join(caminho.split("/")[:-1])
        if os.path.isdir(diretorio) is False:
            os.mkdir(diretorio)

        if os.path.isfile(caminho) == True:
            with open(caminho, 'rb') as pickin:
                arvore = pickle.load(pickin)
            return arvore

        print("Gerando árvore, aguarde.")

        return self.gerador(salvar=caminho)

    def simetricas(self, tabuleiros):
        '''
        Reduz um conjunto de tabuleiros aos simétricos
        '''
        eq = []
        adicionados = []
        li = 0
        ntab = len(tabuleiros)

        def append(tb):
            if tb in tabuleiros:
                idx = tabuleiros.index(tb)
                if idx in adicionados:
                    return

                if li != idx:
                    cmp = (li, tabuleiros.index(tb))
                    if li not in adicionados:
                        adicionados.append(li)
                    adicionados.append(cmp[1])
                    if cmp not in eq:
                        eq.append(cmp)

        for tabuleiro in tabuleiros:
            tb = frt.emtabela(tabuleiro)

            for q in range(0, 8):

                tmp = frt.emtupla(frt.girar(tb, q, False, False, False))
                tbflip = frt.emtupla(frt.girar(tb, q, False, False, True))
                tbflipud = frt.emtupla(frt.girar(tb, q, False, True, False))
                tbfliplr = frt.emtupla(frt.girar(tb, q, True, False, False))

                append(tmp)
                append(tbflip)
                append(tbflipud)
                append(tbfliplr)

            li += 1
        if eq:
            eq = array(eq)
            remover = list(eq[:, 1])
            remover.sort()
            return remover
        return []

    def gerador(self, salvar=None):
        """
        Gerador de árvore de jogo da velha, baseado em busca em largura.
        """
        visitar = [self._raiz]
        total = 0
        x = 0
        o = 0
        n = 0
        while len(visitar) > 0:

            visitando = visitar[0]

            tabuleiro = frt.emtabela(visitando.no)

            jogador = visitando.jogador
            visitar.pop(0)
            fim, ganhador = frt.jogo_finalizado(tabuleiro)

            if fim == False:
                total += 1
                possiveis = frt.jogadas_possiveis(tabuleiro,
                                                  jogador,
                                                  self._vazio)

                jogador = self._segundo if jogador == self._primeiro \
                                        else self._primeiro

                noadd = self.simetricas(possiveis)
                pi = 0
                for possivel in possiveis:
                    if pi not in noadd:
                        tmp = ArvoreJogoDaVelha()
                        tmp.no = possivel
                        tmp.mae = visitando
                        tmp.jogador = jogador
                        visitando.folhas = tmp
                        visitar.append(tmp)
                    pi += 1
            else:

                if ganhador == -1:
                    o += 1
                elif ganhador == 1:
                    x += 1
                else:
                    n += 1

        if salvar is not None:
            with open(salvar, "wb") as pickle_out:
                pickle.dump(self._raiz, pickle_out)

        print("Total: {0}. Vitorias de - X: {1}, O: {2}, V: {3}".format(total,
                                                                        x,
                                                                        o,
                                                                        n))

    def print(self, no):
        '''
        Imprime os galhos de uma árvore a partir de um nó.
        Entrada:
            no: nó da árvore de jogadas.
        '''
        if no.folhas:
            print("\n\n")
            print(5 * "-*-")
            print("no")
            print(array(no.no).reshape((3, 3)))
            print("Jogador {}".format(no.jogador))
            print("Ganhador {}".format(no.ganhador))
            print("Folhas {}".format(len(no.folhas)))
            for folha in no.folhas:
                print("\n")
                print("Ganhador {}".format(folha.ganhador))
                print(array(folha.no).reshape((3, 3)))
            input("Enter para seguir.")

            for folha in no.folhas:
                self.print(folha)

    @property
    def raiz(self):
        return self._raiz

    @property
    def primeiro(self):
        '''
        Valor que representa o primeiro jogador (X).
        '''
        return self._primeiro

    @property
    def segundo(self):
        '''
        Valor que representa o segund jogador (O).
        '''
        return self._segundo

    @property
    def vazio(self):
        '''
        Valor que representa casa vazia jogador ( ).
        '''
        return self._vazio
