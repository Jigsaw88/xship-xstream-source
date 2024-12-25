
import os
import xbmcaddon
from xbmcvfs import translatePath
from resources.lib.utils import kill

# siehe Zeile 51
addonInfo = xbmcaddon.Addon().getAddonInfo
addonId = addonInfo('id')
addonVersion = addonInfo('version')

def starter2():
    root_path = translatePath(os.path.join('special://home/addons/', '%s'))
    addon_data_path = translatePath(os.path.join('special://home/userdata/addon_data/', '%s'))
    userdata_path = translatePath(os.path.join('special://home/userdata/', '%s'))

    pass