from howfo.logger import logger as log
from app.controllers.hello_controller import get_hello_content


class demo_plugin:
    @staticmethod
    def get():
        return_data = get_hello_content()
        log.info("retuen data: {0}".format(return_data))
        return return_data, 200
