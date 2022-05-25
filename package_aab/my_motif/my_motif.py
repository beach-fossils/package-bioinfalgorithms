# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class: MyMotifs
"""

def createMatZeros(line_num, col_num):
    """
    Método para criar uma matriz de zeros
    :param line_num: número de linhas da matriz
    :param col_num: número de colunas da matriz
    :return: matriz de zeros
    """
    mat_z = [] #lista vazia para criar a matriz de zeros
    for i in range(0, line_num): #por cada linha de zero ao número de linhas desejado
        mat_z.append([0]*col_num) #adiciona um zero col_num vezes
    return mat_z


def printMat(mat):
    """
    Método utilizado para imprimir a matriz.
    :param mat: matriz a imprimir
    :return:
    """
    for i in range(0, len(mat)): #por cada índice da lista da matriz
        print(mat[i]) #imprime o valor correspondente


class MyMotifs:
    """

    """

    def __init__(self, seqs=[], pwm=[], alphabet=None):
        if seqs:
            self.size = len(seqs[0])
            self.seqs = seqs  # objetos classe MySeq
            self.alphabet = seqs[0].alfabeto()
            self.doCounts()
            self.createPWM()
        else:
            self.pwm = pwm
            self.size = len(pwm[0])
            self.alphabet = alphabet

    def __len__(self):
        return self.size

    def doCounts(self):
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1

    def createPWM(self):
        if self.counts == None:
            self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)

    def consensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]
        return res

    def maskedConsensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]
            else:
                res += "-"
        return res

    def probabSeq(self, seq):
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res

    def probAllPositions(self, seq):
        res = []
        for _ in range(len(seq)-self.size+1):
            res.append(self.probabSeq(seq))
        return res

    def mostProbableSeq(self, seq):
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size):
            p = self.probabSeq(seq[k:k + self.size])
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind


def test():
    # test
    from my_seq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat(motifs.counts)
    printMat(motifs.pwm)
    print(motifs.alphabet)

    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))

    print(motifs.consensus())
    print(motifs.maskedConsensus())


if __name__ == '__main__':
    test()