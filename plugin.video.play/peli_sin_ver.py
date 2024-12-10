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
import os
import xbmcvfs
import sqlite3
import urllib
from urllib.parse import unquote

kodi_version = xbmc.getInfoLabel('System.BuildVersion')
if kodi_version.startswith('19'):    
    db_name = "MyVideos119.db"
elif int(kodi_version.split('.')[0]) >= 20:    
    db_name = "MyVideos121.db"
else:
    raise RuntimeError("Versión de Kodi no compatible")
TRANSLATEPATH = xbmcvfs.translatePath
def ruta_especial(url):
    
    TRANSLATEPATH = xbmcvfs.translatePath
    url = 'special://home/addons/plugin.video.play/resources/lib/por_ver.html'
    a = TRANSLATEPATH(url)
    retocada = a.replace("\\","\\\\")
    #xbmc.log(retocada, xbmc.LOGINFO)
    #xbmcgui.Dialog().ok("Resultados de la búsqueda en la tabla files", retocada)
    return a
    

def reproducir_por_idfile(idfile):
    try:
        # Crear la URL del archivo utilizando el idfile
        url = f"plugin://plugin.video.library?action=play&idfile={idfile}"
        xbmcgui.Dialog().ok("Resultados de la búsqueda en la tabla files", str(url))
        # Crear un objeto ListItem con la URL
        list_item = xbmcgui.ListItem(path=url)

        # Iniciar la reproducción del archivo
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=list_item)
    except Exception as e:
        xbmcgui.Dialog().ok("Error al reproducir el archivo:", e)
    sys.exit()
# Llamar a la función y pasar el idfile que deseas reproducir

def eliminar_contenido_entre_etiquetas(ruta_archivo):
    # Abrir el archivo en modo lectura y escritura
    with open(ruta_archivo, 'r+', encoding="utf-8") as archivo:
        contenido = archivo.read()
        # Buscar y eliminar el contenido entre las etiquetas <item> y </item>
        contenido_modificado = re.sub(r'<item>.*?</item>', '', contenido, flags=re.DOTALL)
        # Regresar al inicio del archivo y escribir el contenido modificado
        archivo.seek(0)
        archivo.write(contenido_modificado)
        # Truncar el archivo para eliminar cualquier contenido adicional
        archivo.truncate()
        
        contenido_final = re.sub(r'\n\s*\n', '\n', contenido_modificado)
        archivo.seek(0)
        archivo.write(contenido_final)
        archivo.truncate()
        #xbmcgui.Dialog().ok("costruir_xml", "Hecho")
        #sys.exit()
contador_peliculas = 0
def costruir_xml(url, foto, titulo, direccion):
    global contador_peliculas
    contador_peliculas += 1
    #xbmc.log(url, xbmc.LOGINFO)
    #xbmcgui.Dialog().ok("costruir_xml", url)
    url = str(url)
    if "pyFunction" in  url and "myFunctions.Pcloud" in url:
        contenido = f"""
<item>
<title>El patron</title>
<link>$doregex[pagina]</link>

	<regex>
		<name>pagina</name>
		
		<listrepeat><![CDATA[
		<title>[COLOR blue]C[pagina.param1][/COLOR]</title>
		<inputstream>$doregex[elpatron]</inputstream>	<thumbnail>https://m.media-amazon.com/images/M/MV5BZGFmNGU5OWUtZmM4Zi00NjU2LTgzYTEtODJiMTNiMTEyMGU5XkEyXkFqcGdeQXVyMTcxNTYyMjM@._V1_.jpg</thumbnail><fanart>https://images.mubicdn.net/images/film/198080/cache-312808-1518696377/image-w1280.jpg</fanart>		
		]]></listrepeat>
		<expres>(?s)"name": "C([^.]+).*?fileid": ([^,]+)</expres>
		<page>https://e.pcloud.link/publink/show?code=kZknG1ZoIxX3egPFMLDuPTzgrx3DfTDrQS7</page>
		<cookieJar></cookieJar>
	</regex>
	
	<regex>
        <name>elpatron</name>
        <expres>$pyFunction:myFunctions.Pcloud("https://eapi.pcloud.com/getpublinkdownload?fileid=[pagina.param2]&forcedownload=true&code=kZknG1ZoIxX3egPFMLDuPTzgrx3DfTDrQS7")</expres>
        <page></page>
    </regex>
	                  
<thumbnail>https://m.media-amazon.com/images/M/MV5BYWM5ZjljNDQtMzIwNS00ZmZiLWE1MWUtNjAxYmIyNDUyMGRlXkEyXkFqcGdeQXVyNjUxOTkzOTk@._V1_.jpg</thumbnail>
<fanart>https://images.mubicdn.net/images/film/198080/cache-312808-1518696377/image-w1280.jpg</fanart>
</item>"""
   
    elif "pyFunction" in  url and "petra.cajon" in url:
        if any(substring in url for substring in ["vidhide", "dhtpre", "wish", "filemoon", "upstream", "vtube", "gamovideo", "videzz.net", "vidoza.net"]):       
                       
            contenido = f"""
<item>
    <title>{titulo}</title>
    <inputstream>$doregex[series]</inputstream>
    <regex>
        <name>series</name>
        <expres>{url}</expres>
        <page></page>
    </regex>
    <thumbnail>{foto}</thumbnail>
</item>"""
            #xbmcgui.Dialog().ok("3 condiciones", url)   
        else:    
            # Contenido a escribir entre las etiquetas <item></item>
            contenido = f"""
    <item>
        <title>{titulo}</title>
        <urlsolve>$doregex[series]</urlsolve>
        <regex>
            <name>series</name>
            <expres>{url}</expres>
            <page></page>
        </regex>
        <thumbnail>{foto}</thumbnail>	
    </item>"""
