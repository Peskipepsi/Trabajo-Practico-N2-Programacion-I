#Definimos variables globales para poder mostrar los datos en el resumen
CODIGO = 0     
NOMBRE = 1       
CATEGORIA = 2     
PRECIO = 3    
STOCK = 4


def catalogo_inicial():
    """Devuelve el catálogo de partida del kiosco (lista de listas)."""
    return [
        [305, "Alfajor triple",           1, 1500.0, 24],
        [112, "Agua saborizada 500 ml",   2, 1900.0, 10],
        [421, "Cuaderno",                 4, 10000.0, 15],
        [208, "Galletitas surtidas",      3, 2800.0,  8],
        [117, "Gaseosa 1.5 L",            2, 4000.0,  6],
        [302, "Chicles",                  1,  700.0, 40],
        [415, "Birome azul",              4, 1200.0,  3],
        [210, "Fideos 500 g",             3, 2100.0, 12],
        [310, "Chocolate con leche",      1, 3200.0,  4],
        [119, "Jugo en polvo",            2,  900.0, 30],
    ]

def calcularDescuentoPorMonto(subtotal):
    #esta funcion calcula el descuento por monto
    #recibe el subtotal y devuelve el monto con el descuento aplicado
    if (subtotal) > 25000:
      return subtotal * 0.9
    return subtotal

def CalcularAjustePorMedioDePago(monto, medioDePago):
    # Esta función calcula el ajuste según el medio de pago.
    # Recibe el monto y el medio de pago.
    # Devuelve el monto ajustado.
     if medioDePago == 1:
        return monto * 0.95
     elif medioDePago == 2:
         return monto
     elif medioDePago == 3:
         return monto * 1.08

def CalcularImporteFinal(subtotal, medioDePago):
    # Esta función calcula el importe final de una venta.
    # Recibe el subtotal y el medio de pago.
    # Devuelve el importe final.
    montoConDescuento = calcularDescuentoPorMonto(subtotal)
    importeFinal = CalcularAjustePorMedioDePago(montoConDescuento, medioDePago)
    return importeFinal

NUMERODEVENTA = 0
CODIGOTICKET = 1
CANTIDAD = 2
MEDIODEPAGO = 3
IMPORTE = 4

def verResumen(catalogo, ventas):
    #(numeroDeVenta, producto[CODIGO], cantidad, medioDePago, importeFinal)
    cantidadTotalDeVentas = len(ventas)
    cantidadTotalDeVentasEfectivo = 0
    cantidadTotalDeVentasDebito = 0
    cantidadTotalDeVentasCredito = 0
    medioMasUtilizado = ""

    totalGolosinas = 0
    totalBebidas = 0
    totalAlmacen = 0
    totalLibreria = 0

    totalRecaudado = 0

    importeDeLaVentaMasAlta = 0

    ordenarSeleccion(catalogo)

    if cantidadTotalDeVentas == 0:
        return "Todavia no se registraron ventas."

    for i in range(len(ventas)):
        ticket = ventas[i]
        if ticket[MEDIODEPAGO] == 1:
            cantidadTotalDeVentasEfectivo += 1
        elif ticket[MEDIODEPAGO] == 2:
            cantidadTotalDeVentasDebito += 1
        else: 
            cantidadTotalDeVentasCredito += 1

        totalRecaudado += ticket[IMPORTE]

        if ticket[IMPORTE] >= importeDeLaVentaMasAlta:
            importeDeLaVentaMasAlta = ticket[IMPORTE]

        importePromedio = totalRecaudado / cantidadTotalDeVentas

        producto = buscarPorCodigo(catalogo, ticket[CODIGOTICKET])
            
        if producto[CATEGORIA] == 1:
            totalGolosinas += 1
        elif producto[CATEGORIA] == 2:
            totalBebidas += 1
        elif producto[CATEGORIA] == 3:
            totalAlmacen += 1
        else:
            totalLibreria += 1


    if cantidadTotalDeVentasEfectivo > cantidadTotalDeVentasDebito and cantidadTotalDeVentasEfectivo > cantidadTotalDeVentasCredito:
        medioMasUtilizado = "Efectivo"
    elif cantidadTotalDeVentasDebito > cantidadTotalDeVentasEfectivo and cantidadTotalDeVentasDebito > cantidadTotalDeVentasCredito:
        medioMasUtilizado = "Debito"
    else:
        medioMasUtilizado = "Credito"

    print(f"""
        RESUMEN:
        Total recaudado: {totalRecaudado}
        Cantidad total de ventas: {cantidadTotalDeVentas}
        Recaudado por categoria:
        Golosinas: {totalGolosinas}
        Bebidas: {totalBebidas}
        Almacen: {totalAlmacen}
        Libreria: {totalLibreria}
        Importe venta más alta: {importeDeLaVentaMasAlta}
        Importe promedio: {importePromedio}

        Cantidad total de ventas efectivo: {cantidadTotalDeVentasEfectivo}
        Cantidad total de ventas debito: {cantidadTotalDeVentasDebito}
        Cantidad total de ventas credito: {cantidadTotalDeVentasCredito}
        Medio de pago mas utilizado: {medioMasUtilizado}
    """)

