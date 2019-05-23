from time import sleep

from model.client import Client

client = Client()
client.connect()
if len(client.server_robots_list) > 0:
    client.activate_manual_mode()
    client.send_command(pickup=True, command='(1, 6)', robot=client.server_robots_list[0][0])
client.deactivate_manual_mode()
client.disconnect()