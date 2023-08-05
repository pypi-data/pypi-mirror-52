#!/usr/bin/env python3.6
# -*- coding: UTF-8 -*-
"""
Módulo responsável por gerenciar os Jogadores.
"""

from random import randint
from numpy import load, zeros, array
import pickle


from jogodavelhagenetico.arvorejogodavelha import ArvoreJogoDaVelha
from jogodavelhagenetico.jogadorgenetico import JogadorGenetico
from jogodavelhagenetico.ferramentas import ferramentas as frt
from jogodavelhagenetico.modelos import ARVORE, POPULACAO_NUM_X, POPULACAO_NUM_O


class Jogadores(object):

    def __init__(self, controle, posicoes):
        self.controle = controle
        self.posicoes = posicoes
        self.fim_de_partida = False
        self._vencedor = None
        self._marcacao_humano = None
        self._jogar = True

        MAPA = None
        with open(ARVORE, 'rb') as pickin:
            MAPA = pickle.load(pickin)

        POPX = load(POPULACAO_NUM_X)
        POPO = load(POPULACAO_NUM_O)
        self._jogador_x = JogadorGenetico(POPX[-1,:], 1, MAPA)
        self._jogador_o = JogadorGenetico(POPO[-1,:], -1, MAPA)

    @property
    def marcacao_humano(self):
        return "x" if self._marcacao_humano == 1 else "o"

    @property
    def marcacao_maquina(self):
        return "x" if self._marcacao_humano == -1 else "o"

    @marcacao_humano.setter
    def marcacao_humano(self, marc):
        marc = 1 if marc == "x" else -1
        self._marcacao_humano = marc

    def jogador(self):
        if self.posicoes[self.controle.pos_y][self.controle.pos_x] == " ":
            marc = "x" if self._marcacao_humano == 1 else "o"
            self.posicoes[self.controle.pos_y][self.controle.pos_x] = marc
            return True
        return False

    def robo(self):
        tabuleiro = zeros((3, 3))
        tmp = array(self.posicoes)
        tabuleiro[tmp == "o"] = -1
        tabuleiro[tmp == "x"] = 1
        if self._marcacao_humano == 1:
            i, j = self._jogador_o.jogar_em(tabuleiro)
        else:
            i, j = self._jogador_x.jogar_em(tabuleiro)

        self.posicoes[i][j] = "o" if self._marcacao_humano == 1 else "x"
        return True

    def reiniciar_robo(self):
        self._jogador_x.reiniciar()
        self._jogador_o.reiniciar()

    def __total_alinhado(self, linha):
        num_x = linha.count("x")
        num_o = linha.count("o")

        if num_x == 3:
            return "x"
        if num_o == 3:
            return "o"

        return None

    def ganhador(self):
        diagonal1 = [self.posicoes[0][0],
                     self.posicoes[1][1],
                     self.posicoes[2][2]
                     ]

        diagonal2 = [self.posicoes[0][2],
                     self.posicoes[1][1],
                     self.posicoes[2][0]
                     ]

        transposta = [[], [], []]
        for i in range(3):
            for j in range(3):
                transposta[i].append(self.posicoes[j][i])

        gan = self.__total_alinhado(diagonal1)
        if gan is not None:
            self._vencedor = gan
            return True

        gan = self.__total_alinhado(diagonal2)

        if gan is not None:
            self._vencedor = gan
            return True

        velha = 9
        for i in range(3):

            gan = self.__total_alinhado(self.posicoes[i])
            if gan is not None:
                self._vencedor = gan
                return True

            gan = self.__total_alinhado(transposta[i])
            if gan is not None:
                self._vencedor = gan
                return True

            velha -= self.posicoes[i].count("x")
            velha -= self.posicoes[i].count("o")

        if velha == 0:
            self._vencedor = "velha"
            return True

        return False

    def jogar(self):

        jogador1, jogador2 = (self.jogador, self.robo) \
                             if self._marcacao_humano == 1 else \
                             (self.robo, self.jogador)

        if self._jogar == True:
            self._jogar = jogador1()
            self.fim_de_partida = self.ganhador()

        cond = self._marcacao_humano == -1 and self.fim_de_partida is False \
               or self._jogar == True and self.fim_de_partida is False

        if cond:
            self._jogar = jogador2()
            self.fim_de_partida = self.ganhador()

    @property
    def vencedor(self):
        return self._vencedor

    @vencedor.setter
    def vencedor(self, vencedor):
        self._vencedor = vencedor
