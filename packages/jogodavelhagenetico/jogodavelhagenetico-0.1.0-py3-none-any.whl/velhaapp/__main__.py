#!/usr/bin/env python3.6
# -*- coding: UTF-8 -*-
"""
Módulo principal do Jogo
"""

from curses import initscr, wrapper
from random import randint
from .tela import Tela
from .controle import Controle
from .jogadores import Jogadores

def jogo(stdscr):
    posicoes = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    controle = Controle(stdscr=stdscr)
    tela = Tela(stdscr=stdscr, posicoes=posicoes)
    jogadores = Jogadores(controle=controle, posicoes=posicoes)
    tela.reiniciar_tela()

    jogador_humano = 0
    jogador_maquina = 0

    jogadores.marcacao_humano = "o" if randint(0, 1) == 0 else "x"
    jmaqui = True if jogadores.marcacao_humano == "o" else False

    while True:

        if jmaqui is True:
            jmaqui = False
            jogadores.jogar()
            tela.tabuleiro(controle)
            if jogadores.fim_de_partida is True:
                if jogadores.vencedor == jogadores.marcacao_humano:
                    jogador_humano += 1
                if jogadores.vencedor == jogadores.marcacao_maquina:
                    jogador_maquina += 1

        controle.espaco_do_tabuleiro()
        if jogadores.fim_de_partida is False:
            if controle.entrada == "\n":
                jogadores.jogar()
                jmaqui = True if jogadores.marcacao_humano == "o" else False

            if jogadores.fim_de_partida is True:
                if jogadores.vencedor == jogadores.marcacao_humano:
                    jogador_humano += 1
                if jogadores.vencedor == jogadores.marcacao_maquina:
                    jogador_maquina += 1


        if controle.entrada == 'h':
            tela.ajuda()
        else:
            tela.tabuleiro(controle)
            tela.placar(jogador_humano, jogador_maquina)
            if jogadores.fim_de_partida is True:
                tela.fim_de_jogo(jogadores.vencedor)
            controle.cursor()


        if controle.entrada == "y":

            for i in range(3):
                for j in range(3):
                    posicoes[i][j] = " "

            controle.pos_y = 0
            controle.pos_x = 0
            jogadores.vencedor = None
            jogadores.reiniciar_robo()
            jogadores.marcacao_humano = "o" if randint(0, 1) == 0 else "x"
            jmaqui = True if jogadores.marcacao_humano == "o" else False
            jogadores.fim_de_partida = False
            tela.reiniciar_tela()




def main():
    initscr()
    wrapper(jogo)
