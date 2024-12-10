import base64
import xbmcgui
import xbmc
import xbmcplugin
import xbmcaddon
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import quote
import sys
import time
import threading
import os
import xbmcvfs
import sqlite3
import urllib
from urllib.parse import urlparse

def desofuscar(url):
              #  Wish, Vidhide, Upstream, filemoon              
    regex = r"text/javascript'>(.*?)</script>"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    match = re.search(regex, html_content, re.DOTALL)
    
    if match:
        match = match.group(1)
        #xbmc.log("LA CAPTURA EN BRUTO ES " + str(match), xbmc.LOGINFO)
        #xbmcgui.Dialog().ok("auto_desofuscar", "vete al log")
    #else:
        #xbmcgui.Dialog().ok("Error 2701", "Ponte en contacto con el creador del addon para darle el código de error. Disculpe las molestias.")
        #sys.exit()
        
    #xbmc.log("LA CAPTURA EN BRUTO ES " + str(match), xbmc.LOGINFO)
    
    re_1 = r':\[\{([^\}]+)'
    re_p = re.search(re_1, match)
    if re_p:
        re_p = re_p.group(1)
        #xbmc.log("LA CAPTURA DE PLANTILLA  ES " + str(re_p), xbmc.LOGINFO)    
    re_2 = r"',36[^|]*([^']+)"
    re_k = re.search(re_2, match)
    if re_k:
        re_k = re_k.group(1)
        #xbmc.log("LA CAPTURA ARRAY ES " + str(re_k), xbmc.LOGINFO)
        #xbmcgui.Dialog().ok("auto_desofuscar", str(re_k))
############################################################################        
    p = re_p
    k = re_k
    a = 36
    #xbmc.log("para la variable p :  " + p, xbmc.LOGINFO)
    #xbmc.log("  para la variable k :  " + k, xbmc.LOGINFO)
    # Convierte k en una lista de elementos.
    k_list = k.split('|') 
    #xbmc.log("  para la variable k_list :  " + str(k_list), xbmc.LOGINFO)
    # Patrones para encontrar los índices ofuscados
    pattern = re.compile(r'\b[0-9a-zA-Z]+\b')
    #xbmc.log("  para la variable pattern :  " + str(pattern), xbmc.LOGINFO)
    # Función para obtener el reemplazo
    def reemplazo(match):
        # Extrae el índice desde el grupo del match
        index = int(match.group(0), a)
        if index < len(k_list):
            # Obtiene el valor de k_list
            valor_reemplazo = k_list[index]
            # Si el valor de reemplazo no es vacío, lo devuelve; de lo contrario, devuelve el texto original
            return valor_reemplazo if valor_reemplazo != "" else match.group(0)
        # Si el índice está fuera del rango, no realiza reemplazo
        return match.group(0)

    # Reemplaza las ocurrencias en el texto p utilizando la función reemplazo
    # Esto devuelve el texto modificado con los reemplazos
    p_modificado = pattern.sub(reemplazo, p)
########################################################################################      
    url_deo = p_modificado
    re_3 = r'file:"([^"]+)'
    url_sin = re.search(re_3, url_deo).group(1)
    url_con = url_sin + "|User-Agent=Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/127.0.0.0Safari/537.36"
    #xbmc.log("URL FINAL ES :  " + url_con, xbmc.LOGINFO)
    #if "https://" not in url_con:
        #pattern = r"p1=([^&]+)"
        #match = re.search(pattern, url_con)
        # Verificar si se encontró una coincidencia y obtener el valor
        #if match:
            #sp1_value = match.group(1)
            #url_con = f'https://{sp1_value}.upstreamcdn.co' + url_con
            #xbmcgui.Dialog().ok("valor de sp1", str(sp1_value))
    return url_con
    #
    
def resolver_Streamwish(url):
    regex = 'file: "([^"]+)'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    match = re.search(regex, html_content)
    if match:
        url_final = match.group(1)
        #xbmcgui.Dialog().ok("Estoy dentro de url_con_cabeza", str(url_final))
        url = url_final
    else:
        xbmcgui.Dialog().ok("Error 2701", "Ponte en contacto con el creador del addon para darle el código de error. Disculpe las molestias.")
        #sys.exit()    
    return url
