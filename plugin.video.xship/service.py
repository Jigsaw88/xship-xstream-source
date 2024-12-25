# -*- coding: utf-8 -*-

# 2022-10-09
# edit 2024-12-17

import sys
from xbmcaddon import Addon
from resources.lib.requestHandler import cRequestHandler

is_python2 = sys.version_info.major == 2
if is_python2:
    from xbmc import translatePath
    from urlparse import urlparse
else:
    from xbmcvfs import translatePath
    from urllib.parse import urlparse

addonInfo = Addon().getAddonInfo
addonPath = translatePath(addonInfo('path'))
addonVersion = addonInfo('version')
setSetting = Addon().setSetting
_getSetting = Addon().getSetting

def getSetting(Name, default=''):
    result = _getSetting(Name)
    if result: return result
    else: return default

# Html Cache beim KodiStart loeschen
def delHtmlCache():
    from time import time
    deltaDay = int(getSetting('cacheDeltaDay', 2))
    deltaTime = 60*60*24*deltaDay # Tage
    currentTime = int(time())
    # einmalig
    if getSetting('delHtmlCache') == 'true':
        cRequestHandler('').clearCache()
        setSetting('lastdelhtml', str(currentTime))
        setSetting('delHtmlCache', 'false')
    # alle x Tage
    elif currentTime >= int(getSetting('lastdelhtml', 0)) + deltaTime:
        cRequestHandler('').clearCache()
        setSetting('lastdelhtml', str(currentTime))

# Scraper(Seiten) ein- / ausschalten
#  [(providername, domainname), ...]     providername identisch mit dateiname
def _getPluginData():
    from os import path, listdir
    sPluginFolder = path.join(addonPath, 'scrapers', 'scrapers_source', 'de')
    sys.path.append(sPluginFolder)
    items = listdir(sPluginFolder)
    aFileNames=[]
    aPluginsData = []
    for sItemName in items:
        if sItemName.endswith('.py'): aFileNames.append(sItemName[:-3])
    for fileName in aFileNames:
        if fileName ==  '__init__': continue
        try:
            plugin = __import__(fileName, globals(), locals())
            print(plugin.SITE_DOMAIN +'  '+ plugin.SITE_IDENTIFIER)
            aPluginsData.append({'domain': plugin.SITE_DOMAIN, 'provider': plugin.SITE_IDENTIFIER})
        except:
            pass
    return aPluginsData

def check_domains():
    domains = _getPluginData()
    for item in domains:
        _domain = item['domain']
        _provider = item['provider']
        if _provider == 'vavoo':
            setSetting('provider.' + _provider + '.check', 'true')
            continue
        domain = getSetting('provider.'+ _provider +'.domain', _domain)
        base_link = 'https://' + domain
        try:
            oRequest = cRequestHandler(base_link, caching=False)
            oRequest.request()
            status_code = int(oRequest.getStatus())
            #print(str(status_code) + '  ' + _provider)
            if 300 <= status_code <= 400:
                url = oRequest.getRealUrl()
                #setSetting('provider.'+ _provider +'.base_link', url)
                setSetting('provider.' + _provider + '.domain', urlparse(url).hostname)
                setSetting('provider.' + _provider + '.check', 'true')
            elif status_code == 200:
                #setSetting('provider.' + provider + '.base_link', base_link)
                setSetting('provider.' + _provider + '.domain', urlparse(base_link).hostname)
                setSetting('provider.' + _provider + '.check', 'true')
            else:
                setSetting('provider.' + _provider + '.check', 'false')
                setSetting('provider.' + _provider + '.domain', domain)
        except:
            setSetting('provider.' + _provider + '.check', 'false')
            setSetting('provider.' + _provider + '.domain', domain)
            pass

