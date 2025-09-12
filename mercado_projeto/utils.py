import re

def input_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro válido.")

def input_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Digite um número decimal válido.")

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    return len(cpf) == 11
