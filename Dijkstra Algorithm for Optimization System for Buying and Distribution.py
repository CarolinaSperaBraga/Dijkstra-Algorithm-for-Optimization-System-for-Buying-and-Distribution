"""
SME0827 - Data Structures
Dijkstra Algorithm for Optimization System for Buying and Distribution
"""



############################# Entradas ########################################################

# O primeiro índice se refere ao índice do mercado e o índice interno se refere ao índice do produto.
# Todas as sublistas devem ter o mesmo tamanho, mesmo que compostas de 0s.
produtos_m = [[2,2,5,8], # Produtos contidos nos mercados
              [3,5,7,4],
              [1,2,3,0]]
produtos_c = [[0,0,5,2], # Produtos a serem comprados pelos clientes
              [4,2,1,1],
              [1,1,0,0],
              [0,0,1,0],
              [1,3,1,7]]
# Matriz de preços dos produtos por mercado. Mesmas dimensões que a matriz de quantidade
produtos_p = [[1,2,2,3],
              [2,2,2,2],
              [3,2,1,1]]

# Quais nós são clientes e quais são mercados
mercados = [0,3,7]
clientes = [1,2,4,5,6]

# A forma do grafo, uma matriz de adjacências com os valores relativos aos caminhos percorridos
adjacencias = [[0,2,0,0,3,0,0,1],
               [2,0,2,1,0,0,0,0],
               [0,2,0,0,2,0,3,1],
               [0,1,0,0,0,2,1,0],
               [3,0,2,0,0,0,0,0],
               [0,0,0,2,0,0,0,0],
               [0,0,3,1,0,0,0,0],
               [1,0,1,0,0,0,0,0]]

#######################################################################################