#elif all(s in url for s in ["pyFunction", "petra.cajon", "vidhide"]):
    #xbmcgui.Dialog().ok("terminado lanza el listado", str(url))
    
           
    elif "plugin://plugin.video.duffyou" in url or "plugin.video.moestv" in url:
        # Contenido a escribir entre las etiquetas <item></item>
        contenido = f"""
<item>
<title>{titulo}</title>
<link>{url}</link>
<thumbnail>{foto}</thumbnail>
</item>"""
    elif "pyFunction" in  url and "myFunctions.Archivo_pcloud" in url:
        # Contenido a escribir entre las etiquetas <item></item>
        contenido = f"""
<item>
<title>{titulo}</title>
<inputstream>$doregex[pagina]</inputstream>

	<regex>
		<name>pagina</name>
		<expres>{url}</expres>
		<page></page>
	</regex>
	
<thumbnail>{foto}</thumbnail>
</item>"""
    
    
    else:
        # Contenido a escribir entre las etiquetas <item></item>
            contenido = f"""
        <item>
            <title>{titulo}</title>
            <urlsolve>{url}</urlsolve>            
            <thumbnail>{foto}</thumbnail>	
        </item>"""
        
    # Ruta del archivo
    ruta_archivo = direccion  # Reemplaza 'ruta/a/tu/archivo.xml' con la ruta de tu archivo

    # Leer el contenido actual del archivo
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido_actual = archivo.read()

    # Buscar la posición de la etiqueta <items> en el contenido actual
    pos_items = contenido_actual.find("<items>")

    if pos_items != -1:
        # Insertar el nuevo contenido después de la etiqueta <items>
        contenido_modificado = contenido_actual[:pos_items + len("<items>")] + "\n" + contenido + contenido_actual[pos_items + len("<items>"):]
        
        # Escribir el contenido modificado de vuelta al archivo
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_modificado)
        
        #xbmcgui.Dialog().ok("costruir_xml", "Hecho")
        return
    else:
        xbmcgui.Dialog().ok("costruir_xml", "Error: No se encontró la etiqueta <items> en el archivo.")
    
    