# Download Helper File  - code neutral für xship und xstream (py3)
def download_help():
    from os import path
    from time import time
    from resources.lib.utils import download_url, unzip
    from xbmcvfs import translatePath, delete
    from xbmcaddon import Addon

    addonInfo = Addon().getAddonInfo
    getSetting = Addon().getSetting
    setSetting = Addon().setSetting
    addonPath = translatePath(addonInfo('path'))  # 'C:\\Program Files\\Kodi21\\portable_data\\addons\\plugin.video.xship\\'

    diffTime = 60*60*8 # 8 Stunden
    currentTime = int(time())
    url = 'https://raw.githubusercontent.com/xsupdater/xsupdater/backup/logo_aktuell.jpg'
    contr = translatePath(path.join(addonPath, 'resources', 'lib', 'help.py'))
    dest = translatePath(path.join(addonPath, 'resources', 'lib'))
    src = translatePath(path.join('special://temp', url.split('/')[-1]))

    # Schutz vor Manipulation "setting.xml"
    try:
        if getSetting('hosts.refresh') == '': setSetting('status.refresh', '')
        elif getSetting('status.refresh') == '': setSetting('hosts.refresh', '')
        elif getSetting('status.refresh') !=  getSetting('hosts.refresh')[::-1]:
            setSetting('status.refresh', '')
    except:
        setSetting('status.refresh', '')

    if not path.exists(contr) or getSetting('status.refresh')=='' or int(getSetting('status.refresh')) <= currentTime - diffTime:
        try:
            delete(contr)
            download_url(url, src, dp=False) # dp - progressDialog nicht anzeigen
            unzip(src, dest, folder=None)
            delete(src)
            setSetting('hosts.refresh', str(currentTime)[::-1])
            setSetting('status.refresh', str(currentTime))
        except:
            from xbmcgui import Dialog
            from xbmc import executebuiltin
            Dialog().ok('ERROR', '[COLOR red] Problem mit der Internet Verbindung ? [/COLOR]')
            executebuiltin("Dialog.Close(all)")
            executebuiltin("ActivateWindow(Home)")


# kasi - Code für Zwangsupdate
def checkVersion():
    import requests, re
    from xbmcaddon import Addon
    addonInfo = Addon().getAddonInfo
    addonId = addonInfo('id')
    addonVersion = addonInfo('version')
    addonPath = translatePath('special://home/addons/%s') % addonId
    url = 'https://raw.githubusercontent.com/watchone/watchone.github.io/refs/heads/repo/plugin.video.xship/addon.xml'
    r = requests.get(url)
    if r.status_code != 200 : return
    remoteVersion = re.findall('version="([^"]+)', str(r.content))[1]
    if addonVersion == remoteVersion: return

    from os import path
    from xbmcvfs import delete
    from resources.lib.utils import download_url, unzip, remove_dir
    zipfile = 'plugin.video.xship-%s.zip' % remoteVersion
    url = 'https://github.com/watchone/watchone.github.io/raw/refs/heads/repo/plugin.video.xship/%s' % zipfile
    src = translatePath(path.join('special://temp', url.split('/')[-1]))
    dest = translatePath('special://home/addons')
    download_url(url, src, dp=True)  # dp - progressDialog nicht anzeigen
    remove_dir(addonPath)
    unzip(src, dest, folder=None)
    delete(src)
    from xbmc import executebuiltin, getInfoLabel
    # executebuiltin("UpdateLocalAddons()") # kasi - ist das nötig?
    profil = getInfoLabel('System.ProfileName')
    if profil:  executebuiltin('LoadProfile(' + profil + ',prompt)')


def main():
    # temp. resolveurl  patch __init__.py - priority
    from resources.lib.utils import patchResolver
    patchResolver()

    import xbmc
    if not xbmc.getCondVisibility("System.HasAddon(inputstream.adaptive)"):
        xbmc.executebuiltin('InstallAddon(inputstream.adaptive)')
        xbmc.executebuiltin('SendClick(11)')

    checkVersion()
    download_help()

    from os import path
    contr = translatePath(path.join(addonPath, 'resources', 'lib', 'help.py'))
    if path.exists(contr):
        # ab hier die restlichen Aufrufe
        check_domains()
        delHtmlCache()

if __name__ == "__main__":
    main()

    # try:
    #     import pydevd
    #     if pydevd.connected: pydevd.kill_all_pydev_threads()
    # except:
    #     pass
    # finally:
    #     exit()
