from helper.fp import FreeProxy

class Singleton(object):
    """
    Singleton class
    """
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

class AvalibleProxies(Singleton):
    """
    Class for saving avalible proxies
    """
    def __init__(self, ):
        self._proxies = set()
        self._used_proxies = set()
        self.update_proxies()
    
    def update_proxies(self, ) -> None:
        avalible_proxies = [i['https'] for i in FreeProxy(https=True).get()]
        self._proxies.update(avalible_proxies)
        return

    def get_available_proxies(self, ) -> list:
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

