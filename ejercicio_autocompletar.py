def cuadrados (n):
    n = int(input("Ingrese un número n: "))
    cuadrados = [i**2 for i in range(1, n + 1)]
    print("Los cuadrados de los primeros", n, "números naturales son:", cuadrados)