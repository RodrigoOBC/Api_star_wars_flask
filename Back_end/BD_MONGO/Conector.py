from bson import SON
from pymongo import MongoClient
from decouple import config
import pytest
import datetime


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

    def buscar_Planeta(self, collection, origem):
        try:
            if origem == 'B':
                if self.conectar():
                    arquivo = self.buscar_collection('Planetas').find()
                    self.desconectar()
                    return arquivo
            elif origem == 'C':
                if self.conectar():
                    arquivo = self.buscar_collection(collection).find()
                    self.desconectar()
                    return arquivo

        except:
            return False

    def buscar_valor_agregado(self, collection, variavel):
        try:
            dc = [
                {"$group": {"_id": f"${variavel}", "valor": {"$sum": "$Valor"}}},
                {"$sort": SON([("_id", 1), ("valor", 1)])}
            ]
            if self.conectar():
                arquivo = self.buscar_collection(collection).aggregate(dc)
                self.desconectar()
                return arquivo
        except:
            return False




if __name__ == '__main__':
    a, b, c, d, e = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], \
                    ['02/03/2020', '02/03/2020', '02/03/2020', '03/03/2020', '04/03/2020', '05/03/2020', '05/03/2020',
                     '05/03/2020', '06/03/2020', '06/03/2020'], \
                    [1452.28, 269.56, 50.39, 665.60, 133.02, 331.51, 500, 96.30, 2405.23, 1137.44], \
                    ['AMBEV', 'OI', 'Celular', 'Itaipava', 'Seguro', 'Assim', 'Ademir', 'Água', 'Souza Cruz', 'Luz'], \
                    ['02/03/2020', '02/03/2020', '02/03/2020', '03/03/2020', '04/03/2020', '05/03/2020', '05/03/2020',
                     '05/03/2020', '06/03/2020', '06/03/2020']
    for (id, data, valor, cliente, vencimento) in zip(a, b, c, d, e):
        dic = {"_id": id,
               "Data": datetime.datetime.strptime(data, "%d/%m/%Y"), "Valor": valor, "Cliente": cliente,
               "vencimento": vencimento}
        id = Interar_BD(user=config("usuario_mongo_adm"), senha=config("senha_adm_mongo"),
                        banco='Contabil').inserir_documento(collection='Gastos_Bar', arquivo=dic)
        print(id)
