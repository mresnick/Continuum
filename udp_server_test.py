from udp_server import udpServer
import admin


if not admin.isUserAdmin():
    admin.runAsAdmin()
q1 = udpServer()
