import base64
import xbmcgui
import xbmc
import xbmcplugin
import xbmcaddon
from bs4 import BeautifulSoup
import requests
import re
import sys
import time
import six
import json
import resolveurl
from xbmcgui import ListItem

#xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", str(sys.path))
#from datos1 import makeRequest

def encode(page_data, a):
    c = base64.b64encode(a.encode('utf-8'))
    return c
def decourl_photocall(url):
    headers = {'User-Agent': 'iPad'}
    response = requests.get(url, headers=headers)
    html_content = response.text  
    xbmc.log(f"URL final encontrada en bruto: {html_content}")
    xbmcgui.Dialog().ok("Estoy dentro de m3u", "Ole")            
    
    #match = re.search(regex, html_content)
    #url_final = match.group(1)
def addme(page_data, a, b):
    return a + b  

def lista_pelis (url):
    #ASI SE PIDE A PALANTIR LA LISTA DE PELICULAS Y EN EL xml EXTERNALLINK

    Paso_1 = '{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":[ "plot","playcount","director", "genre","votes","duration","trailer","premiered","thumbnail","title","year","dateadded","fanart","rating","season","episode","studio","mpaa"]},"id":1}' % url
    Paso_2 = xbmc.executeJSONRPC(Paso_1)
    movie_list = json.loads(Paso_2)
    total = 0
    #xbmcplugin.setPluginCategory(int(sys.argv[1]), "Películas")
    #xbmcplugin.setContent(int(sys.argv[1]), "videos")
    
    # Iterar sobre cada película en la lista
    for movie in movie_list.get('result', {}).get('files', []):
        total += 1
        # Obtener la URL de la película
        movie_url = movie.get('file', '')
        name = movie.get('title', '')
        fanart = movie.get('fanart', '')
        plot = movie.get('plot', '')
        thumbnail = movie.get('thumbnail', '')
        
        # Crear un ListItem para la película
        liz = xbmcgui.ListItem(name)
        liz.setArt({'thumb': thumbnail, 'fanart': fanart})
        liz.setInfo('video', {'plot': plot})
        
        # Añadir la película al directorio
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=movie_url, listitem=liz, totalItems=total, isFolder=False)
        #xbmcgui.Dialog().ok("a ver", str(total))
    # Finalizar el directorio
    xbmcplugin.endOfDirectory(int(sys.argv[1]), succeeded=True)
    sys.exit()
    
    
def m3u(page_data, url):
    #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", url)   
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text    
    match = re.search("setVideoHLS\('(.+?)'", html_content)
    url_final = match.group(1)
    #xbmcgui.Dialog().ok("Estoy dentro de m3u", url_final)            
    #xbmc.log("URL final encontrada: {}".format(url_final))
    return url_final
def vidhide_descarga(url):   
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=xbmcgui.ListItem(path=url))
    
def vidhide(url, foto, fondo, info):
    #xbmcgui.Dialog().textviewer("esto dentro ", "de la funcion vidhide")
    import default
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text 
    
    matches = re.findall(r'link":"([^"]+)', html_content)  
    #links = [match for match in matches]AQUI LO COGE DE SERIE https://vidhidepre.com/file...................
    links = [match for match in matches]
    contador_link = len(links)
    matches = re.findall(r'(?s)title":"([^"]+)', html_content)  
    titulos = [match for match in matches]
    
    lista_combinada = list(zip(titulos, links))
    
    #xbmcgui.Dialog().textviewer("COMUNICACION ", str(lista_combinada))
 
    for titulo, link in lista_combinada:        
        # Llamar a la función addLink en el módulo default
        default.addLink(url=link, name=titulo, iconimage=foto, fanart=fondo, description=info, genre='', date='', showcontext=False, playlist=None, regexs=None, total=contador_link)
    #xbmc.executebuiltin("Container.SetSortMethod(1)")##para verlo en orden todos los capitulos
    xbmc.executebuiltin("Container.SetViewMode(515)")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))    
    sys.exit()


    

        
    

##############              PEDIR CARPETA MAS LIMPIO A PCCLOUD            ##################################
def Pcloud(url):
#con esto llegamos a descargar la url siendo un objeto de BeautifulSoup la variable soup   
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text    
    #parece que esta linea no hubiera hecho falta soup = BeautifulSoup(html_content, 'html.parser')
    
#aqui el objeto a texto con str(soup), buscamos para darle valor a v1    
    match = re.search('(?s)"path": "([^"]+)', html_content)
  #aqui la extracion se la damos a la variable v2
    v2 = match.group(1)
    
#aqui el objeto a texto con str(soup) y buscamos en este texto        
    match = re.search('(?s)"hosts":.*?"([^"]+)', html_content)
  #aqui la extracion se la damos a la variable v1      
    v1 = match.group(1)   
    
