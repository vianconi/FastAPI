# def suma(num1: int, num2: int) -> int:
#     return num1 + num2

# val1: int = 20
# val2: int = 10

# resul: int = suma(val1, val2)
# print(resul)

# class User():

#     def __init__(self, username:str, password:str) -> None:
#         self.username = username
#         self.password = password

#     def saluda(self) -> str:
#         return f'Hola {self.username}'


# cody = User('Cody', 'pass123')
# print(cody.saluda())

from typing import List


calificaciones: List[int] = [10, 9, 5, 5, 7, 9, 9]


def promedio(calificaciones: List[int]) -> float:
    return sum(calificaciones) / len(calificaciones)


print(promedio(calificaciones))
