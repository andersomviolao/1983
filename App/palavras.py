import random
import time

# Lista de palavras em inglês
palavras = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon",
            "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine", "ugli", "vanilla",
            "watermelon", "xigua", "yam", "zucchini", "apricot", "blueberry", "cantaloupe", "dragonfruit", "eggplant", "fig"]

# Função para gerar palavras aleatórias
def gerar_palavras_aleatorias(n):
    return random.sample(palavras, n)

# Gerar 30 palavras aleatórias
palavras_aleatorias = gerar_palavras_aleatorias(30)

# Imprimir palavras a cada 5 segundos
for palavra in palavras_aleatorias:
    print(palavra)
    time.sleep(5)
