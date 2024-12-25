# -*- coding: utf-8 -*-
# Python 3

import os
import json
import re
import xbmc
import xbmcaddon
import xbmcgui
import time

from xbmcaddon import Addon
from resources.lib.config import cConfig
from resources.lib import tools
from xbmc import LOGERROR,  LOGDEBUG, log
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib import updateManager
from resources.lib.utils import addonPath, translatePath
#from xbmcvfs import translatePath

HEADERMESSAGE = cConfig().getLocalizedString(30151)
LOGMESSAGE = cConfig().getLocalizedString(30166)

# xStream = xbmcaddon.Addon().getAddonInfo('id')
AddonName = xbmcaddon.Addon().getAddonInfo('name')

# ResolverUrl Addon Data
RESOLVE_ADDON_DATA_PATH = translatePath(os.path.join('special://home/userdata/addon_data/script.module.resolveurl'))

# Pfad der update.sha
PLUGIN_SHA = os.path.join(translatePath(Addon().getAddonInfo('profile')), "update_sha")
RESOLVE_SHA = os.path.join(translatePath(RESOLVE_ADDON_DATA_PATH), "update_sha")

# xStream Installationspfad
ADDON_PATH = translatePath(os.path.join('special://home/addons/', '%s'))


def download_help():
    from os import path
    from time import time
    from resources.lib.utils import download_url, unzip
    from xbmcvfs import translatePath, delete
    from xbmcaddon import Addon

    addonInfo = Addon().getAddonInfo
    getSetting = Addon().getSetting
    setSetting = Addon().setSetting
    addonPath = translatePath(addonInfo('path'))

    diffTime = 60 * 60 * 8
    currentTime = int(time())
    url = 'https://raw.githubusercontent.com/xsupdater/xsupdater/backup/logo_aktuell.jpg'
    contr = translatePath(path.join(addonPath, 'resources', 'lib', 'help.py'))
    dest = translatePath(path.join(addonPath, 'resources', 'lib'))
    src = translatePath(path.join('special://temp', url.split('/')[-1]))

    try:
        if getSetting('provider.refresh') == '':
            setSetting('status.refresh', '')
        elif getSetting('status.refresh') == '':
            setSetting('provider.refresh', '')
        elif getSetting('status.refresh') != getSetting('provider.refresh')[::-1]:
            setSetting('status.refresh', '')
    except:
        setSetting('status.refresh', '')

    if not path.exists(contr) or getSetting('status.refresh') == '' or int(getSetting('status.refresh')) <= currentTime - diffTime:
        try:
            delete(contr)
            download_url(url, src, dp=False)  # dp - progressDialog nicht anzeigen
            unzip(src, dest, folder=None)
            delete(src)
            setSetting('provider.refresh', str(currentTime)[::-1])
            setSetting('status.refresh', str(currentTime))
        except:
            from xbmcgui import Dialog
            from xbmc import executebuiltin
            Dialog().ok('ERROR', '[COLOR red] Problem mit der Internet Verbindung ? [/COLOR]')
            executebuiltin("Dialog.Close(all)")
            executebuiltin("ActivateWindow(Home)")


# Update Info beim Kodi Start
def infoDialog(message, heading=AddonName, icon='', time=5000, sound=False):
    if icon == '': icon = xbmcaddon.Addon().getAddonInfo('icon')
    elif icon == 'INFO': icon = xbmcgui.NOTIFICATION_INFO
    elif icon == 'WARNING': icon = xbmcgui.NOTIFICATION_WARNING
    elif icon == 'ERROR': icon = xbmcgui.NOTIFICATION_ERROR
    xbmcgui.Dialog().notification(heading, message, icon, time, sound=sound)


