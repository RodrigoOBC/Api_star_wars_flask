from bson import SON
from pymongo import MongoClient
from decouple import config
import pytest
import datetime
from requests import get, post


class Conector:
    def __init__(self, senha=None, usuario=None):
        self.senha = senha
        self.usuario = usuario
        self.conn = MongoClient(
            f'mongodb+srv://{self.usuario}:{self.senha}@cluster0-1vunb.mongodb.net/test?retryWrites=true&w=majority')
        self.conn.close()

    def conectar(self):
        try:
            self.conn = MongoClient(
                f'mongodb+srv://{self.usuario}:{self.senha}@cluster0-1vunb.mongodb.net/test?retryWrites=true&w=majority')
            return True
        except:
            return False

    def desconectar(self):
        try:
            self.conn.close()
            return True
        except:
            return False

    def listar_banco(self, banco=None):
        if self.conectar():
            banco = self.conn[banco]
            if self.desconectar():
                return banco
            else:
                return False
        else:
            return False

    def listar_Collection(self, banco, collection):
        try:
            collection = self.listar_banco(banco)[collection]
            return collection
        except:
            return False


class Interar_BD(Conector):
    def __init__(self, user, senha, banco=None):
        self.senha = senha
        self.user = user
        Conector.__init__(self, senha=self.senha, usuario=self.user)
        self.banco = "B2w_planetas"

    def buscar_collection(self, collection):
        coll = self.listar_Collection(self.banco, collection)
        return coll

    def inserir_documento(self, collection, arquivo):
        try:
            if self.conectar():
                id = Interar_BD(user=config("usuario_mongo_adm"), senha=config("senha_adm_mongo")).busca_id('Planetas')
                if arquivo['Nome'] == None or arquivo['Clima'] == None or arquivo['Terreno'] == None:
                    return False
                if len(list(id)) > 0:
                    arquivo['_id'] = list(id)[0]['_id'] + 1
                else:
                    arquivo['_id'] = 0
                id_aqu = self.buscar_collection(collection).insert_one(arquivo).inserted_id
                self.desconectar()
                return id_aqu
            else:
                return False
        except:
            return False

    def deletar_Planeta(self, collection, id):
        try:
            if self.conectar():
                self.buscar_collection(collection).delete_one({"_id": id})
                self.desconectar()
                return True
        except:
            return False

    def autalizar_Planeta(self, collection, id, arquivo):
        try:
            if self.conectar():
                self.buscar_collection(collection).update_one({'_id': id}, {'$set': arquivo})
                self.desconectar()
                return True
        except:
            return False

    def buscar_Planeta(self, collection):
        try:
            if self.conectar():
                arquivo = self.buscar_collection(collection).find()
                self.desconectar()
                return arquivo
        except:
            return False

    def buscar_planeta_id(self, collection, variavel):
        try:
            if self.conectar():
                arquivo = self.buscar_collection(collection).find_one({"_id": variavel})
                self.desconectar()
                return arquivo

        except:
            return False

    def buscar_planeta_nome(self, collection, variavel):
        try:
            if self.conectar():
                arquivo = self.buscar_collection(collection).find_one({"Nome": variavel})
                self.desconectar()
                return arquivo

        except:
            return False

    def busca_id(self, collection):
        try:
            if self.conectar():
                arquivo = self.buscar_collection(collection).find().sort([("_id", -1)]).limit(1)
                self.desconectar()
                return arquivo

        except:
            return False


if __name__ == '__main__':
    pass
