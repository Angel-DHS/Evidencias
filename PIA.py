from datetime import date, datetime
import sqlite3
import sys
from sqlite3 import Error


def Menu():
    print('\n\n--- Menú Principal ---')
    print('1. Registrar una venta\n2. Consultar venta\n3. Salir')
    apartado = int(input('\tAbrir apartado: '))
    return apartado


while True:
    apartado = Menu()
    if apartado == 1:
        fecha = date.today()
        print('\t➝ REGISTRO DE VENTAS')
        try:
            with sqlite3.connect('PIA.db') as conn:
                c = conn.cursor()
                c.execute('INSERT INTO Venta(fecha) VALUES(?)', (fecha,))
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo un error: {sys.exc_info()[0]}')
        finally:
            conn.close()

        while True:
            total = 0
            while True:
                descripcion = input('\n\t\t▸ Descripción del artículo: ')
                if descripcion != '':
                    break
                else:
                    print('\t\tDescripció no válida')

            while True:
                cantidad = int(input('\t\t▸ Cantidad: '))
                if cantidad > 0:
                    break
                else:
                    print('\t\tDescripción no válida')

            while True:
                precio = float(input('\t\t▸ Precio unitario: '))
                if precio > 0:
                    break
                else:
                    print('\t\tDescripció no válida')

            try:
                with sqlite3.connect('PIA.db') as conn:
                    c = conn.cursor()
                    c.execute('SELECT MAX(folio) FROM Venta')
                    consulta = c.fetchall()
                    folio = consulta[0][0]

                    c.execute('''
                            INSERT INTO Detalles(folio, descripcion, cantidad, precio)
                            VALUES(?,?,?,?)
                            ''', (folio, descripcion, cantidad, precio))
            except Error as e:
                print(e)
            except Exception:
                print(f'Se produjo un error: {sys.exc_info()[0]}')
            finally:
                conn.close()

            total += cantidad * precio
            control = int(input('\n\t▸ ¿Desea agregar otro artículo? (0. No / 1. SI): '))

            if control == 0:
                print(f'\n\t▸Total Venta: ${total:>6}')
                break

    if apartado == 2:
        total = 0
        fecha = datetime.now()
        print('\n\n\t➝ CONSULTA DE VENTAS')

        while True:
            fec_busqueda = input('\t\t▸ Fecha de Venta: ')
            n_fecha = datetime.strptime(fec_busqueda, '%Y-%m-%d')
            
            if n_fecha <= fecha:
                break
            else:
                print('\t\t¡ERROR! Fecha no válida')

        try:
            with sqlite3.connect('PIA.db') as conn:
                c = conn.cursor()
                c.execute('''
                          SELECT Venta.folio, Detalles.descripcion, Detalles.cantidad, Detalles.precio
                          FROM detalles
                          INNER JOIN Venta ON Detalles.folio = Venta.folio
                          WHERE Venta.fecha = ?
                          ''', (fec_busqueda,))
                registro = c.fetchall()
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo un error: {sys.exc_info()[0]}')
        finally:
            conn.close()
            
            venta_control = 0
            if registro:
                for venta in registro:
                    if venta[0] != venta_control:
                        print(f'\nFolio: {venta[0]}')
                        print(f'\t{"Cant.":<8}{"Descripción":<25}{"Precio":>10}')

                        for folio, descripcion, cantidad, precio in registro:
                            if folio == venta[0]:
                                total += cantidad * precio
                                print(f'\t{cantidad:<10}{descripcion:<25}${precio:>9}')
                        print('-' * 50)
                    venta_control = venta[0]
                print(f'\n\tTotal de ventas: ${total:>10}')
            else:
                print('\n\tNO EXISTEN VENTAS REGISTRADAS PARA LA FECHA ESPECIFICADA')

    if apartado == 3:
        break
    
    if apartado > 3 or apartado == 0:
        print('Apartado no existente')
        
        