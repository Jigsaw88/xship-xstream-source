
import os
import xbmcaddon
from xbmcvfs import translatePath
from resources.lib.utils import kill

# siehe Zeile 51
addonInfo = xbmcaddon.Addon().getAddonInfo
addonId = addonInfo('id')
addonVersion = addonInfo('version')

def starter2():
    pass