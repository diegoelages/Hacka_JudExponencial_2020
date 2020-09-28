# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:08:15 2020

@author: diego
"""
import pandas as pd
import json
from bs4 import BeautifulSoup
import spacy
from spacy import displacy
import unicodedata

class NERJuridico:   
    """
    Classe responsavel por carregar o grapho referente aos fluxos
    """
    def __init__(self, verbose=False):
        """
        :param verbose: Booleana para indicar se serão printadas informações durante o treinamento
        :return: Uma instância da classe FluxoPje
        """       
        self.verbose = verbose
        self.output_dir = '../modelo'
        self.df = pd.read_excel('../dados/Significados.xlsx')    
        self.tags = ['CARGO', 'TERMO.JURIDICO', 'CONSTITUICAO.FEDERAL', 'ADCT', 'EMENDA.CONSTITUCIONAL', 'LEI.COMPLEMENTAR', 'TRATADOS', 'LEI.ORDINARIA', 'LEI.DELEGADA', 'MEDIDA.PROVISORIA', 'DECRETO.LEGISLATIVO', 'RESOLUCAO', 'DECRETO', 'INSTRUCAO.NORMATIVA', 'IMPOSTO', 'SENTENÇA', 'DESPACHO', 'DECISAO', 'ORGAO.PUBLICO', 'RECURSO.EXTRAORDINARIO', 'PARTE', 'RECURSO']
        self.cores = ['YELLOW', 'BLUE', 'BEIGE', 'CARAMEL', 'BROWN', 'GREY', 'CREAM', 'ORANGE', 'LILAC', 'PINK', 'PURPLE', 'GREEN', 'RED', 'VIOLET', 'SALMON', 'ACQUAMARINE', 'TURQUOISE', 'MUSTARD', 'BABY PINK', 'BURGUNDY', 'BRIGHT PINK', 'KHAKI']
        self.retorno = []
        
    def print_status(self, str):
       if self.verbose:
           print(str)
        
    def traduzir(self, Texto):
        self.print_status('[traduzir]: limpando o texto')
        texto_limpo = NERJuridico.cleanhtml_beautifulsoup(Texto)
        self.print_status(f'[traduzir]: Texto limpo: {texto_limpo}')
        
        nlp2 = spacy.load(self.output_dir)
        doc = nlp2(texto_limpo)

        for ent in doc.ents:
            self.retorno.append({'cor':self.cores[self.tags.index(ent.label_)], 'palavras':ent.text, 'significado':self.df[self.df['TERMO']==ent.text.strip()]['SIGNIFICADO'].values[0]})
            #self.print_status(ent.text, ",", ent.label_)
            #self.retorno.append({'cor':self.cores[self.tags.index(ent.label_)], 'palavras':ent.text, 'significado':'Termo utilizado para atribuir causa'})

        return self.retorno

    # funcao auxiliar para remover os acentos
    @staticmethod
    def remover_acentos(txt):
        return unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    
    # funcao auxiliar para fazer a limpeza do texto
    @staticmethod    
    def cleanhtml_beautifulsoup(raw_html):
        cleantext = ''
        if not raw_html is None:
            txt = BeautifulSoup(raw_html.replace("\n"," "), "html.parser").text.lower().replace("  ", "").replace("  ", "").replace("  ", "").replace("  ", "").replace("  ", "").replace("  ", "").replace("  ", "").replace("  ", "").replace("  ", "").replace("  ", "").replace("  ", "").replace("'","")
            cleantext = NERJuridico.remover_acentos(txt)
        return cleantext