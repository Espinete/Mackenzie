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
from urllib.parse import urlparse

#chrome w10 = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
#opera w10 = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/80.0.4170.72
#brave w10 = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Brave/95.1.31.88
#firefox w10= Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0
#edge w10 = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55
#Safari en macOS = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15
#chrome android = Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36
#firefox andorid = Mozilla/5.0 (Android 10; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0
#Safari IOS = Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1
 
#regex = '(?s): \[{file:"([^"]+)'
def deofuscar(p, k):
    a=36
    # Convierte k en una lista de elementos.
    k_list = k.split('|') if isinstance(k, str) else k
    
    # Patrones para encontrar los índices ofuscados
    pattern = re.compile(r'\b[0-9a-zA-Z]+\b')

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

    return p_modificado





def auto_desofuscar(url):
              #  Wish, Vidhide, Upstream, filemoon              
    regex = r"text/javascript'>(.*?)</script>"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    match = re.search(regex, html_content, re.DOTALL)
    
    if match:
        match = match.group(1)
        #xbmc.log("LA CAPTURA EN BRUTO ES " + str(match), xbmc.LOGINFO)
        #xbmcgui.Dialog().ok("auto_desofuscar", "vete al log")
    else:
        xbmcgui.Dialog().ok("Primera captura con errores", "Error 2701")
        sys.exit()
    #xbmc.log("LA CAPTURA EN BRUTO ES " + str(match), xbmc.LOGINFO)
    
    re_1 = r':\[\{([^\}]+)'
    re_p = re.search(re_1, match)
    if re_p:
        re_p = re_p.group(1)
        #xbmc.log("LA CAPTURA EN BRUTO ES " + str(re_p), xbmc.LOGINFO)    
    re_2 = r"',36[^|]*([^']+)"
    re_k = re.search(re_2, match)
    if re_k:
        re_k = re_k.group(1)
        #xbmc.log("LA CAPTURA EN BRUTO ES " + str(re_k), xbmc.LOGINFO)
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
    url_con = url_sin + "|User-Agent=Mozilla/5.0(iPhone;CPUiPhoneOS14_7likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Version/14.0Mobile/15E148Safari/604.1"
    xbmc.log("URL FINAL ES :  " + url_con, xbmc.LOGINFO)
    return url_con
    #xbmcgui.Dialog().ok("auto_desofuscar", url_final)
    
