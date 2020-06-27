import pytest
from decouple import config
from .Conector import Conector


class TestClass:

    def test_conectar(self):

        conn = Conector(usuario=config("usuario_mongo_adm"), senha=config("senha_adm_mongo"))
        Resposta = conn.conectar()
        conn.desconectar()
        assert Resposta == True

    def test_desconectar(self):
        conn = Conector(usuario=config("usuario_mongo_adm"), senha=config("senha_adm_mongo"))
        conn.conectar()
        assert conn.desconectar() == True

if __name__ == '__main__':
    pass