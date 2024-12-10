import xbmc
import xbmcgui
import time
import os
kodi_version = xbmc.getInfoLabel('System.BuildVersion')
if kodi_version.startswith('19'):
    from xbmc import translatePath as variacion_translatePath
elif int(kodi_version.split('.')[0]) >= 20:
    from xbmcvfs import translatePath as variacion_translatePath
else:
    raise RuntimeError("Versión de Kodi no compatible")
ruta_especial = variacion_translatePath('special://home/addons/plugin.video.play/resources/lib/contador.txt')
def topuria (url):
    def cargar_contador():
        if os.path.exists(ruta_especial):
            with open(ruta_especial, "r") as f:
                return int(f.read())
        else:
            return 1

    def guardar_contador(a):
        with open(ruta_especial, "w") as f:
            f.write(str(a))     
    topuria.a = cargar_contador()    
    if topuria.a == 1:
        mp3 = "special://home/addons/plugin.video.play/resources/lib/topuria.mp3"
        xbmc.Player().play(mp3)
        time.sleep(8)        
        
    url = "https://dl.dropbox.com/s/7cvtsxlyfcog69t/topuria.html"
    topuria.a += 1
    guardar_contador(topuria.a)
    #xbmcgui.Dialog().ok("contador", str(topuria.a))
    return url