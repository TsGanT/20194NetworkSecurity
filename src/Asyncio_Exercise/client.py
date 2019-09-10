import asyncio
import time

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.flag = 0
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data.decode())

        # Define the command list
        command_list = ["SUBMIT,Tianshi Feng,tfeng7@jhu.edu,team 4,1024", "look", "look chest", "look mirror", "get hairpin",
                        "unlock chest with hairpin", "open chest", "look in chest", "get hammer in chest", "unlock door with hairpin",
                        "open door"]
        if self.flag <= len(command_list)-1:
            command = self.send_message(command_list[self.flag])
            self.transport.write(command.encode())
            self.flag = self.flag + 1
        # time.sleep(0.25)

    def send_message(self, message):
        command = message + "<EOL>\n"
        return command

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


loop = asyncio.get_event_loop()

coro = loop.create_connection(lambda: EchoClientProtocol(loop), '192.168.200.52', 19003)
#coro = loop.create_connection(lambda: EchoClientProtocol(loop), 'localhost', 1024)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