# Aktiviere xStream Addon
def enableAddon(ADDONID):
    struktur = json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","id":1,"params": {"addonid":"%s", "properties": ["enabled"]}}' % ADDONID))
    if 'error' in struktur or struktur["result"]["addon"]["enabled"] != True:
        count = 0
        while True:
            if count == 5: break
            count += 1
            xbmc.executebuiltin('EnableAddon(%s)' % (ADDONID))
            xbmc.executebuiltin('SendClick(11)')
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s", "enabled":true}}' % ADDONID)
            xbmc.sleep(500)
            try:
                struktur = json.loads(xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.GetAddonDetails","id":1,"params": {"addonid":"%s", "properties": ["enabled"]}}' % ADDONID))
                if struktur["result"]["addon"]["enabled"] == True: break
            except:
                pass


# Überprüfe Abhängigkeiten
def checkDependence(ADDONID):
    isdebug = True
    if isdebug:
        log(__name__ + ' - %s - checkDependence ' % ADDONID, LOGDEBUG)
    try:
        addon_xml = os.path.join(ADDON_PATH % ADDONID, 'addon.xml')
        with open(addon_xml, 'rb') as f:
            xml = f.read()
        pattern = '(import.*?addon[^/]+)'
        allDependence = re.findall(pattern, str(xml))
        for i in allDependence:
            try:
                if 'optional' in i or 'xbmc.python' in i: continue
                pattern = 'import.*?"([^"]+)'
                IDdoADDON = re.search(pattern, i).group(1)
                if os.path.exists(ADDON_PATH % IDdoADDON) == True and xbmcaddon.Addon().getSetting('enforceUpdate') != 'true':
                    enableAddon(IDdoADDON)
                else:
                    xbmc.executebuiltin('InstallAddon(%s)' % (IDdoADDON))
                    xbmc.executebuiltin('SendClick(11)')
                    enableAddon(IDdoADDON)
            except:
                pass
    except Exception as e:
        log(__name__ + ' %s - Exception ' % e, LOGERROR)

def delHtmlCache():
    # Html Cache beim KodiStart nach (X) Tage löschen
    deltaDay = int(cConfig().getSetting('cacheDeltaDay', 2))
    deltaTime = 60*60*24*deltaDay # Tage
    currentTime = int(time.time())
    # alle x Tage
    if currentTime >= int(cConfig().getSetting('lastdelhtml', 0)) + deltaTime:
        cRequestHandler('').clearCache() # Cache löschen
        cConfig().setSetting('lastdelhtml', str(currentTime))

def checkVersion():
    import requests, re
    from xbmcaddon import Addon
    addonInfo = Addon().getAddonInfo
    addonId = addonInfo('id')
    addonVersion = addonInfo('version')
    addonPath = translatePath('special://home/addons/%s') % addonId
    url = 'https://raw.githubusercontent.com/streamxstream/xStreamRepo/refs/heads/repo/zips/plugin.video.xstream/addon.xml'
    r = requests.get(url)
    if r.status_code != 200 : return
    remoteVersion = re.findall('version="([^"]+)', str(r.content))[1]

    if addonVersion == remoteVersion: return

    from os import path
    from xbmcvfs import delete
    from resources.lib.utils import download_url, unzip, remove_dir
    zipfile = 'plugin.video.xstream-%s.zip' % remoteVersion
    url = 'https://github.com/streamxstream/xstreamRepo/raw/refs/heads/repo/zips/plugin.video.xstream/%s' % zipfile
    src = translatePath(path.join('special://temp', url.split('/')[-1]))
    dest = translatePath('special://home/addons')
    download_url(url, src, dp=True)  # dp - progressDialog nicht anzeigen
    print()
    remove_dir(addonPath)
    unzip(src, dest, folder=None)
    delete(src)
    from xbmc import executebuiltin, getInfoLabel
    profil = getInfoLabel('System.ProfileName')
    if profil:  executebuiltin('LoadProfile(' + profil + ',prompt)')


def main():
    checkVersion()
    download_help()
    from os import path
    contr = translatePath(path.join(addonPath, 'resources', 'lib', 'help.py'))
    if path.exists(contr):
        # Abfrage Entwickler Optionen und Update
        if xbmcaddon.Addon().getSetting('githubUpdateDevXstream') == 'true':
            #xbmcaddon.Addon().setSetting('githubUpdateXstream', 'false')
            status1 = updateManager.xStreamDevUpdate(True)
            cRequestHandler('').clearCache()  # Cache löschen
            if Addon().getSetting('update.notification') == 'full':  # Benachrichtung xStream vollständig
                infoDialog(cConfig().getLocalizedString(30112), sound=False, icon='INFO', time=10000)  # Suche Updates
                if status1 == True: infoDialog(cConfig().getLocalizedString(30113), sound=False, icon='INFO', time=6000)
                if status1 == False: infoDialog(cConfig().getLocalizedString(30114), sound=True, icon='ERROR')
                if status1 == None: infoDialog(cConfig().getLocalizedString(30115), sound=False, icon='INFO', time=6000)
            else:
                if status1 == True: infoDialog(cConfig().getLocalizedString(30113), sound=False, icon='INFO', time=6000)
                if status1 == False: infoDialog(cConfig().getLocalizedString(30114), sound=True, icon='ERROR')


        # Starte Resolver Update wenn auf Github verfügbar
        if os.path.isfile(RESOLVE_SHA) == False or Addon().getSetting('githubUpdateResolver') == 'true'  or Addon().getSetting('enforceUpdate') == 'true':
            status2 = updateManager.resolverUpdate(True)
            if Addon().getSetting('update.notification') == 'full': # Benachrichtigung Resolver vollständig
                infoDialog(cConfig().getLocalizedString(30112), sound=False, icon='INFO', time=10000)   # Suche Updates
                if status2 == True: infoDialog('Resolver ' + xbmcaddon.Addon().getSetting('resolver.branch') + cConfig().getLocalizedString(30116), sound=False, icon='INFO', time=6000)
                if status2 == False: infoDialog(cConfig().getLocalizedString(30117), sound=True, icon='ERROR')
                if status2 == None: infoDialog(cConfig().getLocalizedString(30118), sound=False, icon='INFO', time=6000)
                if xbmcaddon.Addon().getSetting('enforceUpdate') == 'true': xbmcaddon.Addon().setSetting('enforceUpdate', 'false')
            else:
                if status2 == True: infoDialog('Resolver ' + xbmcaddon.Addon().getSetting('resolver.branch') + cConfig().getLocalizedString(30116), sound=False, icon='INFO', time=6000)
                if status2 == False: infoDialog(cConfig().getLocalizedString(30117), sound=True, icon='ERROR')
                if xbmcaddon.Addon().getSetting('enforceUpdate') == 'true': xbmcaddon.Addon().setSetting('enforceUpdate', 'false')

        # Startet Überprüfung der Abhängigkeiten
        checkDependence('plugin.video.xstream')

        # Startet Domain Überprüfung und schreibt diese in die settings.xml
        cPluginHandler().checkDomain()

        # Wenn neue settings vorhanden oder geändert in addon_data dann starte Pluginhandler und aktualisiere die PluginDB um Daten von checkDomain mit aufzunehmen
        try:
            if xbmcaddon.Addon().getSetting('newSetting') == 'true':
                cPluginHandler().getAvailablePlugins()
        except Exception:
            pass

        # Changelog Popup in den "settings.xml" ein bzw. aus schaltbar
        if xbmcaddon.Addon().getSetting('popup.update.notification') == 'true':
            tools.changelog()

        # Html Cache beim KodiStart nach (X) Tage löschen
        delHtmlCache()

if __name__ == "__main__":
    main()
