from neirwork.proxy_controller import AvalibleProxies
from neirwork.controller import DeepinfraController
import requests
import json

if __name__ == '__main__':
    print('start proxy')
    pr = AvalibleProxies()
    nc = DeepinfraController()
    nc.add_message('Привет', 'user')
    json_data = nc.create_json_data()
    
    proxies = pr.get_available_proxies()
    while proxies == []:
        print('another')
        pr.update_proxies()
        proxies = pr.get_available_proxies()
    proxies = pr.ip_to_proxy(proxies[0])
    print('proxy: ', proxies)

    response = requests.post('https://api.deepinfra.com/v1/openai/chat/completions', json=json_data, proxies=proxies)
    print(response.text)
    resp_text = ''.join([json.loads(i)['choices'][0]['delta']['content'] for i in response.text.split('data: ') if i != '' and not '[DONE]' in i and 'content' in json.loads(i)['choices'][0]['delta'].keys()])

    print(resp_text)