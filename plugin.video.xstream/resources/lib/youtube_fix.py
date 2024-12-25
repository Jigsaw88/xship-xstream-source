# -*- coding: utf-8 -*-
# Python 3

import os
import xbmcaddon, xbmcgui, xbmcvfs
from xbmcvfs import translatePath
from urllib.request import urlretrieve
from urllib.parse import quote_plus

Addon = xbmcaddon.Addon()
addonInfo = xbmcaddon.Addon().getAddonInfo
addonID = addonInfo('id')
addonName = addonInfo('name')
addon = xbmcaddon.Addon(addonID)
addonPath = translatePath(addon.getAddonInfo('path'))
profilePath = translatePath(addon.getAddonInfo('profile'))
progressDialog = xbmcgui.DialogProgress()


def download_url(url, dest, dp=None):
    # download_url(url, src, dp=[None / True / False / Dialog])
    if dp == None or dp == True:
        dp = progressDialog
        dp.create("URL Downloader", " \n  Downloading  File:  [B]%s[/B]" % url.split('/')[-1])
    elif dp == False:
        return urlretrieve(url, dest)
    try:
        dp.update(0)
        urlretrieve(url, dest, lambda nb, bs, fs, url=url: _pbhook(nb, bs, fs, dp))
        dp.close()
    except:
        urlretrieve(url, dest)

def _pbhook(numblocks, blocksize, filesize, dp):
    try:
        percent = min((numblocks * blocksize * 100) / filesize, 100)
        dp.update(int(percent))
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        dp.close()
        raise Exception("Canceled")


def unzip_recursive(path, dirs, dest):
    for directory in dirs:
        dirs_dir = os.path.join(path, directory)
        dest_dir = os.path.join(dest, directory)
        xbmcvfs.mkdir(dest_dir)
        dirs2, files = xbmcvfs.listdir(dirs_dir)
        if dirs2:
            unzip_recursive(dirs_dir, dirs2, dest_dir)
        for file in files:
            # unzip_file(os.path.join(dirs_dir, file.decode('utf-8')), os.path.join(dest_dir, file.decode('utf-8')))
            unzip_file(os.path.join(dirs_dir, file), os.path.join(dest_dir, file))

def unzip_file(path, dest):
    ''' Unzip specific file. Path should start with zip:// '''
    xbmcvfs.copy(path, dest)
    #LOG.debug("unzip: %s to %s", path, dest)

def unzip(path, dest, folder=None):
    ''' Unzip file. zipfile module seems to fail on android with badziperror.'''
    path = quote_plus(path)
    root = "zip://" + path + '/'

    if folder:
        xbmcvfs.mkdir(os.path.join(dest, folder))
        dest = os.path.join(dest, folder)
        root = get_zip_directory(root, folder)
    dirs, files = xbmcvfs.listdir(root)
    if dirs:
        unzip_recursive(root, dirs, dest)

    for file in files:
        unzip_file(os.path.join(root, file), os.path.join(dest, file))
    #LOG.warn("Unzipped %s", path)

def get_zip_directory(path, folder):
    dirs, files = xbmcvfs.listdir(path)
    if folder in dirs:
        return os.path.join(path, folder)
    for directory in dirs:
        result = get_zip_directory(os.path.join(path, directory), folder)
        if result:
            return result


def remove_dir(folder):
    import os, shutil
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def countdown(bKill=False):
    from xbmcaddon import Addon
    from xbmcgui import DialogProgress
    from xbmc import executebuiltin, Monitor

    addonInfo = Addon().getAddonInfo
    addonName = addonInfo('name')

    Addon().setSetting('xs_logo', 'true')   # wird noch nicht ausgewertet
    executebuiltin("Dialog.Close(all)")
    executebuiltin("ActivateWindow(Home)")

    seconds = 5
    percentage = 100
    monitor = Monitor()
    pDialog = DialogProgress()
    pDialog.create(addonName + ' Manipulation')
    # while not monitor.abortRequested() and percentage > 0:
    while percentage > 0:
        # percentage -= 20
        # secondsTxt = "seconds" if seconds > 1 else "second"
        # pDialog.update(percentage, f"Kodi wird in {seconds} {secondsTxt} beendet.")
        pDialog.update(percentage, f"{addonName} bzw. Kodi wird in wenigen Sekunden beendet.")
        seconds -= 1
        percentage -= 20
        if monitor.waitForAbort(1): dummy =''
        #if monitor.waitForAbort(1): break
        #if pDialog.iscanceled(): return True
    pDialog.close()

    ## Addon deaktivieren & Kodi beenden
    if not bKill:
        from xbmc import executeJSONRPC
        addonInfo = Addon().getAddonInfo
        addonId = addonInfo('id')  # 'plugin.video.xship'
        executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s", "enabled":false}}' % addonId)
        # Kodi beenden
        executebuiltin('Quit')
        exit()

def kill():     # Löschfunktion
    countdown(True)

    from xbmcaddon import Addon
    from xbmc import getInfoLabel, executebuiltin, executeJSONRPC
    try: from xbmcvfs import translatePath
    except: from xbmc import translatePath

    addonInfo = Addon().getAddonInfo
    addonId = addonInfo('id')
    addonPath = translatePath(addonInfo('path'))
    addonProfilePath = translatePath(addonInfo('profile'))

    executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","id":1,"params":{"addonid":"%s", "enabled":false}}' % addonId)
    remove_dir(addonPath)
    remove_dir(addonProfilePath)

    # ## Reload Profil oder Kodi beenden
    # ##==================================
    # # Reload Profil
    # profil = getInfoLabel('System.ProfileName')
    # if profil: executebuiltin('LoadProfile(' + profil + ',prompt)')

    # Kodi beenden
    executebuiltin('Quit')
    exit()

# # Todo - soll mal Hilfefunktion werden
def help():
    return 'OK' # Platzhalter

