# -*- coding: utf-8 -*-
#!flask/bin/python
from flask import Flask
from flask import send_file
from pjefluxo import FluxoPje
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('..\..\imagem')

@app.route('/menorcaminho/de/<string:noorigem>/para/<string:nodestino>', defaults={'completo': None}, methods=["GET"])
@app.route('/menorcaminho/de/<string:noorigem>/para/<string:nodestino>/<string:completo>', methods=["GET"])
def menorcaminho(noorigem, nodestino, completo):
    fluxo = FluxoPje()
    path = fluxo.menorCaminho(noorigem,nodestino,completo)
    return 'Menor caminho encontrado: {}'.format(path)

@app.route('/vermenorcaminho/de/<string:noorigem>/para/<string:nodestino>')
def vermenorcaminho(noorigem, nodestino):
    fluxo = FluxoPje(verbose=True)
    img = fluxo.verMenorCaminho(noorigem, nodestino) 
    print('ws.vermenorcaminho: {}'.format(img))
 

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'path.jpg')
    print('arquivo: {}'.format(full_filename))
    return send_file('path.jpg', mimetype='imagem')



if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)