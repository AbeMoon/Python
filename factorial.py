def factorial(n):
    if n < 0:
        return None
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

# Ejemplo de uso:
numero = 5
print(f"El factorial de {numero} es {factorial(numero)}")