def texto_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    return html_content
    
def url_con_cabeza(url, regex):    
    headers = {'User-Agent': 'iPad'}
    response = requests.get(url, headers=headers)
    html_content = response.text  
    
    match = re.search(regex, html_content)
    url_final = match.group(1)
    
    url_final_with_headers = f'''{url_final}|Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/98.0.4758.102Safari/537.36'''
    #return url_final_with_headers
    #xbmc.log(url_final_with_headers, xbmc.LOGINFO) 
    #xbmcgui.Dialog().ok("Estoy dentro de url_con_cabeza", str(url_final))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=xbmcgui.ListItem(path=url_final_with_headers))
    sys.exit()
    
def resolver_Vtube(url, regex1, regex2): 
    headers = {'User-Agent': 'iPad'}
    response = requests.get(url, headers=headers)
    html_content = response.text
        
    match = re.search(f"(?s){regex1}.*?{regex2}", html_content)
    cacho2 = match.group(1)    
    cacho1 = match.group(2)    
    url_final = f"https://{cacho1}.vtube.network/hls/{cacho2}.urlset/master.m3u8"  
    #xbmc.log(url_final, xbmc.LOGINFO) 
    url_final_with_headers = f'''{url_final}|Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/98.0.4758.102Safari/537.36'''
    return url_final_with_headers
    #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=xbmcgui.ListItem(path=url_final_with_headers))
    #sys.exit()
def resolve_vidhide(url):
    try:                
        resolved_url = desofuscar(url)           
        url = resolved_url        
        return url
        #xbmc.log(url, xbmc.LOGINFO) 
        #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=xbmcgui.ListItem(path=url))#con la url resuelta se la mandamos a kodi para que el reproductor la reproduzca
        
    except:
        html_content = texto_url(url)
        if "Video is processing" in html_content:
            xbmcgui.Dialog().ok("Aviso de codificación.", "Pendiente de codificación, cuando termine el proceso podrá disfrutar del video, disculpe las molestias.")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem())
            xbmc.executebuiltin('Dialog.Close(all)')
            #sys.exit()
        elif "vidhide" in url:
            url_descargas = url.replace("/v/", "/download/").replace("/file/", "/download/")   
            html_content = texto_url(url_descargas)                
            
            if '.mkv' in html_content:
                prefijo = "_n" 
                nueva_url_descargas = url_descargas + prefijo
                html_content = texto_url(nueva_url_descargas)
                
                if 'Downloads disabled' in html_content:
                    xbmcgui.Dialog().ok("Aviso de codificación", "Pendiente de codificación, cuando termine el proceso podrá disfrutar del video, disculpe las molestias.")
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem())
                    xbmc.executebuiltin('Dialog.Close(all)') 
        
        elif "Please allow a few hours for the file to be" in html_content or "Please give us some time" in html_content:       
            xbmcgui.Dialog().ok("Servidor en mantenimiento", "Espere unas horas para que el archivo se transfiera a un servidor de mayor rendimiento. Gracias por su paciencia.")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem())
            xbmc.executebuiltin('Dialog.Close(all)')                
        elif "File Not Found" in html_content:
            xbmcgui.Dialog().ok("Archivo borrado", "Contacte con el creador del addon para que repare el enlace. Si no le avisa, él no sabrá que este enlace tiene que repararlo. Disculpe las molestias.")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem())
            xbmc.executebuiltin('Dialog.Close(all)')
        else:
            xbmcgui.Dialog().ok("Error 2701", "Contacte con el creador del addon para darle el código de error. Disculpe las molestias.")
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem())
            xbmc.executebuiltin('Dialog.Close(all)')
    #xbmcgui.Dialog().ok("Error 2701", str(url))
