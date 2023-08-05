#!/usr/bin/env python3.6
#-*- Coding: UTF-8 -*-
"""
Arvore de possibilidades do jogo da velha.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
import time
import pickle

from numpy import zeros, hsplit, concatenate, array, save, load
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from pathos.helpers import cpu_count
from pathos.multiprocessing import ProcessPool

from pygenec.populacao import Populacao

from pygenec.selecao.torneio import Torneio
from pygenec.selecao.classificacao import Classificacao

from pygenec.cruzamento.embaralhamento import Embaralhamento

from pygenec.mutacao.sequenciareversa import SequenciaReversa
from pygenec.evolucao import Evolucao
from pygenec import binarray2int

from .geradordearvore import GeradorDeArvore
from .arvorejogodavelha import ArvoreJogoDaVelha
from .jogadorgenetico import JogadorGenetico
from .ferramentas import ferramentas as frt


def salvar_probabilidades(saida, populacao, cromossomos, bits):

    def valores(populacao):
        bx = hsplit(populacao, cromossomos)
        const = 2 ** bits - 1
        const = 1.0 / const
        x = [const * binarray2int(xi) for xi in bx]
        x =  concatenate(x).T
        return x

    x = valores(populacao)
    save(saida, x)

def main(arvore_velha, dir_pop, dir_fig):
    '''
    Função de Treinamento do Alogirtmo de Jogo da Velha.
    '''

    with open(arvore_velha, 'rb') as pickin:
        MAPA = pickle.load(pickin)

    LIMIAR = 1.0
    cromossomos = 60
    tamanho_populacao = 100
    tamanho = int(0.1 * tamanho_populacao) if tamanho_populacao > 20 else 5

    bits = 7
    genes = bits * cromossomos
    pmut = 0.15
    pcruz = 0.6
    epidemia = None
    elitista = True

    def valores(populacao):
        bx = hsplit(populacao, cromossomos)
        const = 2 ** bits - 1
        const = 1.0 / const
        x = [const * binarray2int(xi) for xi in bx]
        x =  concatenate(x).T
        return x


    def jogar(individuo, verbose=False, humano=False):
        tabuleiro = zeros((3,3), dtype=int)
        marcacao = 1
        jogador = JogadorGenetico(individuo, marcacao,
                                  MAPA,
                                  limiar=LIMIAR)

        jog1, jog2 = (frt.jogada_aleatoria_p, jogador.jogar_em) \
                      if marcacao == -1 \
                      else (jogador.jogar_em, frt.jogada_aleatoria_p)

        while True:

            p1 = jog1(tabuleiro)

            tabuleiro[p1] = 1
            fim, ganhador = frt.jogo_finalizado(tabuleiro)

            if fim is True:
                break
            p2 = jog2(tabuleiro)
            if p2 is None:
                return None

            tabuleiro[p2] = -1

            fim, ganhador = frt.jogo_finalizado(tabuleiro)


            if fim is True:
                break

        if ganhador == marcacao:
            return 1
        elif ganhador == 0:
            return 0
        else:
            return -1

    def avaliacao(populacao):
        x = valores(populacao)
        npop = len(populacao)

        def steps(k):
            individuo = x[k, :]
            gnd = 0
            for i in range(30):
                gnd += jogar(individuo)

            return gnd

        peso = None
        ncpu = 12
        with ProcessPool(nodes=ncpu) as pool:
            p = pool.map(steps, list(range(npop)))
            peso = array(p)
        return peso

    populacao = Populacao(avaliacao,
                               genes,
                               tamanho_populacao)



    selecao = Classificacao(populacao)
    cruzamento = Embaralhamento(tamanho_populacao)
    mutacao = SequenciaReversa(pmut=pmut)

    evolucao = Evolucao(populacao,
                             selecao,
                             cruzamento,
                             mutacao)

    evolucao.nsele = tamanho
    evolucao.pcruz = pcruz
    evolucao.manter_melhor = elitista
    evolucao.epidemia = epidemia

    gminmax = []

    for i in range(1000):
        t0 = time.time()
        vmin, vmax = evolucao.evoluir()
        tf = round(time.time() - t0, 2)
        print("G: {0}, max: {1}, min: {2}, T: {3}".format(evolucao.geracao,
                                                          vmax, vmin, tf))
        gminmax.append([evolucao.geracao, vmax, vmin])

    fname =  "{0}/populacao_{1}_{2}_{3}.npy".format(dir_pop,
                                                         tamanho_populacao,
                                                         evolucao.geracao,
                                                         int(LIMIAR * 100)
                                                         )
    save(fname, populacao.populacao)
    x = valores(populacao.populacao)
    individuo = x[-1,:]

    x = array([-1, 0, 1])
    y = array([0, 0, 0])
    n = 1000
    for i in range(n):
        print("i: {}".format(i))
        ganhador = jogar(individuo)
        if ganhador == -1:
            y[0] += 1
        elif ganhador == 0:
            y[1] += 1
        else:
            y[2] += 1

    y = y / n

    def percent(x, pos):
        'The two args are the value and tick position'
        return '{0:.1f}%'.format(x * 100)


    formatter = FuncFormatter(percent)
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(formatter)

    plt.bar(x, y)
    plt.xticks(x, ('O', 'V', 'X'))
    plt.xlabel("Jogador")
    plt.ylabel("Vitórias (porcentagem)")

    plt.title(r"População {0} Geracao {1} Limiar {2}".format(tamanho_populacao,
                                                             evolucao.geracao,
                                                             LIMIAR))
    plt.savefig("{0}/jogo_{1}_{2}_{3}.png".format(dir_fig,
                                                        tamanho_populacao,
                                                        evolucao.geracao,
                                                        int(LIMIAR * 100)))
