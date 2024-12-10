import os
import sys
import xbmc
import shutil
import xbmcgui
import xbmcaddon
from xbmcvfs import translatePath as TRANSLATEPATH
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

origen_xonfluence = TRANSLATEPATH('special://home/addons/plugin.video.play/resources/lib/skin.xonfluence')
origen_play = TRANSLATEPATH('special://home/addons/plugin.video.play/resources/lib/plugin.video.play')
origen_embuary = TRANSLATEPATH('special://home/addons/plugin.video.play/resources/lib/script.embuary.info')
origen_sources = TRANSLATEPATH('special://home/addons/plugin.video.play/resources/lib/sources.xml')
origen_advancedsettings = TRANSLATEPATH('special://home/addons/plugin.video.play/resources/lib/advancedsettings.xml')

addon_data_folder = TRANSLATEPATH('special://profile/addon_data/')

destino_xonfluence = os.path.join(addon_data_folder, 'skin.xonfluence')
destino_play = os.path.join(addon_data_folder, 'plugin.video.play')
destino_embuary = os.path.join(addon_data_folder, 'script.embuary.info')
destino_sources = TRANSLATEPATH('special://userdata/sources.xml')
destino_advancedsettings = TRANSLATEPATH('special://userdata/advancedsettings.xml')

def copiar_carpeta(origen, destino):
    if os.path.isdir(origen):
        # La carpeta existe en la segunda ubicación, copia y pega en la primera ubicación
        shutil.copytree(origen, destino)
    elif os.path.isfile(origen):
            # Si es un archivo, copia el archivo
        shutil.copy2(origen, destino)    
    else:
        # La carpeta no existe en ninguna de las ubicaciones, muestra un cuadro de diálogo OK
        xbmcgui.Dialog().ok("Resultado", "La carpeta skin.xonfluence no existe en ninguna de las ubicaciones.")
        
copiar_carpeta(origen_xonfluence, destino_xonfluence)
copiar_carpeta(origen_play, destino_play)
copiar_carpeta(origen_embuary, destino_embuary)
copiar_carpeta(origen_sources, destino_sources)
copiar_carpeta(origen_advancedsettings, destino_advancedsettings)
    
paso_update = 0    
def comprobar_repo(repourl, repoid):#con esto busca la actualizacion del repo
    def get_installed_version(addon_id):
        
        try:
            addon = xbmcaddon.Addon(addon_id)
            retorno = addon.getAddonInfo('version')
            if retorno:                        
                return retorno 
        
        except RuntimeError:
## por fin funciona ya que si no existe lo instala desde tu repo 
            xbmc.executebuiltin(f'InstallAddon({addon_id})')
###una vez instalado a ver si funciona este xbmc.executebuiltin(f'UpdateAddon({addon_id})')                    
            return None
        
    def get_latest_version():
        url = repourl
        response = urllib.request.urlopen(url)
        root = ET.fromstring(response.read())
        for addon in root.findall('addon'):
            if addon.get('id') == repoid:  
                return addon.get('version')
        return None
    def check_for_update(repoid):
        
        global paso_update
        
        installed_version = get_installed_version(repoid)
        
        latest_version = get_latest_version()
        
        dialog = xbmcgui.Dialog()
        
        if latest_version is None or installed_version is None:
            pass
        #elif installed_version == latest_version:
            #dialog.ok("Versión instalada: {}".format(installed_version), "version en el repo: {}".format(latest_version))                        
        elif installed_version < latest_version:
                                  
            if "Macke" in repoid:
                dialog.ok(f"La nueva versión del repo es: {latest_version}", "Kodi se cerrará automáticamente para actualizarlo")
                paso_update = 1
                #xbmc.executebuiltin(f'UpdateAddon({repoid})')
                #dialog.ok("Kodi ", "Actualizar el repo a esta versión más reciente: {}".format(latest_version))
                
      #         URL de descarga de la actualización
                update_url = "https://raw.githubusercontent.com/Espinete/Mackenzie/master/repository.Mackenzie/repository.Mackenzie-{}.zip".format(latest_version)  
      #         Ruta donde se guardará el archivo de actualización
                update_path = TRANSLATEPATH("special://home/addons")                       
      #         Obtener la ruta del addon actual
                update_file = os.path.join(update_path, "update.zip")
      #         Descargar el archivo de actualización
                urllib.request.urlretrieve(update_url, update_file)                       
      #         Extraer el archivo de actualización
                with zipfile.ZipFile(update_file, 'r') as zip_ref:
                    zip_ref.extractall(update_path)                            
      #         Eliminar el archivo de actualización descargado y cerrar kodi
                os.remove(update_file)
                
                #xbmc.executebuiltin('InstallAddon(repository.Mackenzie)')
        return        
    # ID del addon del repositorio que deseas comprobar
    #repo_addon_id = repoid
    # Llama a la función check_for_update() con el ID del addon del repositorio
    check_for_update(repoid)
    return
        
comprobar_repo("https://raw.githubusercontent.com/Espinete/Mackenzie/master/addons.xml", "repository.Mackenzie")
if paso_update == 1:
    xbmc.executebuiltin('RestartApp')    
#xbmcgui.Dialog().ok("Resultado", "Acabo de copiar todo con exito, Kodi se cerrará automáticamente")
#xbmc.executebuiltin('RestartApp')
#xbmc.executebuiltin('Action(ParentDir)')



    
    
    