def buscarPorCodigo(catalogo, codigo):
    """Búsqueda binaria (Clase 8, pág. 6).

    Pre:  secuencia está ORDENADA de menor a mayor. Si no lo está, el
          resultado no es confiable (puede devolver -1 aunque el elemento exista).
    Post: devuelve un índice donde está elemento, o -1 si no está.
    """
    izq = 0
    der = len(catalogo) - 1
    while izq <= der:                    # mientras quede un tramo por revisar
        medio = (izq + der) // 2         # // = división entera (la teoría usa int(... / 2))
        if catalogo[medio] == codigo:
            return medio
        if catalogo[medio] > codigo:  # el buscado está a la izquierda
            der = medio - 1
        else:                            # el buscado está a la derecha
            izq = medio + 1
    return -1

def buscarPorNombre(catalogo, nombreBuscado):
    #busqueda secuencial
    resultados = []
    for i in range(len(catalogo)):
        if nombreBuscado.lower() in catalogo[i][NOMBRE].lower():
            resultados.append(catalogo[i])
    return resultados

def buscarPorCategoria(catalogo, categoriaBuscado):
    #busqueda secuencial
    resultados = []
    for i in range(len(catalogo)):
        if categoriaBuscado.lower() in catalogo[i][CATEGORIA].lower():
            resultados.append(catalogo[i])
    return resultados

def ordenarSeleccion(catalogo, descendente = False):
    """Ordenamiento por selección (Clase 9, pág. 5), con sentido (act. 2.1 y 2.3).

    Pre:  los elementos de L son comparables entre sí.
    Post: L queda ordenada EN EL LUGAR, ascendente por defecto o descendente
          si descendente es True. No devuelve nada (¡no hacer L = ordenar_seleccion(L)!).
          Invariante: al terminar la iteración i, L[0..i] está ordenada y
          ningún elemento de L[i+1..] es "mejor" que L[i].
    """
    for i in range(len(catalogo) - 1):
        p = i                            # p = posición del mejor candidato hasta ahora
        for j in range(i + 1, len(catalogo)):
            # Ascendente: el mejor candidato es el MENOR. Descendente: el MAYOR.
            if descendente:
                if catalogo[j][CODIGO] > catalogo[p][CODIGO]: p = j
            else:
                if catalogo[j][CODIGO] < catalogo[p][CODIGO]: p = j

        catalogo[i], catalogo[p] = catalogo[p], catalogo[i]          # intercambio (se hace aunque p == i)

def registrarVenta(catalogo, ventas):
    #El programa solicita el código del producto y lo busca en el catálogo. Si no existe, lo informa y vuelve a pedirlo (o permite cancelar con 0).
    #Si existe, muestra nombre, precio y stock disponible, y pide la cantidad (entero mayor que cero y no mayor que el stock)
    #y el medio de pago (submenú 1 Efectivo, 2 Débito, 3 Crédito). Luego:

    busqueda = str(input("Introduzca el nombre del producto o 0 para volver al menu principal: "))
    if busqueda == "0":
        #ha cancelado, volver al menu principal
        return

    resultadosBusqueda = buscarPorNombre(catalogo, busqueda)

    if len(resultadosBusqueda) == 0:
        return registrarVenta(catalogo, ventas)

    for i in range(len(resultadosBusqueda)):
        
        print(f"""
            {i}) {resultadosBusqueda[i][NOMBRE]}
            Stock: {resultadosBusqueda[i][STOCK]}
            Precio: {resultadosBusqueda[i][PRECIO]}
            Categoria: {resultadosBusqueda[i][CATEGORIA]}
        """)

    productoSeleccionado = 1
    if len(resultadosBusqueda) > 1:
        productoSeleccionado = solicitarNumeroEnRango("Seleccione el producto deseado:", 1, len(resultadosBusqueda))
    productoSeleccionado -= 1 #el usuario escribe empezando desde la opcion 1, cuando en la tabla es 0, se le resta 1 para compensar
    producto = resultadosBusqueda[productoSeleccionado]

    nombre = producto[NOMBRE]
    stock = producto[STOCK] #el stock del producto es el quinto elemento
    precioUnitario = producto[PRECIO]
    categoria = producto[CATEGORIA]

    print(f""""
        {nombre},
        {precioUnitario},
        {stock}
    """)


    cantidad = solicitarNumeroEnRango("Escriba la cantidad de productos: ", 1, stock)

    medioDePago = solicitarNumeroEnRango("""Seleccione el metodo de pago:
    1) Efectivo
    2) Debito
    3) Credito
    """, 1, 3)

    subtotal = cantidad * precioUnitario
    montoConDescuento = calcularDescuentoPorMonto(subtotal)
    descuento = subtotal - montoConDescuento
    montoConAjuste = CalcularAjustePorMedioDePago(montoConDescuento, medioDePago)
    ajuste = montoConAjuste - montoConDescuento
    importeFinal = CalcularImporteFinal(subtotal, medioDePago)

    mostrarTicket(categoria, subtotal, descuento, ajuste, importeFinal)

    numeroDeVenta = len(ventas) + 1 #el numero de venta sera la cantidad de ventas + 1
    ventas.append((numeroDeVenta, producto[CODIGO], cantidad, medioDePago, importeFinal))
       