def pelis_a_medias(url):
    ruta_especial_kodi = xbmcvfs.translatePath("special://database/").encode("utf-8").decode("utf-8")        
    nombre_db = db_name
    ruta_completa_db = os.path.join(ruta_especial_kodi, nombre_db)
    
    conexion = sqlite3.connect(ruta_completa_db)
    cursor = conexion.cursor()
    cursor.execute("SELECT idfile FROM bookmark")    
    idfiles = cursor.fetchall()
    
    # Crear una lista para almacenar los resultados de la búsqueda en la tabla files
    resultados_files = []
    
    # Buscar los idfile en la tabla files
    for idfile in idfiles:
        #cursor.execute("SELECT strFilename FROM files WHERE idfile = ? AND strFilename LIKE 'plugin://plugin.video.play%'", (idfile[0],))
        ########## FILTRA LA BASE DE DATOS A SOLO MI ADDON
        cursor.execute("SELECT strFilename FROM files WHERE idfile = ?", (idfile[0],))
        
        resultados_files.extend(cursor.fetchall())
        
            
    # Cerrar la conexión con la base de datos
    conexion.close()
    #for index, tupla in enumerate(resultados_files):
        #tupla = f"Tupla {index + 1}: {tupla}"
        #xbmc.log(tupla, xbmc.LOGINFO)
        #xbmcgui.Dialog().ok(f"Tupla {index + 1}:", tupla)
    
    decodificadas = [tuple(unquote(url) for url in tupla[0].split('&')) for tupla in resultados_files]    
    
    TRANSLATEPATH = xbmcvfs.translatePath
    url = 'special://home/addons/plugin.video.play/resources/lib/por_ver.html'
    a = TRANSLATEPATH(url)
    eliminar_contenido_entre_etiquetas(a)
    extracion_1 = ""
    extracion_2 = ""
    titulo = ""
    for index, tupla in enumerate(decodificadas):
        tupla = f"Tupla {index + 1}: {tupla}"
        #xbmc.log(tupla, xbmc.LOGINFO)
        #xbmcgui.Dialog().ok(f"Tupla {index + 1}:", tupla)
        #AQUI LO QUE HAY ES EXLUIR EL PORNO Y LA CAPERTA DE PCLOUD
        if "xvideos" in tupla or "pornhub" in tupla or "xnxx.com" in tupla:
            #xbmcgui.Dialog().ok("contine", "xvideos")
            continue
                     
        elif "pyFunction" in tupla:
            matches = re.search(r"(?s)expres\\': \\'(.*?\))\\',", tupla)
            if matches:
                extracion_1 = matches.group(1)  
                #xbmc.log(extracion_1, xbmc.LOGINFO)
                #xbmcgui.Dialog().ok("Tupla {index + 1}:", "extracion_1")
                extracion_1 = extracion_1.replace("\\\\\\'", "'")                
                               
            matches = re.search(r"(?s)iconimage=(.*?)',", tupla)
            if matches:
                extracion_2 = matches.group(1)
                 
            matches = re.search(r"(?s)nombre=(.*?)'", tupla)
            if matches:                
                titulo = matches.group(1)
                titulo = titulo.replace("+", " ")
                #xbmcgui.Dialog().ok("terminado lanza el listado", str(titulo))
            else:
                titulo = "Sin nombre"
                #xbmc.log(extracion_2, xbmc.LOGINFO)
                #xbmcgui.Dialog().ok(f"Tupla {index + 1}:", extracion_name)
            
            costruir_xml(extracion_1, extracion_2, titulo, a)
        else:
            matches = re.search(r"(?s)url=([^']+)", tupla)
            if matches:
                extracion_1 = matches.group(1)
                #xbmc.log(extracion_1, xbmc.LOGINFO)
                #xbmcgui.Dialog().ok(f"Tupla {index + 1}:", extracion_1)
                if "\\n" in extracion_1:
                    matches = re.search(r"(?s)url=([^\\]+)", tupla)
                    extracion_1 = matches.group(1)
                    #xbmc.log(extracion_1, xbmc.LOGINFO)
                    #xbmcgui.Dialog().ok(f"Tupla {index + 1}:", "dentro de if \\n")
            matches = re.search(r"(?s)iconimage=([^']+)", tupla)
            if matches:
                extracion_2 = matches.group(1)
                
            matches = re.search(r"(?s)nombre=(.+)", tupla)
            if matches: 
                
                titulo = matches.group(1)
                #xbmcgui.Dialog().ok("terminado lanza el listado", str(titulo))
                
                titulo = titulo.replace("+", " ").replace("')", "").replace('")', "")
                #xbmcgui.Dialog().ok("terminado lanza el listado", str(titulo))
            else:
                titulo = "Sin nombre"
            costruir_xml(extracion_1, extracion_2, titulo, a)
    #ruta_especial(url)
    #xbmcgui.Dialog().ok("terminado lanza el listado", str(a))
    return a
    
   
   
    
   