from os import getenv
from dotenv import load_dotenv
from banco.banco import Banco


load_dotenv()

BANCO_NOME = getenv("BANCO_NOME")
BANCO_SENHA = getenv("BANCO_SENHA")
BANCO_USUARIO = getenv("BANCO_USUARIO")
BANCO_IP = getenv("BANCO_IP")
BANCO_PORTA = getenv("BANCO_PORTA")

# print(BANCO_NOME, BANCO_SENHA, BANCO_USUARIO, BANCO_IP, BANCO_PORTA)

def banco_padrao() -> Banco:

    if BANCO_NOME and BANCO_SENHA and BANCO_USUARIO and BANCO_IP and BANCO_PORTA:
        return Banco(
            BANCO_NOME,
            BANCO_SENHA,
            BANCO_USUARIO,
            BANCO_IP,
            BANCO_PORTA,
        )
    else:
        return None