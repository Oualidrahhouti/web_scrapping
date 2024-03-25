from fp.fp import FreeProxy
import requests
from bs4 import BeautifulSoup

proxy = FreeProxy(country_id=['FR']).get(); proxy

proxy_list = [FreeProxy(country_id=['FR']).get() for x in range(3)]; proxy_list

proxies = {'http': proxy_list[1]} 
response = requests.get('http://httpbin.org/ip', proxies=proxies) 
print(response.json()['origin'])