bandera = True    
def ranking(titulo):
    ## con este regex capturas la fotos de los actores (?s)<li class="nb".*?src="(.*?)".*?</li>
    ## con este regex capturas el argunmento (?s)itemprop="description">(.*?)<
    titulo_sin_interrogacion = titulo.replace("¿", "").replace("?", "")
    titulo_codificado = quote(titulo_sin_interrogacion)
    #titulo = re.escape(titulo)
    url = f'https://www.filmaffinity.com/es/search.php?stype=title&stext={titulo_codificado}' 
    #xbmc.log(url, xbmc.LOGINFO)
    
    headers = {'User-Agent': 'iPad'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    #xbmc.log(html_content, xbmc.LOGINFO)
    #xbmcgui.Dialog().textviewer("ruta", "bakala")
    match = re.search('itemprop="description">', html_content)
    #xbmcgui.Dialog().ok("ruta", f"{match}")
    
    if not match:
        for match in re.finditer(r'(?s)<div class="mc-info-container">.*?href="(.*?)".*?title="(.*?)".*?alt="(.*?)".*?mc-year">(.*?)<', html_content):
            if match:
                url_filma = match.group(1)
                titulo_filma = match.group(2).replace("¿", "").replace("?", "")
                #titulo_filma_escape = re.escape(match.group(2))               
                alt_filma = match.group(3)
                ano = match.group(4)
                global bandera
                if bandera and ((alt_filma == 'España' or ano == '2016') and titulo_filma == titulo_sin_interrogacion):
   
                    if 'A pesar de todo' in titulo_filma:
                        for match in re.finditer(r'(?s)<a title="A pesar de todo.*?href="(.*?)".*?img class=".*?mc-year">(.*?)<', html_content):
                            url_filma = match.group(1)
                            ano_filma = match.group(2)
                            if ano_filma == '2019':
                                url = url_filma                   
                                headers = {'User-Agent': 'iPad'}
                                response = requests.get(url, headers=headers)
                                html_content = response.text
                                #xbmc.log(html_content, xbmc.LOGINFO)
                                #xbmcgui.Dialog().textviewer("A pesar de todo", "A pesar de todo")
                    else:                          
                        url = url_filma                   
                        headers = {'User-Agent': 'iPad'}
                        response = requests.get(url, headers=headers)
                        html_content = response.text
                            #xbmc.log(html_content, xbmc.LOGINFO)
                            #xbmcgui.Dialog().textviewer("ruta", "bakala")
                        #xbmc.log(f"URL obtenida: {html_content}", xbmc.LOGINFO)
                        #xbmcgui.Dialog().ok("localizar url", f'{titulo_filma}')
                        #xbmcgui.Dialog().ok("localizar url", f'{url_filma}   {titulo_filma}   {alt_filma}')
                        bandera = False
    # <a class="link"[^>]*> esto quiere decir que solo busque  por dentro de toda la etiqueta de a .*? que siga buscando hasta encontrar src="(.*?)" y capture su contenido 
    matches = re.findall(r'<li class="nb"[^>]*>.*?title="(.*?)".*?src="(.*?)"', html_content)

    # Limitamos la lista a las primeras 10 imágenes
    matches_limited = matches[:10]
    
    match = re.search(r'(?s)div class="avgrat-box">(.*?)<', html_content)
    if match:
        puntuacion = match.group(1)
        #xbmcgui.Dialog().ok("puntuacion de la peli", puntuacion)
    else:
        puntuacion = "--" 
    match = re.search(r'(?s)itemprop="description">(.*?)</dd>', html_content)
    if match:
        trama = match.group(1)
        #xbmcgui.Dialog().ok("trama", trama)
    else:
        trama = "Error 2701"
    return puntuacion, matches_limited, trama

def foto_lista():
     # Obtener la lista de reproducción de video
    playlist_id = xbmc.PLAYLIST_VIDEO
    #xbmc.log(f"Obteniendo la lista de reproducción de videos con ID {playlist_id}.", xbmc.LOGINFO)
    playlist = xbmc.PlayList(playlist_id)
    
    # Asegurarse de que la lista de reproducción no esté vacía
    size = playlist.size()
    #xbmc.log(f"Lista de reproducción de videos obtenida: tamaño {size}.", xbmc.LOGINFO)
    
    ###if size == 0:
        ###xbmc.log("La lista de reproducción de videos está vacía.", xbmc.LOGINFO)
        ###return
    
    #urls = []
    for index in range(size):
        item = playlist[index]
        #xbmc.log(f"Accediendo al elemento {index}.", xbmc.LOGINFO)
        if isinstance(item, xbmcgui.ListItem):
            # Obtener la URL del item, que normalmente se encuentra en el 'path'
            url = item.getPath()
            #xbmc.log(f"URL obtenida: {url}", xbmc.LOGINFO)
            #if url:
                #urls.append(url)
        else:
            xbmc.log(f"Elemento en la lista de reproducción no es un xbmcgui.ListItem: {item}", xbmc.LOGINFO)
    match = re.search(r"iconimage=(.*?)&", url)
    #xbmc.log(f"URL obtenida: {url}", xbmc.LOGINFO)
    #xbmcgui.Dialog().ok("dentro de petra.cajon", url)    
    
    if any(term in url for term in ['palantir', 'mega', 'rapidgator']): #re.search(r'palantir|mega|rapidgator', url):
        foto = 'https://dl.dropbox.com/scl/fi/xljdbiee07ody1xo0mimp/pasar_por_caja.jpg?rlkey=3o2mripsa3c14fqmzj2e6enoz&st=f5qb845n&dl=0'
    else:    
        foto = match.group(1)
   
    return foto
    #xbmcgui.Dialog().ok("dentro de petra.cajon", str(url))
    #sys.exit()
def cajon(trailer, url, saltar, sinopsis, titulo):
    
    #xbmcgui.Dialog().ok("dentro de petra.cajon", str(url))
    if titulo != "":
        foto = foto_lista()
        foto = urllib.parse.unquote(foto)        
        puntuacion_pelicula, fotos_filma, trama = ranking(titulo)
        
        if titulo != "Ocho pasos":
            sinopsis = trama.replace("(FILMAFFINITY)", "").replace("<br />", "") 
########################################################################################################## 
            ######### fotos_filma es una lista de tuplas cada tupla tiene el nombre y foto
        # Inicializar todas las variables con valores vacíos
        nombres = [""] * 10
        imagenes = [""] * 10

        # Asignar valores desde la tupla fotos_filma
        for i, (nombre, imagen) in enumerate(fotos_filma[:10]):
            nombres[i] = nombre
            imagenes[i] = imagen

        # Desempaquetar valores en variables explícitas
        n_ac1, n_ac2, n_ac3, n_ac4, n_ac5, n_ac6, n_ac7, n_ac8, n_ac9, n_ac10 = nombres
        ac1, ac2, ac3, ac4, ac5, ac6, ac7, ac8, ac9, ac10 = imagenes
############################################################################################################       
    salta_cajon = int(saltar)
    
    #Cuando salta_cajon es 1 y respuesta = 0 va directamente a darte la pelicula seccion hecha para cine kinki
    if salta_cajon == 1:
        respuesta = 0
        if any(substring in trailer for substring in ["duffyou", "moestv", "imdb", "vidhidepre"]) and url == "url":            
            respuesta = 1
            #xbmcgui.Dialog().ok("paso 1/4", "respuesta = 1")
    # Determinar la función de traducción de ruta adecuada según la versión de Kodi
    kodi_version = xbmc.getInfoLabel('System.BuildVersion')
    if kodi_version.startswith('19'):
        from xbmc import translatePath as variacion_translatePath
        db_name = "MyVideos119.db"
    elif int(kodi_version.split('.')[0]) >= 20:
        from xbmcvfs import translatePath as variacion_translatePath
        db_name = "MyVideos121.db"
    else:
        raise RuntimeError("Versión de Kodi no compatible")
    
    
    ruta_especial_kodi = xbmcvfs.translatePath("special://database/").encode("utf-8").decode("utf-8")        
    nombre_db = db_name
    ruta_completa_db = os.path.join(ruta_especial_kodi, nombre_db)
    #xbmcgui.Dialog().textviewer("ruta", str(ruta_completa_db))
    # Conecta con la base de datos SQLite
    conexion = sqlite3.connect(ruta_completa_db)
    cursor = conexion.cursor()
    #xbmc.log(str(cursor), xbmc.LOGINFO)
    #xbmcgui.Dialog().textviewer("ruta", str(cursor))
    try:
        # Consulta para obtener todos los datos de la columna strFilename de la tabla files
        cursor.execute("SELECT idFile, strFilename FROM files;")
        resultados = cursor.fetchall()
        
        # Variable para verificar si se encontraron datos
        datos_encontrados = False

        # Imprime los resultados en el log de Kodi
        for resultado in resultados:
            decoded_str_filename = urllib.parse.unquote(resultado[1])  # Decodificar la cadena
            #xbmc.log(f"ID: {resultado[0]}, strFilename: {decoded_str_filename}", xbmc.LOGINFO)
            
            
            if url in decoded_str_filename:
                # Se encontró la URL en el strFilename. Ahora, consultamos la tabla bookmark
                cursor.execute("SELECT idBookmark FROM bookmark WHERE idFile = ?;", (resultado[0],))
                bookmark_resultado = cursor.fetchone()

                if bookmark_resultado:
                    #xbmcgui.Dialog().ok("BINGO!!!!", f"Se encontró la URL en el strFilename. ID: {resultado[0]}\nID Bookmark: {bookmark_resultado[0]}")
                    salta_cajon = 1
                    respuesta = 0
                    if any(substring in trailer for substring in ["duffyou", "moestv", "imdb", "vidhidepre"]) and url == "url":
                        respuesta = 1
                        #xbmcgui.Dialog().ok("paso 2/4", "seguimos insistiendo en respuesta = 1")
                    conexion.close()
                #else:
                    #xbmcgui.Dialog().ok("BINGO!!!!", f"Se encontró la URL en el strFilename. ID: {resultado[0]}\nNo hay Bookmark asociado.")

                #datos_encontrados = True

        # Muestra el mensaje adecuado en el diálogo de Kodi
        #if not datos_encontrados:
            #xbmcgui.Dialog().ok("Datos encontrados.", "NINGUNO")

    except sqlite3.Error as e:
        xbmc.log(f"Error al consultar la base de datos: {e}", xbmc.LOGERROR)

    finally:
        # Cierra la conexión con la base de datos
        if conexion:
            conexion.close()
    #xbmcgui.Dialog().textviewer("ruta", str(cursor))
    

    #xbmcgui.Dialog().ok("ruta", str(salta_cajon))
    if salta_cajon == 0:
        if url.startswith('Estreno:'):
            dialog = xbmcgui.Dialog()
            respuesta = dialog.select('Próximamente......', [f'                                                        [COLOR pink][B]   {url}[/COLOR][/B]  ', '                                    <<  [COLOR green][B]Ver trailer[/B][/COLOR]  >>'])
        else:
            if sinopsis == "":
                dialog = xbmcgui.Dialog()
                respuesta = dialog.select('¿ Qué eliges ver ?                                                            ', ['                                <<<  [COLOR green][B]Ver película[/B][/COLOR]  >>>', '                                    <<  [COLOR green][B]Ver tráiler[/B][/COLOR]  >>'])
            else: 
                class CustomDialog(xbmcgui.WindowXMLDialog):
                    def __init__(self, *args, **kwargs):
                        super(CustomDialog, self).__init__(*args, **kwargs)
                        self.puntuacion = kwargs.get('puntuacion', 'puntuacion no disponible')
                        self.sinopsis = kwargs.get('sinopsis', 'Sinopsis no disponible')
                        self.N_ac1 = kwargs.get('N_ac1', 'N_ac1 no disponible')
                        self.N_ac2 = kwargs.get('N_ac2', 'N_ac2 no disponible')
                        self.N_ac3 = kwargs.get('N_ac3', 'N_ac3 no disponible')
                        self.N_ac4 = kwargs.get('N_ac4', 'N_ac4 no disponible')
                        self.N_ac5 = kwargs.get('N_ac5', 'N_ac5 no disponible')
                        self.N_ac6 = kwargs.get('N_ac6', 'N_ac6 no disponible')
                        self.N_ac7 = kwargs.get('N_ac7', 'N_ac7 no disponible')
                        self.N_ac8 = kwargs.get('N_ac8', 'N_ac8 no disponible')
                        self.N_ac9 = kwargs.get('N_ac9', 'N_ac9 no disponible')
                        self.N_ac10 = kwargs.get('N_ac10', 'N_ac10 no disponible')
                        self.foto = kwargs.get('foto', 'foto no disponible')
                        self.foto_ac1 = kwargs.get('foto_ac1', 'foto_ac1 no disponible')
                        self.foto_ac2 = kwargs.get('foto_ac2', 'foto_ac2 no disponible')
                        self.foto_ac3 = kwargs.get('foto_ac3', 'foto_ac3 no disponible')
                        self.foto_ac4 = kwargs.get('foto_ac4', 'foto_ac4 no disponible')
                        self.foto_ac5 = kwargs.get('foto_ac5', 'foto_ac5 no disponible')
                        self.foto_ac6 = kwargs.get('foto_ac6', 'foto_ac6 no disponible')
                        self.foto_ac7 = kwargs.get('foto_ac7', 'foto_ac7 no disponible')
                        self.foto_ac8 = kwargs.get('foto_ac8', 'foto_ac8 no disponible')
                        self.foto_ac9 = kwargs.get('foto_ac9', 'foto_ac9 no disponible')
                        self.foto_ac10 = kwargs.get('foto_ac10', 'foto_ac10 no disponible')
                        self.button_label = kwargs.get('button_label', 'Python')
                        self.button_label2 = kwargs.get('button_label2', 'Python2')
                        self.respuesta = None

                    def onInit(self):
                        try:
                            self.getControl(200).setImage(self.foto)
                            self.getControl(201).setImage(self.foto_ac1)
                            xbmc.log(f"Setting CurrentActor to: {self.N_ac1}", xbmc.LOGINFO)  # Log para depurar
                            xbmcgui.Window().setProperty("CurrentActor", self.N_ac1)  # Se establece la propiedad directamente
                            self.getControl(202).setImage(self.foto_ac2)
                            self.getControl(203).setImage(self.foto_ac3)
                            self.getControl(204).setImage(self.foto_ac4)
                            self.getControl(205).setImage(self.foto_ac5)
                            self.getControl(206).setImage(self.foto_ac6)
                            self.getControl(207).setImage(self.foto_ac7)
                            self.getControl(208).setImage(self.foto_ac8)
                            self.getControl(209).setImage(self.foto_ac9)
                            self.getControl(210).setImage(self.foto_ac10)
                            self.getControl(101).setLabel(self.puntuacion)
                            self.getControl(100).setText(self.sinopsis)
                            self.getControl(301).setLabel(self.N_ac1)
                            self.getControl(302).setLabel(self.N_ac2)
                            self.getControl(303).setLabel(self.N_ac3)
                            self.getControl(304).setLabel(self.N_ac4)
                            self.getControl(305).setLabel(self.N_ac5)
                            self.getControl(306).setLabel(self.N_ac6)
                            self.getControl(307).setLabel(self.N_ac7)
                            self.getControl(308).setLabel(self.N_ac8)
                            self.getControl(309).setLabel(self.N_ac9)
                            self.getControl(310).setLabel(self.N_ac10)
                            self.getControl(1).setLabel(self.button_label)
                            self.getControl(2).setLabel(self.button_label2)
                            # Aquí puedes configurar los controles si es necesario
                        except Exception as e:
                            xbmcgui.Dialog().textviewer("Error en onInit:", f'{str(e)}')
                            xbmc.log(f"Error en onInit: {str(e)}", xbmc.LOGERROR)
                    
                    def onClick(self, controlId):
                        if controlId == 10:  # El ID del botón "X"
                            self.close()  # Cierra el diálogo
                            
                        elif controlId == 1:
                            self.respuesta = 0
                            self.close()
                        elif controlId == 2:
                            self.respuesta = 1
                            self.close()

                    def getRespuesta(self):
                        return self.respuesta

                # Obtener ruta absoluta para el archivo XML
                addon = xbmcaddon.Addon()
                direccion = addon.getAddonInfo('path')

                # Crear y mostrar el diálogo personalizado
                dialog = CustomDialog('dialog_custom.xml', direccion, 'skin.xonfluence', foto = f'{foto}', foto_ac1 = f'{ac1}|User-Agent=iPad', 
                foto_ac2 = f'{ac2}|User-Agent=iPad', 
                foto_ac3 = f'{ac3}|User-Agent=iPad', 
                foto_ac4 = f'{ac4}|User-Agent=iPad', 
                foto_ac5 = f'{ac5}|User-Agent=iPad', 
                foto_ac6 = f'{ac6}|User-Agent=iPad', 
                foto_ac7 = f'{ac7}|User-Agent=iPad', 
                foto_ac8 = f'{ac8}|User-Agent=iPad', 
                foto_ac9 = f'{ac9}|User-Agent=iPad', 
                foto_ac10 = f'{ac10}|User-Agent=iPad', 
                N_ac1=f'{n_ac1}',
                N_ac2=f'{n_ac2}',
                N_ac3=f'{n_ac3}',
                N_ac4=f'{n_ac4}',
                N_ac5=f'{n_ac5}',
                N_ac6=f'{n_ac6}',
                N_ac7=f'{n_ac7}',
                N_ac8=f'{n_ac8}',
                N_ac9=f'{n_ac9}',
                N_ac10=f'{n_ac10}',
                puntuacion=f"{puntuacion_pelicula}", 
                sinopsis=f"{sinopsis}", 
                button_label=f"[COLOR orange][B]{titulo}[/B][/COLOR]", 
                button_label2="[B]Tráiler[/B]")
                dialog.doModal()

                # Recuperar la respuesta después de que el diálogo se haya cerrado
                respuesta = dialog.getRespuesta()
                #xbmc.log(f"Respuesta del diálogo: {respuesta}", xbmc.LOGDEBUG)
                del dialog
            
                ##dialog = xbmcgui.Dialog()
                ##respuesta = dialog.select('¿ Qué eliges ver ?                                                            ', ['                                <<<  [COLOR green][B]Ver película[/B][/COLOR]  >>>', '                                    <<  [COLOR green][B]Ver tráiler[/B][/COLOR]  >>', '[COLOR orange][B]                                            Sinopsis[/B][/COLOR]'])
       
    if respuesta in [-1, None]:
        url = 'DETENER'        
        return url
        #xbmcgui.Dialog().textviewer("estoy click en cancelar", url)
        #sys.exit()
        #
        #xbmcgui.Dialog().textviewer("estoy click en cancelar", str(respuesta))
        #xbmc.executebuiltin("Action(Back)")           
    elif respuesta == 0: 
        if any(substring in url for substring in ["vidhide", "dhtpre", "wish", "filemoon", "upstream", "vtube"]):
            
            url_final = resolve_vidhide(url) 
            #parsed_url = urlparse(url)
            #dominio = parsed_url.netloc
            #url_final += f"&Referer=https://{dominio}/&Origin=https://{dominio}"            
            #xbmc.log("PASO ULTIMO ANTES DE INPUTSTREAM:  " + url_final, xbmc.LOGINFO)
            #xbmcgui.Dialog().textviewer("paso ultimo antes de inputstream", url_final)
######################## ASI CONSTRUYE LA URL URLSOLVE: https://p2p.hgagecdn.com/hls2/01/02108/gi1yg7qb0lmy_n/master.m3u8?t=Up9oh8UlpDhQzZXs1NBbmHojuybrBev5USCatz5sBZE&s=1722956581&e=129600&f=10542809&srv=R7E4BBU6QXpa&i=0.4&sp=500&p1=R7E4BBU6QXpa&p2=R7E4BBU6QXpa&asn=212238|User-Agent=Mozilla/5.0+(Macintosh;+Intel+Mac+OS+X+17.1.2)+AppleWebKit/800.6.25+(KHTML,+like+Gecko)+Version/17.2+Safari/605.1.15&Referer=https://lulu.st/&Origin=https://lulu.st
            return url_final
        elif url.startswith('plugin://plugin.video.palantir3'):
            ###addon_id = 'plugin.video.palantir3'               
            ###addon = xbmcaddon.Addon(addon_id)    
            ###xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=url))
            #xbmcgui.Dialog().ok("estoy en petra", str(respuesta))
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=xbmcgui.ListItem(path=url))
            #xbmcgui.Dialog().textviewer("estoy click en cancelar", str(respuesta))
            sys.exit()
        elif url.startswith('Estreno:'):               
             # Ruta local al icono en la misma carpeta que tu script
            addon_icon_path = os.path.join(variacion_translatePath('special://home/addons/plugin.video.play'), 'icon.png')
            # Convierte la ruta local a una ruta special://
            icon_path = variacion_translatePath(addon_icon_path)

            # Muestra la notificación con la ruta especial
            xbmcgui.Dialog().notification('[COLOR green]                  No seas impaciente[/COLOR]', f'[COLOR pink][B]   {url}[/COLOR][/B]', icon=icon_path, time=4000)                
            sys.exit()
        elif "sendvid" in url:                 
            regex = '(?s)og:video. content="([^"]+)'
            url_con_cabeza(url, regex)            
        #if "asnwish" in url: 
            #xbmcgui.Dialog().ok("Estoy dentro de vidhidepre", "a ver ")
            #regex = '(?s): \[{file:"([^"]+)'
            #url_con_cabeza(url, regex) 
        elif "videzz.net" in url or "vidoza.net" in url:
            regex = 'src: "([^"]+)'
            url_con_cabeza(url, regex)
        elif "gamovideo" in url:
            regex = '(?s)sources:.*?file: "([^"]+)'
            url_con_cabeza(url, regex)
        elif "goodstream" in url or "pulpo" in url:
            regex = 'file: "([^"]+)'             
            url_con_cabeza(url, regex)            
        else:
            import resolveurl
            #xbmcgui.Dialog().ok("Estoy dentro de import resolveurl", str(url))
            resolved_url = resolveurl.resolve(url)            
            url = resolved_url
            
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=xbmcgui.ListItem(path=url))
            
    elif respuesta == 1:
        #xbmcgui.Dialog().ok("estoy en respuesta 1", trailer)
        if "imdb" in trailer:
            #xbmcgui.Dialog().ok("paso 3/4", "estoy dentro de imbd")
            #xbmc.log(trailer, xbmc.LOGINFO)
            trailer = trailer.replace("&amp;", "&")
            #xbmc.log(trailer, xbmc.LOGINFO)
            #xbmcgui.Dialog().ok("paso 4/4", "dentro de plugin://plugin.video.imdb.trailers")
            #addon_id = 'plugin.video.imdb.trailers'
            #addon = xbmcaddon.Addon(addon_id)
            list_item = xbmcgui.ListItem(path=trailer)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=list_item)
            sys.exit()
        elif "vidhide" in trailer or "dhtpre" in trailer or "wish" in trailer:
            trailer_final = resolve_vidhide(trailer)
            trailer = trailer_final
            return trailer
        elif trailer.startswith('plugin://plugin.video.moestv'):
            #xbmc.log(trailer, xbmc.LOGINFO)
            #xbmcgui.Dialog().ok("paso 4/4", "dentro de plugin://plugin.video.moestv")
            ### SE HIZO ASI POR QUE DE LA OTRA MANERA SERIA IMPOSIBLE
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=xbmcgui.ListItem(path=trailer))                        
            sys.exit()        
        elif trailer.startswith('plugin://plugin.video.duffyou'):
            #xbmcgui.Dialog().textviewer("estoy dentro de youtube", trailer)
            addon_id = 'plugin.video.duffyou'
            addon = xbmcaddon.Addon(addon_id)
            list_item = xbmcgui.ListItem(path=trailer)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=list_item)
            sys.exit()
        else:
            #xbmcgui.Dialog().ok("estoy en else", trailer)
            import resolveurl
            resolved_url = resolveurl.resolve(trailer)            
            url = resolved_url 
            pattern = r'https://[^\s]+'
            url_modi = re.search(pattern, url).group(0)            
            #xbmc.log("PASO ULTIMO ANTES DE INPUTSTREAM:  " + url, xbmc.LOGINFO)
            #xbmcgui.Dialog().textviewer("estoy en resolveurl", url)
            return url_modi
            ##xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=xbmcgui.ListItem(path=url_modi))#con la url resuelta se la mandamos a kodi para que el reproductor la reproduzca
    elif respuesta == 2: 
        xbmcgui.Dialog().textviewer("Sinopsis", f'{sinopsis}') 
        #xbmc.executebuiltin('Dialog.Close(all, true)')
        #cajon(trailer, url, saltar, sinopsis)
        sys.exit()#con esto se para dentro de la funcion y no vuelve al xml
                    