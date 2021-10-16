# EVIDENCIA 1
from collections import namedtuple
import time

#DEFINIMOS UN MENÚ PARA REUTILIZARLO LAS VECES QUE SEA NECESARIO
def menuPrincipal():
    print('\n--- MENÚ ---\n1. Registrar una venta\n2. Consultar una venta\n3. Salir')
    seccion = int(input('\nAbrir seccion no.: '))
    return seccion;


#Definimos tupla nominada
Venta = namedtuple('Venta', ['descripcion', 'cantidad', 'precio'])
#Definimos diccionario
RegistrosVentas = {}

#Inicia la aplicación
print('\n\n----- Llantas "El Corrienton" -----')
while True:
    seccion = menuPrincipal()
    if seccion == 1:
        descripciones = []
        cantidades = []
        precios = []
        
        print('\n\tREGISTRO DE VENTAS')
        while True:
            #Solicita los datos que componen la tupla    
            descripcion = input('\n\t\t> Descripción del artículo: \n\t\t-> ')
            cantidad = int(input('\t\t> Cantidad: '))
            precioUnit = int(input('\t\t> Precio Unitario: '))
            
            #Agregamos los datos dentro de una lista
            descripciones.append(descripcion)
            cantidades.append(cantidad)
            precios.append(precioUnit)
            
            indicadorVenta = int(input('\n\t\t¿Desea agregar otro articulo?\n\t\t(1. SI / 0. NO): '))
            
            #Si el usuario indica que termino de agregar articulos...
            if indicadorVenta == 0:
                #Definimos un id para la venta, nos aseguramos que no se repita ya que este lo genera el codigo
                numVenta = len(RegistrosVentas) + 10
                
                #Guardamos las listas en una tupla nomidada
                registroVenta = Venta(descripciones, cantidades, precios)
                #Dicha tupla se guarda en el diccionario
                RegistrosVentas[numVenta] = registroVenta
                
                print('\n\tGuardando venta...')
                time.sleep(1)
                print(f'\tGuardado correctamente, su numero de venta es {numVenta}')
                
                break
                
        
    if seccion == 2:
       print('\n\tCONSULTAS DE VENTAS') 
       numVenta = int(input('\t\t> Ingrese el número de venta: '))
       
       if numVenta in RegistrosVentas.keys():
           subtotal = 0
           cantArticulos = 0
           print(f'\n\n+{"-" * 20}  {"TICKET DE COMPRA"}  {"-" * 20}+')
           print(f'|Venta no: {numVenta}\n')
           print(f'|{"Descripción":<45}{"Cant":^5}{"Precio":>10}|\n|{"-"*60}|')
           
           #Recorremos las listas que conforman la tupla nominada, las 3 a la vez
           for desc, cant, prec in zip(RegistrosVentas[numVenta].descripcion, RegistrosVentas[numVenta].cantidad, RegistrosVentas[numVenta].precio):
               #Calculamos la cantidad de articulos y subtotal
               cantArticulos += cant
               subtotal += cant * prec
               #Se imprimen los articulos
               print(f'|{desc:<45}{cant:^5}{prec:>10}|')
               
           iva = subtotal * .16
           total = subtotal + iva
           #Mostramos los resultados
           print(f'\n ** Cantidad de productos vendidos: {cantArticulos}')
           print(f'\n{"Subtotal: $":>50}{subtotal:>10}')
           print(f'{"IVA: $":>50}{iva:>10}\n')
           print(f'{"Total: $":>50}{total:>10}')
           print(f'{"-----Gracias por su compra -----":^60}')
        
    if seccion == 3:
        print('Cerrando aplicación...')
        break
    