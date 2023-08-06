from __future__ import absolute_import
import sys
from .mznb import MznbMagics
import json
from pathlib import Path
import os
import zmq
from ipykernel import get_connection_file
import nba_gateway

import urllib.request
from notebook import notebookapp
# This gets updated occassionally

def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  
    # IPython will call the default constructor on it.

    # https://gist.github.com/mbdevpl/f97205b73610dd30254652e7817f99cb
    connection_file_path = get_connection_file()
    connection_file = os.path.basename(connection_file_path)
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]
    config_files = {'linux':  "/.local/share/nb-agent/runtime.json",
                    'darwin': "/Library/nb-agent/runtime.json",
                    'windows': "/.local/share/nb-agent/runtime.json"} # I am guessing!

    config_file = str(Path.home()) + config_files[sys.platform]
    with open(config_file) as json_file:
        data = json.load(json_file)
        port = data['magic-server-port']
        jupyter_port = data['jupyter-port']

    ipynb_filename = 'unknown'
    last_active = 'unknown'
    servers = list(notebookapp.list_running_servers())
    prefix = 'http://127.0.0.1:%s/api/sessions?token=' % (jupyter_port,)
    for svr in servers:
        response = urllib.request.urlopen(prefix + svr['token'])
        sessions = json.loads(response.read().decode())
        for sess in sessions:
            if sess['kernel']['id'] == kernel_id:
                session_id = sess['id']
                ipynb_filename = (sess['notebook']['path'])
                last_active = (sess['kernel']['last_activity'])
                break

    gw = nba_gateway.NBAgateway()
    gw.start_server()
    ipython.push({'nba_gateway': gw})

    ctx = zmq.Context()
    sock = ctx.socket(zmq.REQ)
    sock.connect('tcp://localhost:' + str(port))
    try:
        msg = {'action': 'notify',
               'session-id': session_id,
               'nba-gateway-port': gw.port,
               'dir': os.getcwd(),
               'ipynb-file': ipynb_filename,
               'last-active': last_active}
        msg_str = json.dumps(msg)
        sock.send_string(msg_str)
        print('MiniZinc Notebook Agent Communicator version %s' % (__version__,))
        print('Connected to session %s at port %s.' % (session_id, port))
        print(json.loads(sock.recv()))

    except KeyError:
        print('''Not able to communicate with nb-agent.''')

    magics = MznbMagics(ipython, port, session_id)
    ipython.register_magics(magics)

__version__ = '0.2.0'
