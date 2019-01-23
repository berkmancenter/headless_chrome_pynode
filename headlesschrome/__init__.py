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

    def _command(self, url, har, screenshot, js='false', js_result='false'):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        return [self.node, os.path.join(this_dir, '..', 'chrome_gather', 'cli.js'),
                '--width', str(self.width), '--height', str(self.height),
                '--har', har, '--screenshot', screenshot,
                '--js', js, '--jsresult', js_result,
                '--timeout', str(self.timeout * 1000),
                url]

    def capture(self, url, har='har.json', screenshot='screenshot.png'):
        har = os.path.join(self.result_dir, har)
        screenshot = os.path.join(self.result_dir, screenshot)
        logging.debug(self._command(url, har, screenshot))
        try:
            subprocess.check_output(self._command(url, har, screenshot),
                    stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            msg = e.output.decode('utf-8').splitlines()[0]
            raise RuntimeError(msg)
        return { 'har': har, 'screenshot': screenshot }

    def run_js(self, url, js):
        with tempfile.NamedTemporaryFile() as fp:
            try:
                subprocess.check_output(
                        self._command(url, 'false', 'false', js, fp.name),
                        stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                msg = e.output.decode('utf-8').splitlines()[0]
                raise RuntimeError(msg)
            fp.seek(0)
            return fp.read().decode('utf8')
