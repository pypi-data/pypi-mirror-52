#!/usr/bin/env python3.6
#-*- Coding: UTF-8 -*-
"""
Funções auxiliares.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
from numpy import array,flip, flipud, fliplr, where, roll
from random import choice

class ferramentas:
    '''
    Classe contendo métodos estáticos para auxiliar na manipulação de jogos da
    velha.
    '''
    @staticmethod
    def girar_centro(tabela, q):
        """
        Rotacionar uma matriz 3x3 a partir do centro.
        Entrada:
            tabela: matriz 3x3
            q: inteiro representando passo de rotação.
        """
        i = array([0, 1, 2, 5, 8, 7, 6, 3])
        tabela.flat[i] = roll(tabela.flat[i], q)
        return tabela

    @staticmethod
    def girar_oposto(tabuleiro, q, fp, fud, flr):
        """
        Gira a matriz no sentido reverso.
        """
        tmp = tabuleiro.copy()
        if fp:
            tmp = flip(tmp)
        if fud:
            tmp = flipud(tmp)
        if flr:
            tmp = fliplr(tmp)

        tmp = ferramentas.girar_centro(tmp, 8 - q)
        return tmp

    @staticmethod
    def girar(tabuleiro, q, flr, fud, fp):
        """
        Gira e espelha a matriz de acordo com os parâmetros de entrada.
        """
        tmp = ferramentas.girar_centro(tabuleiro.copy(), q)
        if flr:
            tmp = fliplr(tmp)
        if fud:
            tmp = flipud(tmp)
        if fp:
            tmp = flip(tmp)
        return tmp

    @staticmethod
    def emlista(tabuleiro):
        """
        Converte matriz tabuleiro en uma lista plana.
        Entrada:
            tabuleiro: matriz 3x3.
        """
        return tabuleiro.reshape((1, 9)).tolist()[0]

    @staticmethod
    def emtupla(tabuleiro):
        """
        Converte matriz tabuleiro en uma tupla plana.
        Entrada:
            tabuleiro: matriz 3x3.
        """
        return tuple(ferramentas.emlista(tabuleiro))

    @staticmethod
    def emtabela(tabuleiro):
        """
        Converte uma lista plana numa matriz 3x3 representando o tabuleiro.
        """
        return array(tabuleiro).reshape((3, 3))

    @staticmethod
    def jogadas_possiveis(tabuleiro, jogador, vazio):
        """
        Retorna uma lista de todas as jogadas possíveis, para um dado estado
        do tabuleiro e um dado jogador.
        """
        p = where(tabuleiro == vazio)
        p = zip(p[0], p[1])
        possiveis = []
        for i, j in p:
            tbl = tabuleiro.copy()
            fim, ganhador = ferramentas.jogo_finalizado(tbl)
            if fim == False:
                tbl[i, j] = jogador
                possiveis.append(tuple(ferramentas.emlista(tbl)))
        return possiveis

    @staticmethod
    def jogo_finalizado(tabuleiro):
        """
        Verifica se a partida foi finalizada e qual o ganhador.
        Entrada:
            tabuleiro: matriz 3x3 representando o jogo atual.
            jogador: representa o jogador atual.
        """
        diag0 = tabuleiro.diagonal()
        if abs(diag0.sum()) == 3:
            ganhador =  tabuleiro[0, 0]
            return True, ganhador

        ft = fliplr(tabuleiro)
        diag1 = ft.diagonal()
        if abs(diag1.sum()) == 3:
            ganhador = ft[0,0]
            return True, ganhador

        coluna = abs(tabuleiro.sum(axis=0)) == 3
        fim = [(0, j) for j in range(3) if coluna[j]]
        if fim:
            return True, tabuleiro[fim[0]]

        linha = abs(tabuleiro.sum(axis=1)) == 3
        fim = [(i, 0) for i in range(3) if linha[i]]
        if fim:
            return True, tabuleiro[fim[0]]

        if (tabuleiro != 0).all():
            ganhador =  0
            return True, ganhador

        return False, None

    @staticmethod
    def jogada_aleatoria_p(tabuleiro, vazio=0):
        '''
        Escolhe aleatoriamente uma posição vazia no tabuleiro.
        Dando prioridade para posições de fechamento.
        '''
        diag0 = tabuleiro.diagonal()
        if abs(diag0.sum()) == 2:
            for p in [(0, 0), (1, 1), (2,2)]:
                if tabuleiro[p] == 0:
                    return p

        ft = fliplr(tabuleiro)
        diag1 = ft.diagonal()
        if abs(diag1.sum()) == 2:
            for p in [(0, 2), (1, 1), (2,0)]:
                if tabuleiro[p] == 0:
                    return p

        for i in range(3):
            c = tabuleiro[:, i]
            if c.sum() == 2:
                for p in [(0, i), (1, i), (2, i)]:
                    if tabuleiro[p] == 0:
                        return p
            l = tabuleiro[i, :]
            if l.sum() == 2:
                for p in [(i, 0), (i, 1), (i, 2)]:
                    if tabuleiro[p] == 0:
                        return p

        return ferramentas.jogada_aleatoria(tabuleiro, vazio)


    @staticmethod
    def jogada_aleatoria(tabuleiro, vazio=0):
        '''
        Escolhe aleatoriamente uma posição vazia no tabuleiro.
        '''
        null = tabuleiro == 0
        f = where(null == True)
        f = list(zip(f[0], f[1]))
        p = choice(f)
        return tuple(p)
