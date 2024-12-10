import requests
import re
import xbmcvfs
import xbmc
import xbmcgui
import sys
def carpeta(url, foto, fondo, info):
    if url == "":
        xbmcgui.Dialog().ok("Aviso informativo", "Estará proximamente")
        sys.exit()
    TRANSLATEPATH = xbmcvfs.translatePath
    url_local = 'special://home/addons/plugin.video.play/capitulos_vidhide.html'
    direccion = TRANSLATEPATH(url_local)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Lanza una excepción para errores HTTP
    html_content = response.text
    

    links = re.findall(r'link":"([^"]+)', html_content)
    if "wish" in html_content:
        #xbmc.log(html_content, xbmc.LOGINFO)
        links = [link.replace('wishonly.site', 'strwish.com') for link in links]
    #links = [link + '|User-Agent=Mozilla/5.0(WindowsNT10.0;WOW64;rv:49.0)Gecko/20100101Firefox/49.0' for link in links]
    if "vidhidepre" in html_content:
        links = [link.replace('file', 'v') for link in links]
    #xbmc.log(str(links), xbmc.LOGINFO)
    #xbmcgui.Dialog().ok("links", str(links))
    titulos = re.findall(r'title":"([^"]+)', html_content)    
    tiempo = re.findall(r'length":(\d+)', html_content)
    tiempos = []
    for num in tiempo:
        segundos = int(num)
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segundos_restantes = segundos % 60
        tiempos.append(f"{horas}:{minutos:02}:{segundos_restantes:02}")
    #xbmcgui.Dialog().ok("links", str(tiempos))
    lista_combinada = list(zip(titulos, links, tiempos))
    items_contenido = ""
    for titulo, link, tiempo in lista_combinada:
        items_contenido += f"""
<item>
    <title>[COLOR forestgreen]{titulo}[/COLOR]      [B]&lt;&lt; [/B][COLOR orange]{tiempo}[/COLOR] [B]&gt;&gt;[/B]</title>
    <inputstream>$doregex[series]</inputstream>
    <regex>
        <name>series</name>
        <expres>$pyFunction:petra.cajon("trailer", "{link}", "1", "", "")</expres>
        <page></page>
    </regex>
    <thumbnail>{foto}</thumbnail>
    <fanart>{fondo}</fanart>
    <info>{info}</info>
</item>"""        

    try:
        # Leer el contenido actual del archivo
        with open(direccion, 'r', encoding='utf-8') as archivo:
            contenido_actual = archivo.read()
    except FileNotFoundError:
        #xbmcgui.Dialog().ok("Error de Archivo", "No se encontró el archivo en la ruta especificada.")
        return
    except IOError as e:
        #xbmcgui.Dialog().ok("Error de Archivo", f"No se pudo leer el archivo: {e}")
        return

    pos_inicio_items = contenido_actual.find("<items>")
    pos_fin_items = contenido_actual.find("</items>")
    
    if pos_inicio_items != -1 and pos_fin_items != -1:
        # Crear el nuevo contenido reemplazando lo que está entre <items> y </items>
        contenido_modificado = (contenido_actual[:pos_inicio_items + len("<items>")] + 
                                "\n" + items_contenido + "\n" + 
                                contenido_actual[pos_fin_items:])
        
        try:
            # Escribir el contenido modificado de vuelta al archivo
            with open(direccion, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_modificado)
            #xbmcgui.Dialog().ok("Éxito", "El archivo se actualizó correctamente.")
        except IOError as e:
            #xbmcgui.Dialog().ok("Error de Archivo", f"No se pudo escribir en el archivo: {e}")
            return
    else:
        xbmc.log("Error", xbmc.LOGINFO)
        xbmcgui.Dialog().ok("Error de XML", "No se encontró la etiqueta <items> en el archivo.") 
        return

    #xbmcgui.Dialog().ok("Proceso Completado", f"El archivo ha sido actualizado: {direccion}")
    
    return direccion