# Construção da classe Grafo
class Grafo(object):
    def __init__(self, grafo) -> None:
        self.grafo = grafo

    # Caminho dijkstra entre dois nós 'fonte' e 'alvo'
    def caminho_mais_curto(self, fonte: int, alvo:int) -> list:
        n = len(self.grafo)
        encontrado = [False] * n
        dist = [float('inf')] * n
        anterior = [None] * n
        dist[fonte] = 0

        alt = fonte
        no_atual = fonte

        while(not encontrado[alvo]):
            encontrado[no_atual] = True
            for vizinho in range(n):
                d_aux = self.grafo[no_atual][vizinho]
                if d_aux == 0:
                   continue

                # Marcar o caminho mais curto até certo nó
                alt = dist[no_atual] + d_aux

                if alt < dist[vizinho]:
                    dist[vizinho] = alt
                    anterior[vizinho] = no_atual
            
            # Lambda que retorna o menor elemento e seu índice
            f = lambda i: [[x, dist[i] + v] for x,v in enumerate(self.grafo[i]) if v != 0 and not encontrado[x]]
            
            # Os índices dos valores mínimos dentre as distâncias diferentes de 0 
            # dos vizinhos dos nós já visitados
            l = [[i, min(f(i), key=lambda x: x[1])] for i in range(n) if encontrado[i] and f(i) != []]
            # Em que a é o nó ja visitado e b[0] é o nó seguinte
            a,b = min(l,key=lambda x: x[1][1])
            b = b[0]
            # Quando um nó é encontrado, atualizar sua distância,
            # o nó que veio antes e marcar como visitado
            dist[b] = dist[a] + self.grafo[a][b]
            anterior[b] = a
            no_atual = b
        # Caminho por anteriores do alvo até a fonte
        no_atual = alvo
        caminho = [alvo]
        while(no_atual != fonte):
            no_atual = anterior[no_atual]
            caminho.append(no_atual)
        caminho.reverse()
        return dist[alvo], caminho

    # Caminho mais curto entre chegando em uma fonte a partir de uma lista de nós
    def caminho_mais_curto_list(self, fontes: list, alvo:int) -> list:
        # O caminho é feito a partir do alvo até as fontes
        fonte = alvo
        alvo = fontes

        n = len(self.grafo)
        encontrado = [False] * n
        dist = [float('inf')] * n
        anterior = [None] * n
        dist[fonte] = 0

        alt = fonte
        no_atual = fonte
        
        while(not all([encontrado[a] for a in alvo])):
            encontrado[no_atual] = True
            for vizinho in range(n):
                d_aux = self.grafo[no_atual][vizinho]
                if d_aux == 0:
                   continue

                # Marcar o caminho mais curto até certo nó
                alt = dist[no_atual] + d_aux

                if alt < dist[vizinho]:
                    dist[vizinho] = alt
                    anterior[vizinho] = no_atual
            
            # Lambda que retorna o menor elemento e seu índice
            f = lambda i: [[x, dist[i] + v] for x,v in enumerate(self.grafo[i]) if v != 0 and not encontrado[x]]
            
            # Os índices dos valores mínimos dentre as distâncias diferentes
            # de 0 dos vizinhos dos nós já visitados
            l = [[i, min(f(i), key=lambda x: x[1])] for i in range(n) if encontrado[i] and f(i) != []]
            # Em que a é o nó ja visitado e b[0] é o nó seguinte
            a,b = min(l,key=lambda x: x[1][1])
            b = b[0]
            # Quando um nó é encontrado, atualizar sua distância,
            # o nó que veio antes e marcar como visitado
            dist[b] = dist[a] + self.grafo[a][b]
            anterior[b] = a
            no_atual = b
        # Caminho por anteriores do alvo até a fonte
        caminho = []
        for a in alvo:
            no_atual = a
            c = [a]
            while(no_atual != fonte):
                no_atual = anterior[no_atual]
                c.append(no_atual)
            caminho.append(c)
        return [[dist[v], caminho[x]] for x,v in enumerate(alvo)]


    # Recebe uma lista e forma caminhos entre os pares de nós dessa, caso não existam
    # Modifica o grafo e retorna uma matriz triangular superior, 
    # [mercado_a][mercado_b] = [distancia,caminho]
    def caminhos_internos(self, lista:list) -> list:
        n = len(lista)
        caminhos = [[None] *n for i in range(n)]
        for a in range(n):
            for b in range(a + 1, n):
                A = lista[a]
                B = lista[b]
                aux = self.caminho_mais_curto(A, B)
                # Shallow copy de aux, não adianta reverse() e desnecessário fazer deep copy
                caminhos[a][b] = aux
                caminhos[b][a] = aux
        return caminhos

    # Atribui cada elementos de uma lista A a um elemento de uma lista B baseado na distância.
    # Um dado 'ai' será atribuido a um 'bj' próximo, mas não necessariamente o mais proximo de todos
    def atribuir_nos(self, A:list, B:list) -> list:
        n = len(self.grafo)
        m = len(B)
        flag = [False] * m
        # Lista de nós sem B
        Q = [x for x in range(n) if x not in B]
        extendido = [[B[i]] for i in range(m)]
        
        f = lambda node: [[x,v] for x,v in enumerate(self.grafo[node]) if v!= 0 and x in Q]

        while len(Q) > 1:
            # Uma lista de vizinhos pra priorizar os caminhos de menor distância
            # entre o último nó associado a um mercado e o seu vizinho
            vizinhos = []
            for j in range(m):
                if flag[j]: continue
                vizinhos.append([j, [ min(f(node), key=lambda x:x[1]) for node in extendido[j] if f(node) != []]])
                if len(vizinhos[j][1]) == 0:
                    # Flag se não há mais clientes próximos a esse mercado
                    flag[j] = True
                    continue
                vizinhos[j][1] = min(vizinhos[j][1], key=lambda x:x[1])
            mais_proximo = min(vizinhos, key=lambda x:x[1][1])
            extendido[mais_proximo[0]].append(mais_proximo[1][0])
            Q.remove(mais_proximo[1][0])
        # Último elemento de Q feito separadamente porque não funciona em lambda f
        ultimo = min([[x,v] for x,v in enumerate(self.grafo[Q[0]]) if v!=0], key=lambda x: x[1])
        extendido[ultimo[0]].append(Q[0])
        return extendido

