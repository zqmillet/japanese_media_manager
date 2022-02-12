import http
import os
import signal
import multiprocessing
import contextlib
import tornado.web
import tornado.ioloop

def start_tornado(api_path, port, method, responses, queue):
    class RequestHandler(tornado.web.RequestHandler): # pylint: disable = abstract-method
        response_index = 0

    def _method(self, *args, **kwargs): # pylint: disable = unused-argument
        response = responses[RequestHandler.response_index % len(responses)]
        RequestHandler.response_index += 1
        self.set_status(response.get('status_code', http.HTTPStatus.OK))
        self.finish(response['response'])

    setattr(RequestHandler, method, _method)
    RequestHandler.response_index = 0

    application = tornado.web.Application([(api_path, RequestHandler)])
    application.listen(port)

    try:
        queue.put(None)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()


@contextlib.contextmanager
def mock_server_manager(api_path, responses, port=8001, method='get'):
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=start_tornado, args=(api_path, port, method, responses, queue), daemon=True)
    process.start()
    queue.get()
    yield
    os.kill(process.pid, signal.SIGINT)
    process.join()
