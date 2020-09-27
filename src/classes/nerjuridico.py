# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:08:15 2020

@author: diego
"""
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from fuzzywuzzy import fuzz 

class FluxoPje:   
    """
    Classe responsavel por carregar o grapho referente aos fluxos
    """
    def __init__(self, verbose=False):
        """
        :param verbose: Booleana para indicar se serão printadas informações durante o treinamento
        :return: Uma instância da classe FluxoPje
        """       
        self.verbose = verbose
        self.df = pd.read_csv('..\..\dados\df_1_grau.csv', encoding='utf-8')
        self.dfTarefas = pd.read_csv('..\..\dados\df_tarefas_1_grau.csv', encoding='utf-8')
        
        # Cria dataframe com todos os nos existentes para checar similaridade
        obj = {'Tarefa': [], 'Similaridade': []}
        self.dfTarefas = pd.DataFrame(data=obj)
        dfTemp = pd.DataFrame(data=obj)
        self.dfTarefas['Tarefa'] = self.df[self.df['Tipo']=='task-node']['No origem']
        dfTemp[ 'Tarefa'] = self.df['No destino']
        self.dfTarefas = self.dfTarefas.append(dfTemp, ignore_index=True)
        self.dfTarefas.drop_duplicates(subset=['Tarefa'], keep='first', inplace=True)
        
    def print_status(self, str):
       if self.verbose:
           print(str)
        
    def menorCaminho(self, Origem, Destino, Completo, Formato = 'lista'):
        self.print_status('[menorCaminho]: Verificando nos')
        # Verifica se o nó existe. Caso nao exista, exibe uma lista de possíveis nós no formato Html
        texto = FluxoPje.checarNos(self, Origem, Destino)
        if texto != '':
            return texto
        
        self.print_status('[menorCaminho]: Carregando o grapho')
        G = nx.read_graphml("..\..\graphos\grapho_1_grau.xml")
        texto = ''
        
        # Verifica se existe caminho válidos entre os dois nós.
        if FluxoPje.path_exists(self, Origem, Destino, G):
            caminho = nx.shortest_path(G,Origem,Destino)
            self.print_status('Menor caminho: {}'.format(caminho))
            
            txt = ''
            # 
            if Formato == 'lista':
                texto = caminho
            elif Formato == 'txt':
                for etapa  in range(len(caminho)):
                    texto = texto + caminho[etapa]
            elif Formato == 'html':
                texto = self.enriquecercaminho(self, caminho, Completo)
        else:
            texto = 'Não existe caminho entre os nós {} e {}'.format(Origem, Destino)
        
        return texto

   
    def verMenorCaminho(self, Origem, Destino):
        self.print_status('[verMenorCaminho]: Verificando nos')
        texto = FluxoPje.checarNos(self, Origem, Destino)
        if texto != '':
            return texto
        
        self.print_status('[verMenorCaminho]: Carregando o grapho')
        G = nx.read_graphml("..\..\graphos\grapho_1_grau.xml")
        
        self.print_status('[verMenorCaminho]: Origem: {}, Destino: {}'.format(Origem, Destino))
        newG = FluxoPje.extract_path_edges(self, G, Origem, Destino)
        img = nx.draw_spectral(newG, with_labels=True)
        self.print_status('[verMenorCaminho]: img: {}'.format(img))
        plt.savefig("..\..\imagem\path.jpg")
        plt.clf()
        return 'ok'
    
    def obterCaminhos(self, Origem, Destino, Completo='', cutoff=10, Tipo='S'):
        self.print_status('[obterCaminhos]: Verificando nos')
        texto = FluxoPje.checarNos(self, Origem, Destino)
        if texto != '':
            return texto
        
        self.print_status('[obterCaminhos]: Carregando o grapho')
        G = nx.read_graphml("..\..\graphos\grapho_1_grau.xml")
        if FluxoPje.path_exists(self, Origem, Destino, G):
            if Tipo == 'S':
                caminhos = nx.shortest_simple_paths(G,Origem,Destino)
            else:
                caminhos = nx.all_simple_paths(G,Origem,Destino,cutoff)
        else:
            texto = 'Não existe caminho entre os nós {} e {}'.format(Origem, Destino)
        
        return caminhos 
       
    def obterCaminhosHtml(self, Origem, Destino, Completo='', cutoff=10, Tipo='S'):
        self.print_status('[obterCaminhos]: Verificando nos')
        texto = FluxoPje.checarNos(self, Origem, Destino)
        if texto != '':
            return texto
        
        self.print_status('[obterCaminhos]: Carregando o grapho')
        G = nx.read_graphml("..\..\graphos\grapho_1_grau.xml")
        texto = ''
        i = 1
        if FluxoPje.path_exists(self, Origem, Destino, G):
            if Tipo == 'S':
                caminhos = nx.shortest_simple_paths(G,Origem,Destino)
            else:
                caminhos = nx.all_simple_paths(G,Origem,Destino,cutoff)
            for caminho in caminhos:
                self.print_status('Obter caminhos: {}'.format(caminho))                
                texto = texto + f'<p><b>Caminho {i}: </b><p> ' + self.enriquecercaminho(self, caminho, Completo)
                i += 1
        else:
            texto = 'Não existe caminho entre os nós {} e {}'.format(Origem, Destino)
        
        return texto     
    def checarNos(self, Origem, Destino):
        # Verifica se o no Origem existe
        texto = ''
        achou = self.dfTarefas[self.dfTarefas['Tarefa']==Origem].values.any()
        if achou == False:
            texto = f'<p>Não encontramos nenhuma referência ao nó: <font color="red">{Origem}</font> {FluxoPje.calcularSimilaridade(self,Origem)}' 
        
        # Veridica se o no Destino existe
        achou = self.dfTarefas[self.dfTarefas['Tarefa']==Destino].values.any()
        if achou == False:
            texto = texto + f'<p>Não encontramos nenhuma referência ao nó: <font color="red">{Destino}</font> {FluxoPje.calcularSimilaridade(self,Destino)}'     
            
        return texto    
            
    def calcularSimilaridade(self, texto):
        self.dfTarefas['Similaridade'] = self.dfTarefas.apply(lambda x: fuzz.ratio(x['Tarefa'],texto), axis=1)
        dfNos = self.dfTarefas.sort_values(by=['Similaridade'], ascending=False).head()
        tarefasSimilares = f'<p>No entanto, existem alguns Nós similares. Por favor verifique o Nó desejado e refaça a solicitação :'
        for _ ,tarefa in dfNos.iterrows():
            tarefasSimilares = tarefasSimilares + f'<p>[<font color="blue">Nó</font>]:{tarefa.Tarefa}\t({tarefa.Similaridade}%)'
            
        return tarefasSimilares
    
    @staticmethod
    def enriquecercaminho(self, caminho, Completo):
        texto = ''
        for etapa in range(len(caminho)): 
            self.print_status('Etapa: {}'.format(caminho[etapa]))
            if  (Completo != 'all') and (self.df[(self.df['No origem']==caminho[etapa])]['Tipo'].values[0] != 'task-node'):
                continue
            if etapa == len(caminho)-1:
                texto = texto + '<p> [<font color="red">Processo</font>]: {} [<font color="blue">Nó</font>]: {} ({})</p>'.format(self.df[(self.df['No origem']==caminho[etapa])]['Processo'].values[0], caminho[etapa], self.df[(self.df['No origem']==caminho[etapa])]['Tipo'].values[0])
            else:
                if self.df[(self.df['No origem']==caminho[etapa])]['Tipo'].values[0] == 'process-state':
                    texto = texto + '<p> [<font color="red">Processo</font>]: {} [<font color="blue">Nó</font>]: {} ({}) - <b>Pegue a transição: {} </b></p>'.format(self.df[(self.df['No origem']==caminho[etapa])]['Processo'].values[0], caminho[etapa], self.df[(self.df['No origem']==caminho[etapa])]['Tipo'].values[0], self.df[((self.df['No origem']=='Tarefa inicial')&(self.df['No destino']==caminho[etapa+1]))]['Transicao'].values[0])
                else:
                    texto = texto + '<p> [<font color="red">Processo</font>]: {} [<font color="blue">Nó</font>]: {} ({}) - <b>Pegue a transição: {} </b></p>'.format(self.df[(self.df['No origem']==caminho[etapa])]['Processo'].values[0], caminho[etapa], self.df[(self.df['No origem']==caminho[etapa])]['Tipo'].values[0], self.df[((self.df['No origem']==caminho[etapa])&(self.df['No destino']==caminho[etapa+1]))]['Transicao'].values[0])
            self.print_status('Texto: {}'.format(texto))
        return texto
    
    # funcao auxiliar para extrair subcaminho de uma rede
    @staticmethod
    def extract_path_edges(self, G, source, target):
        self.print_status('[extract_path_edges]: Origem: {}, Destino: {}'.format(source, target))
        # Check to make sure that a path does exists between source and target.
        if FluxoPje.path_exists(self, source, target, G):
            nodes = nx.shortest_path(G, source, target)
            newG = G.subgraph(nodes)
            return newG

        else:
            raise Exception('Path does not exist between nodes {0} and {1}.'.format(source, target))
        
     # funcao auxiliar a identificacao do caminho
    @staticmethod
    def path_exists(self, node1, node2, G):
        """
        This function checks whether a path exists between two nodes (node1, 
        node2) in graph G.
        
        Special thanks to @ghirlekar for suggesting that we keep track of the 
        "visited nodes" to prevent infinite loops from happening. This also 
        removes the need to remove nodes from queue.
        
        Reference: https://github.com/ericmjl/Network-Analysis-Made-Simple/issues/3
        
        With thanks to @joshporter1 for the second bug fix. Originally there was 
        an extraneous "if" statement that guaranteed that the "False" case would 
        never be returned - because queue never changes in shape. Discovered at 
        PyCon 2017.
        
        With thanks to @chendaniely for pointing out the extraneous "break".
        
        If you would like to see @dgerlanc's implementation, see 
        https://github.com/ericmjl/Network-Analysis-Made-Simple/issues/76
        """
        visited_nodes = set()
        queue = [node1]
        
        for node in queue:
            neighbors = list(G.neighbors(node))
            if node2 in neighbors:
                self.print_status('Existe caminho entre os nós {0} e {1}'.format(node1, node2))
                return True
            else:
                visited_nodes.add(node)
                queue.extend([n for n in neighbors if n not in visited_nodes])
        
        self.print_status('Não existe caminho entre os nós {0} e {1}'.format(node1, node2))
        return False