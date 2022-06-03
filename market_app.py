#==========================================================================================================
#================================ CHALLENGE DE JUAN ZENANOVICH ============================================
#==========================================================================================================

import config
import pyRofex
import time

def cerrar_sesion():
    print("Cerrando sesión en Remarkets...")

def imprimir():
    print("Envío de la orden: {0}".format(order["status"]))
    time.sleep(0.2)
    order_status = pyRofex.get_order_status(order["order"]["clientId"])
    estado_orden=order_status["order"]["status"]
    if estado_orden=="REJECTED":
        print("¡Orden Rechazada!, Motivo: {0}".format(order_status["order"]["text"]))
        cerrar_sesion()
    else:
        print("¡Orden ejecutada con éxtio!")
        cerrar_sesion()

print("Iniciando sesión en Remarkets...")
pyRofex.initialize(user=config.user, password=config.password, account= config.account, environment=pyRofex.Environment.REMARKET)

symbol = "GGAL/JUN22" #"SOJ.ROS/NOV22" "YPFD/AGO22" 

print("Consultado símbolo...")
md = pyRofex.get_market_data(ticker=symbol, entries=[pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.LAST])

if list(md.values())[0] == "ERROR":
    print("¡Símbolo inválido!")
    cerrar_sesion()
else:
    try:
        lp = md["marketData"]["LA"]["price"]
        print("Último precio operado: {0}".format(lp))

        print("Consultando BID...")
        try:
            bid = md["marketData"]["BI"][0]["price"]
            print("Precio BID: {0}".format(bid))
            
            print(f"Ingresando orden a {round(bid - 0.01, 2)}")
            order = pyRofex.send_order(ticker=symbol,
                                        side=pyRofex.Side.BUY,
                                        size=10,
                                        price=round(bid - 0.01, 2),
                                        order_type=pyRofex.OrderType.LIMIT)
            imprimir()

        except TypeError:
            print("No hay BIDs activos")

            print(f"Ingresando orden a 75.25")
            order = pyRofex.send_order(ticker=symbol,
                                        side=pyRofex.Side.BUY,
                                        size=10,
                                        price=75.25,
                                        order_type=pyRofex.OrderType.LIMIT)
            imprimir()

    except KeyError:
        print("No hay cotización para este activo")
        cerrar_sesion()

#==========================================================================================================
#================================ FIN DE LA APLICACIÓN ====================================================
#==========================================================================================================