# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
import time
import zmq
import json
import os
import uuid
import asyncio

# The class MUST call this class decorator at creation time
@magics_class
class MznbMagics(Magics):

    def __init__(self, shell, port, session_id):
        # You must call the parent constructor
        super(MznbMagics, self).__init__(shell)
        self.port = port
        self.endpoint = 'tcp://localhost:' + str(self.port)
        self.context = zmq.Context()
        self.session_id = session_id
        self.trans_id = None
        self.sock = None # We thread this thru the different magic functions.
        self.still_waiting = True

    async def listen(self):
        print('Awaiting result.')
        while self.still_waiting:
            await asyncio.sleep(0.6)
            try:
                msg = self.sock.recv(flags=zmq.NOBLOCK) # await here doesn't work
                msg = json.loads(msg)
            except zmq.ZMQError as e:
                msg = False
            if msg:
                print(msg)
                self.still_waiting = False

    async def start_listening(self):
        task = asyncio.create_task(self.listen())
        await task

    def start_listener(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.start_listening())

    @line_cell_magic
    def run_mzn(self, line, cell=None, body=None):
        self.sock = self.context.socket(zmq.REQ)
        self.sock.connect(self.endpoint)
        request = {'action': 'execute', 
                   'session-id': self.session_id,
                   'cmd-line': line,
                   'body': cell}
        self.sock.send_string(json.dumps(request))
        self.start_listener()





