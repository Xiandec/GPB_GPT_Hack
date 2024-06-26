from helper.fp import FreeProxy
import logging
logging.basicConfig(level=logging.INFO)

class Singleton(object):
    """
    Singleton class
    """
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class Proxy():
    def __init__(self, ip: str) -> None:
        self._ip = ip
        self._uses = 0
    
    def get_ip(self) -> dict:
        """
        Конвертирует `IP` в словарь для `requests`

        `http://148.251.76.237:1808` -> `{'https': 'http://148.251.76.237:18080'}`
        """
        return {
            'https': self._ip
        }
    
    def get_uses(self) -> int:
        return self._uses

    def use(self) -> None:
        self._uses += 1
        return

class AvalibleProxies(Singleton):
    """
    Class for saving avalible proxies
    """
    def __init__(self, ):
        self._proxies = set()
        self._used_proxies = set()
    
    def update_proxies(self, ) -> None:
        logging.info("Find avalible proxies")
        proxy = FreeProxy(https=True, timeout=1).get()
        logging.info(f"Proxy: {proxy}")
        while proxy == []:
            logging.info("No avalible proxies, retrying...")
            proxy = FreeProxy(https=True, timeout=1).get()
            logging.info(f"Proxy: {proxy}")
        avalible_proxies = [i['https'] for i in proxy]
        self._proxies.update(avalible_proxies)
        return

    def get_available_proxies(self, ) -> list:
        if len(self._proxies - self._used_proxies) == 0:
            self.update_proxies()
        return list(self._proxies - self._used_proxies)
    
    def update_used_proxies(self, proxy: str) -> None:
        self._used_proxies.add(proxy)
        return
    
    def ip_to_proxy(self, ip: str) -> dict:
        """
        Конвертирует `IP` в словарь для `requests`

        `http://148.251.76.237:1808` -> `{'https': 'http://148.251.76.237:18080'}`
        """
        return {
            'https': ip
        }

