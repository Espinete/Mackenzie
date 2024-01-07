import base64
import xbmcgui
import xbmc
import xbmcplugin
import xbmcaddon
from bs4 import BeautifulSoup
import requests
import re
import sys
def encode(page_data, a):
    c = base64.b64encode(a.encode('utf-8'))
    return c
    
def addme(page_data, a, b):
    return a + b  
    
def m3u(page_data, url):
    #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", url)   
    response = requests.get(url)
    html_content = response.text    
    soup = BeautifulSoup(html_content, 'html.parser')
 
    element = soup.find(text=re.compile(r"setVideoHLS\('(.+?)'\)"))
    if element:
        match = re.search(r"setVideoHLS\('(.+?)'\)", element)
        if match:
            url_final = match.group(1)
            #xbmcgui.Dialog().ok("Estoy dentro de getSoup", url_final)            
            #xbmc.log("URL final encontrada: {}".format(url_final))
            return url_final

def pedircarpeta(page_data, url):
    #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", url)   
    response = requests.get(url)
    html_content = response.text    
    soup = BeautifulSoup(html_content, 'html.parser')
 
    element_v1 = soup.find(text=re.compile(r'(?s)"path": "\\([^"]+)'))
    element_v2 = soup.find(text=re.compile(r'(?s)"hosts": \[.*?\"([^"]+)'))
    #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", element_v2) 
    if element_v1:
        match = re.search(r'(?s)"path": "\\([^"]+)', element_v1)
        if match:
            v1 = match.group(1)
            #xbmcgui.Dialog().textviewer("resultado variable 1", v1)            
    if element_v2:
        match = re.search(r'(?s)"hosts": \[.*?\"([^"]+)', element_v2)
        if match:
            v2 = match.group(1)
            #xbmcgui.Dialog().textviewer("resultado variable 2", v2)
            
    url_final = f"https://{v2}{v1}"
    #xbmcgui.Dialog().textviewer("resultado variable 2", url_final)
    return url_final 

def Fullpcloud(page_data, url):
    #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", url)   
    response = requests.get(url)
    html_content = response.text    
    soup = BeautifulSoup(html_content, 'html.parser')
 
    element = soup.find(text=re.compile(r'(?s)\"downloadlink\": \"https:\\/\\/([^"]+)'))
    #xbmcgui.Dialog().textviewer("aqui ya se ve el contenido web", element)
    if element:
        match = re.search(r'(?s)\"downloadlink\": \"https:\\/\\/([^"]+)', element)
        if match:
            v1 = match.group(1)
            v1 = v1.replace(r"\/", "/")
            url_final = f"https://{v1}"
            #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", url_final)
            return url_final 

def vidoza(page_data, url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',  # Puedes ajustar según sea necesario
    'Accept-Encoding': 'gzip, deflate, br',  # Puedes ajustar según sea necesario
    }
    response = requests.get(url, headers=headers)
    html_content = response.text  
    #xbmcgui.Dialog().textviewer("es aqui donde tienes que hacer el regex en la variable element", html_content)
    soup = BeautifulSoup(html_content, 'html.parser')    
    element = soup.find(text=re.compile(r'src: "([^"]+)'))
    url_final = None
    #xbmc.log(soup, level=xbmc.LOGDEBUG)
    xbmcgui.Dialog().textviewer("es aqui donde tienes que hacer el regex en la variable element", element)
    if element:
        match = re.search(r'src: "([^"]+)', element)
        
        if match:
            v1 = match.group(1)            
            url_final = f"{v1}"            
    #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", url_final)
    return url_final 

def drain(page_data, url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',  # Puedes ajustar según sea necesario
    'Accept-Encoding': 'gzip, deflate, br',  # Puedes ajustar según sea necesario
    }
    response = requests.get(url, headers=headers)
    html_content = response.text  
    xbmcgui.Dialog().textviewer("primer contacto", html_content)
    soup = BeautifulSoup(html_content, 'html.parser')    
    element = soup.find(text=re.compile(r'video\" content=\"([^"]+)'))
    url_final = None
    #xbmc.log(soup, level=xbmc.LOGDEBUG)
    xbmcgui.Dialog().textviewer("es aqui donde tienes que hacer el regex en la variable element", element)
    if element:
        match = re.search(r'video\" content=\"([^"]+)', element)        
        if match:
            v1 = match.group(1)            
            url_final = f"{v1}"            
    xbmcgui.Dialog().textviewer("url final", url_final)
    return url_final  

def petir(page_data, url):
   
        addon_id = 'plugin.video.palantir3'
               
        addon = xbmcaddon.Addon(addon_id)
    
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=url))
        
def trailers(page_data, url):
   
        addon_id = 'plugin.video.imdb.trailers'
               
        addon = xbmcaddon.Addon(addon_id)
    
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=url))
        