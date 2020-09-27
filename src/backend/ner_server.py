# -*- coding: utf-8 -*-
#!flask/bin/python
from flask import Flask
from nerjuridico import NERJuridico
import os

app = Flask(__name__)

@app.route('/traduzir/<string:texto>', methods=["GET"])
def traduzir(texto):
    nerJud = NERJuridico()
    texto_marcado = nerJud.traduzir(texto)    
    
    return texto_marcado

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)