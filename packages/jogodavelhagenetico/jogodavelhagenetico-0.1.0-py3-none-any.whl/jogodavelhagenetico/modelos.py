#!/usr/bin/env python3.6
#-*- Coding: UTF-8 -*-
"""
Arvore de possibilidades do jogo da velha.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""
import pkg_resources

ARVORE = pkg_resources.resource_filename('jogodavelhagenetico',
                                          'modelo/arvorejvelha.pkl')

POPULACAO_O = pkg_resources.resource_filename('jogodavelhagenetico',
                                              '/modelo/populacao_o.npy')

POPULACAO_X = pkg_resources.resource_filename('jogodavelhagenetico',
                                              '/modelo/populacao_x.npy')

POPULACAO_NUM_X = pkg_resources.resource_filename('jogodavelhagenetico',
                                              '/modelo/populacao_p_x.npy')
POPULACAO_NUM_O = pkg_resources.resource_filename('jogodavelhagenetico',
                                                 '/modelo/populacao_p_o.npy')