# Construção da classe Compras    
class Compras(object):
    def __init__(self, grafo:Grafo, clientes:list, produtos_clientes:list,
        mercados:list, produtos_mercados:list, precos:list) -> None:
        self.G = grafo
        self.clientes = clientes
        self.produtos_clientes = produtos_clientes
        self.mercados = mercados
        self.produtos_mercados = produtos_mercados
        self.precos = precos
        self.entre_mercados = self.G.caminhos_internos(self.mercados)
        self.atribuicoes = self.G.atribuir_nos(self.clientes, self.mercados)
        # Lista que relaciona o index dos clientes/mercados da lista de clientes/mercados 
        # com sua posição no grafo para evitar buscas
        self.clientes_id = [None] * len(self.G.grafo)
        for i,v in enumerate(self.clientes):
          self.clientes_id[v] = i
        self.mercados_id = [None] * len(self.G.grafo)
        for i,v in enumerate(self.mercados):
          self.mercados_id[v] = i

    # O cliente compra tudo que pode da sua lista de um dado mercado
    # Retorna produto (soma[0]), quantidade (soma[1]) preco (soma[2])
    def compra_basica(self, produtos_cliente:list, produtos_mercado:list, precos:list) -> list:
        n = len(produtos_mercado)
        p_compra = []
        for i in range(n):
            if produtos_cliente[i] == 0: continue
            # Maior e menor irão referenciar o objeto com menor número do produto
            maior = produtos_cliente
            menor = produtos_mercado
            if produtos_mercado[i] >= produtos_cliente[i]:
                menor = produtos_cliente
                maior = produtos_mercado
            maior[i] -= menor[i]
            # O menor é sempre a quantidade comprada, porque ou o cliente comprou 
            # tudo que queria ou porque comprou tudo que tinha no mercado
            p_compra.append([i, menor[i], precos[i]])
            menor[i] = 0
        # As listas são referenciadas, não precisam ser retornadas
        return p_compra

    # Recebe um cliente, o mercado atual e seu index na lista de mercados
    # Retorna mercado (soma[0]), produto (soma[1][0]), quantidade (soma[1][1]) preco (soma[1][2])
    def compra_resto(self, cliente:int):
        produtos = self.produtos_clientes[self.clientes_id[cliente]]
        n = len(self.produtos_clientes[0])
        soma_produtos = []

        while(len([x for x in produtos if x != 0]) > 0):
            # Comparação entre mercados
            comp = []
            # Visitar o mercado mais próximo do que já está, que tenha produtos que o cliente quer
            # Clientes priorizam preços mais baixos
            # Distância, caminho
            for m_id in range(len(self.mercados)):
                # Comprar o que pode desse mercado de cada produto a um certo preço
                # Semelhante à compra básica, mas não edita os valores internos
                comp.append([m_id, [( produtos[p] if produtos[p] < self.produtos_mercados[m_id][p]
                                    else self.produtos_mercados[m_id][p] )
                                    for p in range(n) if produtos[p] != 0]])
            # Escolhe o mercado em que pode comprar o máximo de produtos
            escolha = max(comp, key=lambda x: x[1])
            if sum(escolha[1]) == 0: break
            escolha = escolha[0]
            soma_produtos.append([escolha, self.compra_basica(produtos, self.produtos_mercados[escolha], self.precos[escolha])])
        return soma_produtos

    # Movimenta os clientes de acordo com suas atribuições de mercado
    def iniciar(self) -> None:
        # m é o index do mercado nas listas de mercados/produtos de mercados
        for m_id in range(len(self.atribuicoes)):
            # Nó no grafo referente ao mercado m
            m_grafo = self.atribuicoes[m_id][0]
            # Distância mercado-cliente para cada cliente atribuido
            m_c_d = self.G.caminho_mais_curto_list(self.atribuicoes[m_id][1:], m_grafo)
            for c in range(1,len(self.atribuicoes[m_id])):
                # Gastos totais
                g_total = 0
                cliente = self.atribuicoes[m_id][c]
                # Index do cliente nas listas de clientes/produtos dos clientes
                c_id = self.clientes_id[cliente]
                # Se o mercado está sem produtos, procurar outro
                aux = [(True if (v == 0 or self.produtos_clientes[c_id][x] == 0) else False) for x,v in enumerate(self.produtos_mercados[m_id])]
                if all(aux):
                    compra_variada = self.compra_resto(cliente)
                    if compra_variada != []:
                        # Mercado (soma[0]), produto (soma[1][0]), quantidade (soma[1][1]) preço (soma[1][2])
                        # Saindo do nó atual e seguindo para todos da lista
                        dist, caminho = self.G.caminho_mais_curto(cliente, self.mercados[compra_variada[0][0]])
                        g_total += dist
                        self.print_caminho(cliente, [dist, caminho])
                        self.print_compra(compra_variada[0][1])
                        for i in range(1, len(compra_variada)):
                            dist, caminho = self.entre_mercados[self.mercados_id[self.mercados[compra_variada[i-1][0]]]][self.mercados_id[self.mercados[compra_variada[i][0]]]]
                            if caminho[0] != self.mercados[compra_variada[i-1][0]]: caminho.reverse()
                            g_total += dist
                            self.print_caminho(cliente, [dist, caminho])
                            self.print_compra(compra_variada[i][1])
                        g_total += sum([sum([p[1] * p[2] for p in compra[1]]) for compra in compra_variada])
                else:
                    gastos = self.compra_basica(self.produtos_clientes[c_id], self.produtos_mercados[m_id], self.precos[m_id])
                    self.print_caminho(cliente, m_c_d[c-1])
                    self.print_compra(gastos)
                    g_total += sum([p[1] * p[2] for p in gastos]) + m_c_d[c-1][0]
                    # Se tem algum produto que o cliente queira
                    resto = [x for x,v in enumerate(self.produtos_clientes[c_id]) if v != 0]
                    if len(resto) > 0:
                        compra_variada = self.compra_resto(cliente)
                        if compra_variada != []:
                            # Saindo do nó atual e seguindo para todos da lista
                            dist, caminho = self.G.caminho_mais_curto(m_grafo, self.mercados[compra_variada[0][0]])
                            g_total += dist
                            self.print_caminho(cliente, [dist,caminho])
                            self.print_compra(compra_variada[0][1])
                            for i in range(1, len(compra_variada)):
                                dist, caminho = self.entre_mercados[self.mercados_id[self.mercados[compra_variada[i-1][0]]]][self.mercados_id[self.mercados[compra_variada[i][0]]]]
                                if caminho[0] != self.mercados[compra_variada[i-1][0]]: caminho.reverse()
                                g_total += dist
                                self.print_caminho(cliente, [dist, caminho])
                                self.print_compra(compra_variada[i][1])
                            g_total += sum([sum([p[1] * p[2] for p in compra[1]]) for compra in compra_variada])
                # Impressão do valor total gasto por cada cliente
                print(f"    Total: ${g_total}")
        resto = [x for x, v in enumerate(self.produtos_clientes) if len([y for y in v if y > 0]) > 0]
        if len(resto) > 0:
            for r in resto:
                print(f"C{self.clientes[r]} ", end='')
            print("Não conseguiram completar a compra")
        return

    # Impressão do caminho percorrido
    def print_caminho(self,cliente:int, caminho:list) -> None:
        c = caminho[1]
        print(f"[C{cliente}]: ", end='')
        for x in range(len(c) -1):
            s = f"C{c[x]}"
            if self.clientes_id[c[x]] == None:
                s = f"M{c[x]}"
            print(f"{s} -> ", end='')
        print(f"M{c[-1]}   |   $ {caminho[0]}")

    # Impressão dos gastos, quantidade de itens comprados e valor unitário
    def print_compra(self,compra:list) -> None:
        print(f"\tGastos:")
        for row in compra:
            if row[1] == 0: continue
            print(f"\t${row[1]*row[2]}\t{row[1]} de p{row[0]} a ${row[2]}")

            
# Resultados            
G = Grafo(adjacencias)
C = Compras(G, clientes, produtos_c, mercados, produtos_m, produtos_p)
C.iniciar()