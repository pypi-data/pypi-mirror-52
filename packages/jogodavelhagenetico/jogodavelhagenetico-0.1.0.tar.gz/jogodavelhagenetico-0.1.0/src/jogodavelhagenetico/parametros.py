#!/usr/bin/env python3.6
#-*- Coding: UTF-8 -*-
"""
Jogador Evolucionário.

Programa sob licença GNU V.3.
Desenvolvido por: E. S. Pereira.
Versão 0.0.1.
"""

class Parametros(tuple):
    """Imutavel."""
    __slots__ = []

    def __new__(cls, populacao, pmut, cromos, bits, nsele, pcruz):
         return tuple.__new__(cls, (populacao,
                                    pmut,
                                    cromos,
                                    bits,
                                    nsele,
                                    pcruz))
    @property
    def populacao(self):
         return tuple.__getitem__(self, 0)

    @property
    def pmut(self):
         return tuple.__getitem__(self, 1)

    @property
    def cromossomos(self):
         return tuple.__getitem__(self, 2)
    @property
    def bits(self):
        return tuple.__getitem__(self, 3)

    @property
    def nsele(self):
        return tuple.__getitem__(self, 4)

    @property
    def pcruz(self):
        return tuple.__getitem__(self, 5)

    def __getitem__(self, ind):
        return tuple.__getitem__(self, ind)
