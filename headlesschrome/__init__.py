import subprocess, os, tempfile, logging, random

class Client:
    DEFAULT_DIMS = (1200, 800)

    def __init__(self, width=DEFAULT_DIMS[0], height=DEFAULT_DIMS[1],
            node=None, port=None, timeout=180):
        self.width = width
        self.height = height
        if node is None:
            this_dir = os.path.dirname(os.path.realpath(__file__))
            node = os.path.join(this_dir, '..', 'node')
        self.node = node
        if port is None:
            port = random.randint(1024, 65535)
        self.port = port
        self.timeout = timeout
        self.result_dir = tempfile.mkdtemp(prefix='headless-chrome-')

    def _command(self, url, har, screenshot):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        return [self.node, os.path.join(this_dir, '..', 'chrome_gather', 'cli.js'),
                '--width', str(self.width), '--height', str(self.height),
                '--har', har, '--screenshot', screenshot,
                '--timeout', str(self.timeout * 1000),
                url]

    def capture(self, url, har='har.json', screenshot='screenshot.png'):
        har = os.path.join(self.result_dir, har)
        screenshot = os.path.join(self.result_dir, screenshot)
        logging.debug(self._command(url, har, screenshot))
        subprocess.check_call(self._command(url, har, screenshot))
        return { 'har': har, 'screenshot': screenshot }
