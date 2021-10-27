from collections import namedtuple as nt
import csv

def Menu():
    print('\nMENÚ PRINCIPAL\n')
    print('\t1. Registrar venta\n\t2. Consultar venta\n\t3. Reporte de ventas\n\t4. Salir')
    seccion = int(input('\t\tAbrir sección:\n\t\t> '))
    return seccion

Venta = nt('Venta', ['descripcion', 'cantidad', 'precio'])
Folio = nt('Folio', ['id', 'fecha'])
Registro = {}

# with open('Ventas.csv','r', newline = '') as file:
#     lector = csv.reader(file)
#     next(lector)
    
#     for folio, fecha, detalles in lector:
#         list(detalles)
#         detalleVenta = []

#         for detalle in detalles:
#             venta_detalle = Venta(detalle[0], int(detalle[1]), float(detalle[2]))
#             detalleVenta.append[venta_detalle]

#         Registro[folio, fecha] = detalleVenta
#     print('\nAplicación iniciada correctamente...\n')

while True:
    seccion = Menu()
    if seccion == 1:
        print('REGISTRO DE VENTAS')
        control = 1
        ventaDetalle = []
        fecha = input('\n\t• Fecha de venta (DD-MM-AAAA):\n\t> ')
        while True:
            descripcion = input('\n\t• Descripción del artículo:\n\t> ')
            cantidad = int(input('\t• Cantidad:\n\t> '))
            precio = float(input('\t• Precio unitario:\n\t> '))

            ventaRegistro = Venta(descripcion, cantidad, precio)
            ventaDetalle.append(ventaRegistro)

            control = int(input('\n\t¿Desea agregar otro articulo? (1. SI / 0. NO)\n\t> '))
            if control == 0:
                indice = len(Registro) + 10
                folio = Folio(indice, fecha)

                Registro[folio] = ventaDetalle

                print('\n\t- Venta registrada correctamente...')
                print(f'\t- Folio de venta: {folio.id}')
                break

    if seccion == 2:
        subtotal = 0
        cantArticulos = 0
        linea = '-' * 50
        print('CONSULTA DE VENTAS')
        folioBusqueda = int(input('\n\t• Folio de venta:\n\t> '))

        for folio in Registro.keys():
            if folioBusqueda == folio.id:
                print(f'\n\n+{linea}+\n|{"TICKET DE VENTA":^50}|\n+{linea}+')

                fecVenta = folio.fecha
                print(f'|Folio: {folio.id:<13}{"Fecha: ":>20}{fecVenta:>10}|')
                print(f'+{"-" * 50}+')
                print(f'|{"Descripción":<35}{"Cant":^5}{"Precio":>10}|')
                print(f'+{"-" * 50}+')

                for articulo in Registro[folio]:
                        subtotal += articulo.cantidad * articulo.precio
                        cantArticulos += articulo.cantidad
                        print(f'|{articulo.descripcion:<35}{articulo.cantidad:^5}{articulo.precio:>10}|')

                iva = subtotal * .16
                total = subtotal + iva

                print(f'+{linea}+\n|Cant. Articulos: {cantArticulos:<33}|')
                print(f'|{"Subtotal: $":>40}{subtotal:>10}|')
                print(f'|{"IVA: $":>40}{iva:>10}|')
                print(f'|{"Total: $":>40}{total:>10}|')
                print(f'+{linea}+')
                break
            else:
                print('\n\t> Folio no encontrado...')

    if seccion == 3:
        granTotal = 0
        ivaTotal = 0
        subtotalF = 0

        print('REPORTE DE VENTAS')
        fechaBusqueda = input('\n\tFecha de las ventas a motrar:\n\t> ')
        print(f'\n\tVentas registradas el día: {fechaBusqueda}')
        for venta in Registro.keys():
            if fechaBusqueda == venta.fecha:
                print(f'\tVenta: {venta.id}')
                subtotal = 0
                cantArticulos = 0
                print(f'\t\t{"Cant":<5} | {"Descripción":<35} | {"Precio":<10}')
                for articulo in Registro[venta]:
                    cantArticulos += articulo.cantidad
                    subtotal += articulo.cantidad * articulo.precio
                    print(
                        f'\t\t{articulo.cantidad:<5} | {articulo.descripcion:<35} | ${articulo.precio:<10}')

                iva = subtotal * .16
                total = subtotal + iva
                print(f'\t\t{"Subtotal: $":>40}{subtotal:>10}')
                print(f'\t\t{"IVA":>40}{iva:>10}')
                print(f'\t\t{"Total: $":>40}{total:>10}')
                print(f'\t\t{"-" * 50}')

                subtotalF += subtotal
                ivaTotal += iva
                granTotal += total

        print(f'\t{"Ventas: $":<15}{subtotalF:>10}')
        print(f'\t{"IVA: $":<15}{ivaTotal:>10}')
        print(f'\t{"Total: $":<15}{granTotal:>10}')

    if seccion >= 4:
        with open('Ventas.csv', 'w', newline='') as file:
            nRegistro = csv.writer(file)
            nRegistro.writerow(('Folio', 'Venta'))
            for folio, venta in Registro.items():
                detalleVentas = []
                
                for detalle in venta:
                    detalles = []
                    detalles.append(detalle.descripcion)
                    detalles.append(detalle.cantidad)
                    detalles.append(detalle.precio)
                
                    detalleVentas.append(detalles)
                
                nRegistro.writerow([folio.id, folio.fecha, detalleVentas])

            print('\n\tRegistros guardados correctamente...')
            break