def desofuscar(url):
    regex = r"<script type='text/javascript'>(.*?)</script>"
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    match = re.search(regex, html_content, re.DOTALL).group(1)
    
    if match:
        xbmc.log("LA CAPTURA EN BRUTO ES " + str(match), xbmc.LOGINFO)
        
        re_1 = r'cdn\|([^\|]+)'
        match1 = re.search(re_1, match).group(1)
        if match1 == "setCurrentAudioTrack" or match1 == "jpg":
            re_1 = r'master\|+[^|]*\|+[^|]*\|+([^|]+)'
            match1 = re.search(re_1, match).group(1)
            
        re_2 = r'\|01\|([^\|]+)'
        match2 = re.search(re_2, match).group(1)
        if match2 == "jupiter":
            re_2 = r'master\|[^|]*\|([^|]+)'
            match2 = re.search(re_2, match).group(1)

        re_3 = r'master\|[^|]*\|([^|]+)'
        match3 = re.search(re_3, match).group(1)
        if match3 == "hls2":
            re_3 = r'\|kind\|([^\|]+)'
            match3 = re.search(re_3, match).group(1)
            if "vtt" in match3:
                re_3 = r'\|vtt\|([^\|]+)'
                match3 = re.search(re_3, match).group(1)  

        re_4 = r'master\|([^\|]+)'
        match4 = re.search(re_4, match).group(1)       
        
        re_5 = r'129600\|(.{43})'
        match5 = re.search(re_5, match).group(1)
        if match5.endswith("|m"):
                xbmcgui.Dialog().ok("Me he distraido", "Perdóname, te va a dar error, intentalo de nuevo y prestaré más atención")
                match5 = match5[:-2]
                xbmc.log("Estoy dentro de match5............................: " + str(match5), xbmc.LOGINFO)
        caracter = "|"
        cantidad = match5.count(caracter)
        #xbmcgui.Dialog().ok("Estoy dentro de match5", str(cantidad))
        if cantidad == 1:
            pattern = r"([^|]+)\|([^|]+)"
            reversed_text = re.sub(pattern, r"\2|\1", match5)            
            match5_bis = reversed_text.replace("|", "-")
            xbmc.log("Estoy dentro de match5............................: " + str(match5) + "  " + str(match5_bis), xbmc.LOGINFO)
            match5 = match5_bis
            #xbmcgui.Dialog().ok("Estoy dentro de match5", str(match5))
        if cantidad == 2: 
            pattern = r"([^|]+)\|([^|]+)\|([^|]+)"
            reversed_text = re.sub(pattern, r"\3|\2|\1", match5)
            match5_bis = reversed_text.replace("|", "-")
            xbmc.log("Estoy dentro de match5............................: " + str(match5) + "  " + str(match5_bis), xbmc.LOGINFO)
            match5 = match5_bis
            
        re_6 = r'get\|+data\|+([^\|]+)'
        match6 = re.search(re_6, match)
        if match6:
            match6 = match6.group(1)
        else: 
            #xbmcgui.Dialog().ok("Estoy dentro de match2", "segundo intento")
            re_6b = r'get\|+([^\|]+)'
            match6 = re.search(re_6b, match)
            if match6:
                match6 = match6.group(1)
            else:
                match6 = None   
        
        re_7 = r'get\|+data\|+[^|]*\|+(\d+)'
        match7 = re.search(re_7, match)
        if match7:
            match7 = match7.group(1)
        else: 
            #xbmcgui.Dialog().ok("Estoy dentro de match3", "segundo intento")
            re_7b = r'get\|+[^|]*\|+(\d+)'
            match7 = re.search(re_7b, match)
            if match7:
                match7 = match7.group(1)
            else:
                match7 = None
        
        re_8 = r'\|100\|([^\|]+)'
        match8 = re.search(re_8, match).group(1)
        if match8 == "kind" or match8 == "setCurrentAudioTrack":
            re_8 = r'\|file\|([^\|]+)'
            match8 = re.search(re_8, match).group(1)
            
        if "wish" in url:        
            re_9 = r'image\|([^\|]+)'
            match9 = re.search(re_9, match).group(1)
        if "vidhide" in url:
            re_9 = r'text\|([^\|]+)'
            match9 = re.search(re_9, match).group(1)
        #xbmcgui.Dialog().ok("Estoy dentro de match5", str(match7))
        
       
        
        if "wish" in url:
            url_final = f"https://{match1}.cdn-jupiter.com/{match2}/01/{match3}/{match4}/master.m3u8?t={match5}&s={match6}&e=129600&f={match7}&srv={match8}&i=0.4&sp=500&p1={match8}&p2={match8}&asn={match9}" + "|User-Agent=Mozilla/5.0(iPhone;CPUiPhoneOS14_7likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Version/14.0Mobile/15E148Safari/604.1"
        if "vidhide" in url:
            url_final = f"https://{match1}.hgagecdn.com/{match2}/01/{match3}/{match4}/master.m3u8?t={match5}&s={match6}&e=129600&f={match7}&srv={match8}&i=0.4&sp=500&p1={match8}&p2={match8}&asn={match9}" + "|User-Agent=Mozilla/5.0(iPhone;CPUiPhoneOS14_7likeMacOSX)AppleWebKit/605.1.15(KHTML,likeGecko)Version/14.0Mobile/15E148Safari/604.1"
            
        xbmc.log("LA CAPTURA ES " + " M1=" + str(match1) + " M2=" + str(match2) + " M3=" + str(match3) + " M4=" + str(match4) + " M5=" + str(match5) + " M6=" + str(match6) + " M7=" + str(match7) + " M8=" + str(match8) + " M9=" + str(match9), xbmc.LOGINFO)
        xbmc.log("LA URL FINAL ES: " + str(url_final), xbmc.LOGINFO)
        return url_final
        #xbmcgui.Dialog().ok("Estoy dentro de desofuscar", "Perfecto")