def mostrarTicket(nombreCategoria, subtotal, descuento, ajuste, importeFinal):
    # Esta función muestra el ticket de una venta.
    # Recibe la categoria, el subtotal, el descuento, el ajuste y el importe final e imprime el ticket
    print(f"""
    TICKET

    Categoria: {nombreCategoria}
    Subtotal: {subtotal}
    Descuento por monto: {descuento}
    Ajuste por medio de pago: {ajuste}
    Importe final: {importeFinal}
    """)

def solicitarNumeroEnRango(mensaje, minimo, maximo):
    # Esta fue la funcion mas dificil de implementar ya que no encontrabamos un metodo
    # Para validar el tipo de dato de entrada, por lo que lo comparamos directamente con
    # los numeros en rango de str, si el string de entrada es 1,2,... puede
    # retornar el valor convertido en tipo entero
    # el caso recursivo es si el dato ingresado no es valido
    numero = input(mensaje)
    for i in range(minimo, maximo + 1):
        if numero == str(i):
            return int(numero)
        
    print("Numero invalido. Ingrese un valor dentro del rango.")
    return solicitarNumeroEnRango(mensaje, minimo, maximo)

def agregarUnProducto(Catalogo, CodProd, NombreProd, Categoria, Precio, Stock):
    return "ayuda"

def consultarCatalogo(catalogo):
    print("\n=== CONSULTAR CATOLOGO ===")
    print("1) Listar catalogo completo")
    print("2) Buscar por codigo")
    print("3) Buscar por nombre")
    print("4) Listar por categoria")
    print("5) Tabla categoría x medio de pago")
    print("6) Volver al menu principal")
    opcion = solicitarNumeroEnRango("Elija una opción: ", 1, 6)

    if opcion == 1:
        for producto in catalogo:
            print(f"{producto[CODIGO]:<12} | {producto[NOMBRE]:^16} | {producto[CATEGORIA]:<12} | {producto[PRECIO ]:<12} | {producto[STOCK]:<12}")


    elif opcion == 2:
        print("2) Buscar por codigo")
        #buscarPorCodigo()
    elif opcion == 3:
        print("2) Buscar por codigo")
    elif opcion == 4:
        print("2) Buscar por codigo")
    elif opcion == 5:
        print("2) Buscar por codigo")


def cuentaRegresiva(numero):
    # Esta función realiza la cuenta regresiva para cerrar la caja.
    # Recibe el numero desde el cual comienza la cuenta regresiva.
    # No devuelve un valor.
    if numero == 0:
        print("¡Caja cerrada!")
    else:
        print(numero)
        cuentaRegresiva(numero - 1)

def cerrarCaja(catalogo, ventas):
    confirmacion = input("¿Esta seguro que desea cerrar la caja? (S/N): ")
    while confirmacion.lower() != "s" and confirmacion.lower() != "n":
        print("Respuesta invalida.")
        confirmacion = input("¿Esta seguro que desea cerrar la caja? (S/N): ")

    if confirmacion == "S" or confirmacion == "s":
        verResumen(catalogo, ventas)
        cuentaRegresiva(5)
    

def main():
    catalogo = catalogo_inicial()
    # TODO: ordenar el catálogo por código ANTES de cualquier búsqueda
    #       (precondición de buscar_por_codigo).

    ventas = []     # historial del día: lista de tuplas
                    # (numero, codigo, cantidad, medio_pago, importe_final)

    opcion = 0
    while opcion != 6:
        print("\n=== KIOSCO EL CAMPUS v2 ===")
        print("1) Registrar una venta")
        print("2) Consultar el catálogo")
        print("3) Ver resumen del día")
        print("4) Ranking de productos más vendidos")
        print("5) Tabla categoría x medio de pago")
        print("6) Cerrar caja y salir")
        opcion = solicitarNumeroEnRango("Elija una opción: ", 1, 6)

        if opcion == 1:
            # TODO: registrar_venta(catalogo, ventas)
            registrarVenta(catalogo, ventas)
        elif opcion == 2:
            # TODO: submenú del catálogo (listar ordenado, buscar por código,
            #       buscar por nombre, listar por categoría, agregar, volver)
            consultarCatalogo(catalogo)
        elif opcion == 3:
            # TODO: mostrar_resumen(catalogo, ventas) — contemplar historial vacío
            verResumen(catalogo, ventas)
        elif opcion == 4:
            # TODO: ranking = armar_ranking(...); ordenar(ranking, 1, True); mostrar
           # mostrarRanking()
           print("mostrarRankin")
        elif opcion == 5:
            # TODO: matriz = armar_matriz(...); mostrar con totales por fila y columna
           # mostrarTablaCategorias()
            print("mostrarTabla")

        else:
            # TODO: confirmar (S/N); si confirma: resumen, ranking, reposición,
            #       cuenta regresiva recursiva y despedida; si no, seguir en el menú.
            cerrarCaja(catalogo, ventas)

    print("¡Hasta mañana, Don Ramón!")

main()
