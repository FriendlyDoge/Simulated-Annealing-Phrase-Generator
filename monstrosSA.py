__author__ = 'Maifriende'

import random
import math
import spacy
import problem

nlp = spacy.load('pt_core_news_sm')

def cria_noodles():
    return []
def contains(lista, palavra): # lista = frase resposta.
    for i in lista:
        if i == palavra: # palavra: palavras possíveis para formar uma frase.
            return True
    return False

def constroi_proximo(lista, palavras): # Deve ser aleatório.
    numero = random.randint(1, 3)
    tamL = len(lista)
    cont = 0
    tamP = len(palavras)
    aux = []
    if(tamL == 0):
        aux.append(palavras[random.randint(0, tamP-1)]) #Insere uma palavra aleatoria do pool de palavras numa posição aleatória da lista.
    else:
        aux = lista.copy()
        if(numero == 1): #Caso 1: trocar palavra de lista por uma de palavras.
            nova = palavras[random.randint(0, tamP-1)]
            while(contains(lista, nova)):
                nova = palavras[random.randint(0, tamP-1)]
            aux[random.randint(0, tamL - 1)] = nova
        if(numero == 2):#Caso 2: tirar uma palavra.
            aux.remove(aux[random.randint(0, tamL - 1)]) #Remove palavra da pos randômica [tamL = aux.count()].
        if(numero == 3):#Caso 3: adicionar palavra.
            nova = palavras[random.randint(0, tamP-1)]
            while(contains(lista, nova)):
                nova = palavras[random.randint(0, tamP-1)]
            aux.insert(random.randint(0, tamL-1), nova) #Insere uma palavra aleatoria do pool de palavras numa posição aleatória da lista.

    return aux

def qualidade(lista):
    ok = 0
    aval = 0
    if(not lista):
        return -5000

    for i in lista:
        x = nlp(i)

        if(x[0].pos_ == "PRON"):
            aval = aval + 3

        elif(x[0].pos_ == "NOUN"):
            aval = aval + 4

        elif(x[0].pos_ == "VERB"):
            if(ok == 1):
                aval = aval - 6
            aval = aval + 5
            ok = 1;

        elif(x[0].pos_ == "DET"):
            aval = aval + 2

        elif(x[0].pos_ == "PROPN"):
            aval = aval + 4

        elif(x[0].pos_ == "ADP"):
            aval = aval + 2

        elif(x[0].pos_ == "NUM"):
            aval = aval + 1

        elif(x[0].pos_ == "ADV"):
            aval = aval + 3

        elif(x[0].pos_ == "SCONJ"):
            aval = aval + 3

    if(ok != 1):
        return -9000
    return aval  #Quanto maior aval melhor frase.

def calcula_delta(atual, proximo):
    return qualidade(proximo)-qualidade(atual)

def probabilidade(delta, t):
    dado = math.e ** (delta / t)
    if random.random() < dado:
        return True
    return False

def forma_palavra_imprime_retorna(array):
    resposta = ""
    if(not array):
        print("vazio")
    else:
        for palavra in array:
            print(palavra)
            resposta = resposta + " " + palavra
        print(resposta)
    return resposta

def temp_function(k, tempAtual):
    #!!!!!! temp = tempAtual * (alfa ^ k)
    alfa = 0.8
    return tempAtual * (alfa ** k)


def annealing(problem, kmax):
    # Retorna a resposta
    atual = cria_noodles()
    k = 0
    t = 1.0
    while k < kmax :
        for i in atual:
            print(i)
        t = temp_function(k, t) #Leva em conta a profundidade de busca e temperatura atual
        if t <= 0.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001 \
                or (len(atual) >= len(problem.getActions())) :
                # Primeira condição t deve ser tao pequeno bem proximo de zero
                # Segunda condição protege de loop infinito caso annealing forma uma frase com todas as palavras
            return atual
        proximo = constroi_proximo(atual, problem.getActions())
        delta = calcula_delta(atual, proximo) # Calcula chance de trocar para a nova frase gerada.
        if delta > 0:
            atual = proximo
        else:
            if probabilidade(delta, t):
                atual = proximo
        print("k: ", k, " t: ", t, "d: ", delta)
        k = k+1
    return  "Nao foi possivel formar frase"

def main(arquivo):
    ziriguidum = problem.Problem("", arquivo)
    return forma_palavra_imprime_retorna(annealing(ziriguidum, 80))

main("arquivograndeansi.txt")