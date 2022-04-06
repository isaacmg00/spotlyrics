import mitmproxy
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster

import threading
import asyncio
import time


class Addon(object):
    def __init__(self):
        self.num = 1

    def request(self, flow):
        flow.request.headers["count"] = str(self.num)

    def response(self, flow):
        self.num = self.num + 1
        flow.response.headers["count"] = str(self.num)
        print(self.num)


# see source mitmproxy/master.py for details
def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)  # This is the key.
    m.run_loop(loop.run_forever)


if __name__ == "__main__":
    options = Options(listen_host='127.0.0.1', listen_port=8080, http2=True)
    m = DumpMaster(options, with_termlog=False, with_dumper=False)
    config = ProxyConfig(options)
    m.server = ProxyServer(config)
    m.addons.add(Addon())

    # run mitmproxy in backgroud, especially integrated with other server
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop, m))
    t.start()

    # Other servers, such as a web server, might be started then.
    time.sleep(20)
    print('going to shutdown mitmproxy')
    m.shutdown()
