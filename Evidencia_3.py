# Evidencia 3
#Importación de librerias necesarias
import sys
import sqlite3
from sqlite3 import Error

#Función Menu para iterar el programa
def Menu():
    print('\n\nMENÚ PRINCIPAL')
    print('\n1. Registrar Venta\n2. Consultar Venta\n3. Reporte de Ventas\n4. Salir')
    apartado = int(input('\n\tAbrir apartado:\n\t>'))
    return apartado


while True:
    apartado = Menu()

    #Apartado de registro de ventas
    if apartado == 1:
        print('\n\tREGISTRO DE VENTAS')
        folio = int(input('\tFolio de Venta:\n\t> '))
        fecha = input('\tFecha de Venta:\n\t> ')
        venta = (folio, fecha)
        
        #Iniciamos la conexion a la BD
        try:
            with sqlite3.connect('db.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO ventas(folio, fecha) VALUES(?,?)", venta)
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo un error: {sys.exc_info()[0]}')

        #Ciclamos la captura de articulos
        while True:
            descripcion = input('\n\tDescripción del articulo:\n\t> ')
            cantidad = int(input('\tCantidad:\n\t> '))
            precio = float(input('\tPrecio Unitario:\n\t> '))

            detalle = (folio, descripcion, cantidad, precio)
            
            #Conectamos a la base de datos para la iserción de los detalles
            try:
                with sqlite3.connect('db.db') as conn:
                    c = conn.cursor()
                    c.execute(
                        "INSERT INTO detalles(folio, descripcion, cantidad, precio) VALUES(?,?,?,?)", detalle)
            except Error as e:
                print(e)
            except Exception:
                print(f'\n\tSe produjo un error: {sys.exc_info()[0]}')
            
            control = int(input('\n\t¿Desea agregar otro articulo? (1. SI/ 0. NO)\n\t> '))
            
            if control == 0:
                print('Venta registrada correctamente')
                break
    
    #Consulta de la venta
    if apartado == 2:
        print('\n\tCONSULTA DE VENTAS')
        f_busqueda = int(input('\n\tIngrese folio de venta:\n\t> '))
        subtotal = 0
        cantArticulos = 0
        
        #Conectamos a la BD para la busqueda de la venta
        try:
            with sqlite3.connect('db.db') as conn:
                c = conn.cursor()
                #busqueda = {"folio":f_busqueda}
                c.execute("SELECT * FROM detalles WHERE folio = ?", (f_busqueda,))
                registro = c.fetchall()
                
                if registro:                    
                    print(f'|{"TICKET DE COMPRA":^60}|\n+{"-" * 60}+')
                    print(f'|{"Descripción":<35}{"Cant":^10}{"Precio":>15}|\n+{"-"*60}+')

                    for num, folio, descripcion, cantidad, precio in registro:
                        subtotal += cantidad * precio
                        cantArticulos += cantidad
                        print(f'|{descripcion:<35}{cantidad:^10}{precio:>15}|')

                    iva = subtotal * .16
                    total = subtotal + iva
                    print(f'+{"-" * 60}+\n|Total productos: {cantArticulos:<43}|')
                    print(f'|{"Subtotal $":>45}{subtotal:>15}|')
                    print(f'|{"IVA $":>45}{iva:>15}|')
                    print(f'|{"Total: $":>45}{total:>15}|\n+{"-" * 60}+')
                else:
                    print(f'No se encontró una venta con el folio especificado')   
        except Error as e:
            print(e)
        except Exception:
            print(f'\n\tSe produjo un error: {sys.exc_info()[0]}')
        finally:
            conn.close()
    
    #Reporte de ventas            
    if apartado == 3:
        print('\n\tREPORTE DE VENTAS')
        fecha_busqueda = input('\n\tIngrese fecha de ventas:\n\t> ')
        
        #Conectamos a la BD para realizar la consulta 
        try:
            with sqlite3.connect('db.db') as conn:
                c = conn.cursor()
                busqueda = {"fecha":fecha_busqueda}
                c.execute("""
                          SELECT ventas.folio, detalles.descripcion, detalles.cantidad, detalles.precio \
                              FROM detalles \
                              INNER JOIN ventas ON detalles.folio = ventas.folio \
                              WHERE ventas.fecha = ?
                          """, (fecha_busqueda,))
                registro = c.fetchall()
                
                print('\n\tREPORTE DE VENTAS')
                print(f'\n\tFecha: {fecha_busqueda}')
                
                subtotalF = 0
                cArticulos = 0
                
                #Iteramos el registro para separarlos por ventas
                ventaControl = 0
                for venta in registro:
                    if venta[0] != ventaControl:
                        print(f'\nFolio: {venta[0]}')
                        print(f'\t{"Cant":<10}{"Descripción":<35}{"Precio":>15}')
                    
                        for folio, descripcion, cantidad, precio in registro:
                            if folio == venta[0]:
                                subtotalF += cantidad * precio
                                cArticulos += cantidad
                            
                                print(f'\t{cantidad:<10}{descripcion:<35}$ {precio:>13}')
                        
                        print(f'\t{"-" * 60}')
                    
                    ventaControl = venta[0]
                
                iva = subtotalF * .16
                total = subtotalF + iva
                print(f'\n\tSubtotal: ${subtotalF:>10}')
                print(f'\tIVA: ${iva:>10}')
                print(f'\tTotal: ${total:>10}')

        except Error as e:
            print(e)
        except Exception:
            print(f'\n\tSe produjo un error: {sys.exc_info()[0]}')
        finally:
            conn.close()
    
    if apartado >= 3:
        print('Cerrando Aplicación...')
        break