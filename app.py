from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from decouple import config
from flask import json
from requests import get, post
from Back_end import Interar_BD

app = Flask(__name__)
COLLECTION = "Planetas"

@app.errorhandler(404)
def not_found(e):
    return 'Pronto você não está, jovem padawan!'


@app.route('/inserir_planeta', methods=['POST'])
def inserir_planeta():
    if request.method == 'POST':
        IT = Interar_BD()
        json_planetas = request.get_json()
        id = IT.inserir_documento(COLLECTION, json_planetas)

        if type(id) == int:
            response = app.response_class(
                response=json.dumps({"resultado": "incluido", 'id': id}),
                status=201,
                mimetype='application/json'
            )
            return response
        else:
            response = app.response_class(
                response=json.dumps({"resultado": "não inserido"}),
                status=404,
                mimetype='application/json'
            )
            return response


@app.route('/deletar_planeta/id=<id>', methods=['DELETE'])
def deletar_planetas(id):
    if request.method == 'DELETE':
        IT = Interar_BD()
        Planetas = IT.deletar_Planeta(COLLECTION, int(id))
        if Planetas:
            response = app.response_class(
                response=json.dumps({"resultado": "deletado"}),
                status=202,
                mimetype='application/json'
            )
        else:
            response = app.response_class(
                response=json.dumps({"resultado": "erro ao deletar"}),
                status=500,
                mimetype='application/json'
            )
        return response


@app.route('/buscar_planeta/id=<id>', methods=['Get'])
def buscar_id(id):
    IT = Interar_BD()
    Planetas = IT.buscar_planeta_id(COLLECTION, int(id))
    if Planetas:
        Planetas_dic = []
        Planetas_dic.append(Planetas)

        for planeta in Planetas_dic:
            filmes = get(f"https://swapi.dev/api/planets/?search={planeta['Nome']}").json()
            if len(filmes["results"]) > 0:
                planeta['Filmes'] = len(filmes['results'][0]["films"])
            else:
                planeta['Filmes'] = 0
        response = app.response_class(
            response=json.dumps(Planetas_dic),
            status=200,
            mimetype='application/json'
        )
        return response

    response = app.response_class(
        response=json.dumps({"resultado": "erro ao encontrar"}),
        status=404,
        mimetype='application/json'
    )
    return response


@app.route('/buscar_planeta/nome=<nome>', methods=['Get'])
def buscar_nome(nome):
    IT = Interar_BD()
    Planetas = IT.buscar_planeta_nome(COLLECTION, nome)
    Planetas_dic = []
    Planetas_dic.append(Planetas)

    for planeta in Planetas_dic:
        filmes = get(f"https://swapi.dev/api/planets/?search={planeta['Nome']}").json()
        if len(filmes["results"]) > 0:
            planeta['Filmes'] = len(filmes['results'][0]["films"])
        else:
            planeta['Filmes'] = 0
    response = app.response_class(
        response=json.dumps(Planetas_dic),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/buscar_planeta/', methods=['Get'])
def buscar_tudo():
    IT = Interar_BD()
    Planetas = IT.buscar_Planeta(COLLECTION)
    Planetas_dic = []
    for planeta in Planetas:
        Planetas_dic.append(planeta)

    for planeta in Planetas_dic:
        filmes = get(f"https://swapi.dev/api/planets/?search={planeta['Nome']}").json()
        if len(filmes["results"]) > 0:
            planeta['Filmes'] = len(filmes['results'][0]["films"])
        else:
            planeta['Filmes'] = 0

    response = app.response_class(
        response=json.dumps(Planetas_dic),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/atualizar_planeta/id=<id>', methods=['PUT'])
def atualizar_planeta(id):
    if request.method == 'PUT':
        IT = Interar_BD()
        json_planetas = request.get_json()
        Planetas = IT.autalizar_Planeta(COLLECTION, int(id), json_planetas)
        if Planetas:
            response = app.response_class(
                response=json.dumps({"resultado": "atualizado"}),
                status=202,
                mimetype='application/json'
            )
        else:
            response = app.response_class(
                response=json.dumps({"resultado": "erro ao atualizar"}),
                status=500,
                mimetype='application/json'
            )
        return response


if __name__ == '__main__':
    app.run(debug=True)