# construir la url reemplazando \ por nada para que quede correctamente construida
    url_final = f"https://{v1}{v2}".replace("\\", "")
    #xbmc.log("resultado variable 2: " + url_final, xbmc.LOGINFO)
    #xbmcgui.Dialog().textviewer("resultado variable 2", url_final)
    #sys.exit()
    return url_final 
####################################################################################################            
##############              PEDIR CARPETA A PCCLOUD  version antigua     ##################################
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
    
    # Utilizar la variable bus_sin_backslash en tu URL final
    url_final = f"https://{v2}{v1}".replace("\\", "")
    #xbmc.log("resultado variable 2: " + url_final, xbmc.LOGINFO)
    #xbmcgui.Dialog().textviewer("resultado variable 2", url_final)
    return url_final 
####################################################################################################
##############              PEDIR FICHERO A PCCLOUD            #################################
def Archivo_pcloud(page_data, url):
    #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", url)   
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text    
                                    #aqui buscamos para darle valor a v1    
    match = re.search('(?s)"downloadlink": "([^"]+)', html_content)
    v1 = match.group(1)    
    url_final = f"{v1}".replace("\\", "")    
    return url_final
    
#xbmc.log(url_final, xbmc.LOGINFO)
    #xbmcgui.Dialog().ok("A ver", "al log para ver la url")
    #sys.exit()    
##############              PEDIR FICHERO A PCCLOUD  version antigua          ##################################
def Fullpcloud(page_data, url):
    #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", url)   
    response = requests.get(url)
    html_content = response.text    
    soup = BeautifulSoup(html_content, 'html.parser')
 
    element = soup.find(text=re.compile(r'(?s)"downloadlink": "https:\\/\\/([^"]+)'))
    #xbmcgui.Dialog().textviewer("aqui ya se ve el contenido web", element)
    if element:
        match = re.search(r'(?s)\"downloadlink\": \"https:\\/\\/([^"]+)', element)
        
        if match:
            v1 = match.group(1)
            #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", v1)
            v1 = v1.replace(r"\/", "/")
            url_final = f"https://{v1}"
            #xbmc.log("resultado variable 2: " + url_final, xbmc.LOGINFO)
            #xbmcgui.Dialog().textviewer("resultado variable 2", url_final)
            #xbmcgui.Dialog().textviewer("estoy dentro de mi funcion", url_final)
            return url_final
#############################################################################################################

            

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

def petir(url1):
        from default import addLink
        addLink(url=url1, name="", iconimage="", fanart="", description="", genre="", date="", showcontext="", playlist="", regexs="", total=0)
        
        
        
        
#funciono 3 o 4 veces pero luego no
    #comando = 'ActivateWindow({}, "{}")'.format(str(ventana_id), url)    
    #xbmcgui.Dialog().textviewer("url final", comando)
    #xbmc.sleep(2000)
    #   
    #xbmc.executebuiltin(comando)
    #xbmc.executebuiltin('Dialog.Close(all, true)')# Cierra todos los diálogos modales
    #time.sleep(1)
    #xbmc.executebuiltin('Container.SetViewMode(500)')
    #xbmc.executebuiltin("Container.SetViewMode(fanart)")
    #xbmc.executebuiltin("Container.SetViewMode(53)")
    #xbmc.executebuiltin(url)

def abrir_ventana(page_data, url): 
    #funciona perfectamente
    xbmcgui.Dialog().textviewer("abrir_ventana", str(url))
    import default    
    default.mode = 53
    default.viewmode = 500
    default.pluginquerybyJSON(url)   
    xbmc.log("he vuelto " + str(url), xbmc.LOGINFO)
    sys.exit()
    
    
def tocar_puerta(page_data, url): 
        addon_id = 'plugin://plugin.video.palantir3'

        # Obtener información de introspección
        result = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"JSONRPC.Introspect","params":{"filter":{"type":"addon","id":"%s"}},"id":1}' % addon_id)
        

        # Mostrar el resultado en el archivo de registro de Kodi
        xbmc.log("he vuelto " + str(result), xbmc.LOGINFO)

            
    
    #xbmcgui.Dialog().textviewer("url final", url)

        
def trailers(page_data, url):
    try:
        addon_id = 'plugin.video.imdb.trailers'
        addon = xbmcaddon.Addon(addon_id)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=url))
    except Exception:
        pass  # No hacer nada en caso de error, simplemente ignorarlo 
def repo(page_data, url):
    try:
        addon_id = 'script.luar'
        addon = xbmcaddon.Addon(addon_id)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=url))
    except Exception as e:        
        print(f"Error en la función repo: {e}")
    pass  # No hacer nada en caso de error, simplemente ignorarlo        