def filemon(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text 
    xbmc.log("URL es...: " + str(html_content), xbmc.LOGINFO)
    xbmcgui.Dialog().ok("Estoy dentro de varios_link", str(html_content))
    regex = '(?s)a href="([^"]+)'
    match = re.search(regex, html_content)
    url_final = match.group(1)
    xbmc.log("URL es...: " + str(url_final), xbmc.LOGINFO)
    xbmcgui.Dialog().ok("Estoy dentro de varios_link", str(url_final))
def obtener_nombre_servidor(url):
    parsed_url = urlparse(url)
    servidor_completo = parsed_url.netloc
    nombre_servidor = servidor_completo.split(".")[0]  # Obtiene solo la parte antes del primer punto
    if "www" in nombre_servidor or "plugin" in nombre_servidor:
       nombre_servidor = "                                   [COLOR forestgreen][B]Tráiler de la película[/COLOR][/B]" 
    return nombre_servidor 
def varios_link(url, titulo):
    #convierte la captura en lista 
    urls = url.split(", ")
    
    nombres_servidor = [obtener_nombre_servidor(url) for url in urls]
    # Mostrar el cuadro de opciones
    dialog = xbmcgui.Dialog()
    indice = dialog.select("[COLOR blue] " +titulo + "                                                         [/COLOR]", nombres_servidor)
    if indice == -1:
        sys.exit()        
    if indice != -1:
        if "plugin" in urls[indice]:
            #xbmc.log("URL es...: " + str(urls[indice]), xbmc.LOGINFO)
            #xbmcgui.Dialog().ok("Estoy dentro de varios_link", str(urls[indice]))
            import petra
            petra.cajon(urls[indice], "", "1")            
        #xbmc.log("URL es...: " + str(urls[indice]), xbmc.LOGINFO)
        #xbmcgui.Dialog().ok("Estoy dentro de varios_link", str(urls[indice]))
        if any(substring in urls[indice] for substring in ["videzz", "vidoza", "asnwish", "gamovideo"]):
            import petra
            petra.cajon("", urls[indice], "1")
            
        return urls[indice]  # Devolver la URL asociada al clic del usuario
    else:
        return None
    #xbmc.log("URL es...: " + str(url), xbmc.LOGINFO)
    #xbmcgui.Dialog().ok("Estoy dentro de varios_link", str(url))
    
def resolver (url, regex):
    #funciona para GAMOVIDEO y SENDVID
    #xbmc.log("URL es...: " + url, xbmc.LOGINFO)
    #xbmcgui.Dialog().ok("Estoy dentro de m3u", url) 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    if "gamovideo" in url:
        match = re.search(regex, html_content)
        url_final = match.group(1)
    elif "videzz.net" in url or "vidoza.net" in url:
        regex = 'src: "([^"]+)'
        match = re.search(regex, html_content)
        url_final = match.group(1)
    else: 
        regex = '(?s)og:video. content="([^"]+)'
        #xbmcgui.Dialog().ok("Estoy dentro de sendvid", html_content)
        match = re.search(regex, html_content)
        url_final = match.group(1)     
    return url_final    
    
def resolver_Streamwish(url):
    regex = '(?s): \[{file:"([^"]+)'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    match = re.search(regex, html_content)
    url_final = match.group(1)
    return url_final

    
def resolver_Streamvid (url, regex1, regex2):     
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    
    match = re.search(f"{regex1}.*?{regex2}", html_content)
    if match:
        cacho1 = match.group(1)
        cacho2 = match.group(2)
        url_final = f"https://{cacho1}.flyeyes.pics/hls/,{cacho2},.urlset/master.m3u8" 
    else:    
        regex1 = "(?s)\|media\|\|([^\|]+)"
        match = re.search(f"{regex1}.*?{regex2}", html_content)
        if match:
            cacho1 = match.group(1)
            cacho2 = match.group(2)
            url_final = f"https://{cacho1}.streamvid.media/hls/,{cacho2},.urlset/master.m3u8"
        else:
            regex1 = "(?s)\|false\|([^\|]+)"
            match = re.search(f"{regex1}.*?{regex2}", html_content)
            cacho1 = match.group(1)
            cacho2 = match.group(2)
            url_final = f"https://{cacho1}.streamvid.net/hls/,{cacho2},.urlset/master.m3u8"
        
    
    #xbmc.log("URL es...: " + url_final, xbmc.LOGINFO)
    #xbmcgui.Dialog().ok("Estoy dentro de m3u", url_final)                  
    return url_final  
    
def resolver_Vtube (url, regex1, regex2): 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    html_content = response.text
    #xbmc.log("URL es...: " + html_content, xbmc.LOGINFO)
    #xbmcgui.Dialog().ok("Estoy dentro de m3u", html_content)
    
    match = re.search(f"{regex1}.*?{regex2}", html_content)
    cacho2 = match.group(1)    
    cacho1 = match.group(2)    
    url_final = f"https://{cacho1}.vtube.network/hls/,{cacho2},.urlset/master.m3u8"  
    #xbmcgui.Dialog().ok("Estoy dentro de m3u", url_final)
    return url_final
    
