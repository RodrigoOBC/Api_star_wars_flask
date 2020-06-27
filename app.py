from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from decouple import config
from flask import json
from requests import get,post
from Back_end import Interar_BD

app = Flask(__name__)


@app.route('/inserir_planeta', methods=['POST'])
def inserir_planeta():
    if request.method == 'POST':
        IT = Interar_BD(user=config("usuario_mongo_adm"), senha=config("senha_adm_mongo"))
        json_planetas = request.get_json()
        IT.inserir_documento("Planetas", json_planetas)
        response = app.response_class(
            response=json.dumps({"resultado": "incluido"}),
            status=201,
            mimetype='application/json'
        )
        return response

    response = app.response_class(
        response=json.dumps({"resultado": "não encontrado"}),
        status=404,
        mimetype='application/json'
    )
    return response


@app.route('/buscar_planeta/id=<id>', methods=['Get'])
def tabela_grafico(id):
    IT = Interar_BD(user=config("usuario_mongo_adm"), senha=config("senha_adm_mongo"))
    Planetas = IT.buscar_planeta_id('Planetas',int(id))
    filmes = len(get(f"https://swapi.dev/api/planets/?search={Planetas['Nome']}").json()['results'][0]["films"])
    Planetas["Filmes"] = filmes
    response = app.response_class(
        response=json.dumps(Planetas),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/buscar_planeta/', methods=['Get'])
def hello_world():
    IT = Interar_BD(user=config("usuario_mongo_adm"), senha=config("senha_adm_mongo"))
    Planetas = IT.buscar_Planeta("Planetas")
    response = app.response_class(
        response=json.dumps(list(Planetas)),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)
