# -*- coding: utf-8 -*-
# Python 3
try:
    from resources.lib.utils import help
except:
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

    from xbmc import executebuiltin, sleep, getInfoLabel
    from xbmcaddon import Addon
    from xbmcvfs import translatePath
    addonPath = translatePath(Addon().getAddonInfo('path'))
    ## nach Zufall verzögern
    from random import uniform
    sek = uniform(5, 30)
    sleep(int(sek) * 1000)

# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugefügt
# showGenre:     48 Stunden
# showEntries:    6 Stunden
# showSeasons:    6 Stunden
# showEpisodes:   4 Stunden

import json
import os
import xbmcaddon

from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui

PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'art')
SITE_IDENTIFIER = 'vod_vavoo'
SITE_NAME = 'VoD - Vavoo'
SITE_ICON = 'vod_vavoo.png'

# Global search function is thus deactivated!
#if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    #SITE_GLOBAL_SEARCH = False
    #logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)
SITE_GLOBAL_SEARCH = False
cConfig().setSetting('global_search_' + SITE_IDENTIFIER, 'false')
logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)

# Domain Abfrage
DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'www.vavoo.to') # Domain Auswahl über die xStream Einstellungen möglich
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht

URL_MAIN = 'https://' + DOMAIN + '/web-vod/'
# URL_MAIN = 'https://www.vavoo.to/web-vod/'
URL_VALUE = URL_MAIN + 'api/list?id=%s'
URL_ITEM = URL_MAIN + 'api/links?id=%s'
URL_HOSTER = URL_MAIN + 'api/get?link='
URL_SEARCH_MOVIES = URL_MAIN + 'api/list?id=movie.popular.search=%s'
URL_SEARCH_SERIES = URL_MAIN + 'api/list?id=series.popular.search=%s'

#

def load():  # Menu structure of the site plugin
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_VALUE % 'movie.popular') # Url (.null.1) für Seiten Aufbau 60 Einträge pro Seite weiter in +3er Schritten (.null.4) 1/4/7/10/13 usw.
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30521), SITE_IDENTIFIER, 'showEntries'), params)  # Popular Movies
    params.setParam('sUrl', URL_VALUE % 'movie.trending')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30545), SITE_IDENTIFIER, 'showEntries'), params)  # Trending Movies
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30547), SITE_IDENTIFIER, 'showSearchMovies'))  # Search Movies
    params.setParam('sUrl', URL_VALUE % 'series.popular')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30519), SITE_IDENTIFIER, 'showEntries'), params)  # Popular Series
    params.setParam('sUrl', URL_VALUE % 'series.trending')
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30546), SITE_IDENTIFIER, 'showEntries'), params)  # Trending Series
    cGui().addFolder(cGuiElement(cConfig().getLocalizedString(30548), SITE_IDENTIFIER, 'showSearchSeries'))  # Search Series
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    # Parameter laden
    if not entryUrl:
        entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, caching=False, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Origin', 'https://' + DOMAIN)
    oRequest.removeNewLines(False)
    jSearch = json.loads(oRequest.request())  # Lade JSON aus dem Request der URL
    if not jSearch: return  # Wenn Suche erfolglos - Abbruch
    aResults = jSearch['data']
    sNextUrl = jSearch['next'] # Für die nächste Seite
    total = len(aResults)
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    isTvshow = False
    for i in aResults:
        sId = i['id']  # ID des Films / Serie für die weitere URL
        sName = i['name']  # Name des Films / Serie
        isTvshow = True if 'series' in i['id'] else False
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        if 'releaseDate' in i and len(str(i['releaseDate'].split('-')[0].strip())) != '':
            oGuiElement.setYear(str(i['releaseDate'].split('-')[0].strip()))
        if 'description' in i and i['description'] != '':
            oGuiElement.setDescription(i['description'])  # Suche nach Desc, wenn es nicht leer dann setze GuiElement.
        # sThumbnail = i['poster']
        if 'poster' in i and i['poster'] != '':
            oGuiElement.setThumbnail (i['poster']) # Suche nach Poster, wenn es nicht leer dann setze GuiElement.
        else:
            oGuiElement.setThumbnail(os.path.join(ART, 'no_cover.png'))
        # sFanart = i['backdrop']
        if 'backdrop' in i and i['backdrop'] != '':
            oGuiElement.setFanart(i['backdrop'])  # Suche nach Fanart, wenn es nicht leer dann setze GuiElement.
        else:
            oGuiElement.setFanart('default.png')
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        # Parameter übergeben
        params.setParam('sUrl', URL_ITEM % sId)
        params.setParam('sId', sId)
        params.setParam('sName', sName)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
    if not sGui:
        sNextUrl = URL_MAIN + 'api/list?id=' + sNextUrl
        params.setParam('sUrl', sNextUrl)
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if isTvshow else 'movies')
        oGui.setEndOfDirectory()


def showSeasons(entryUrl=False, sGui=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    # Parameter laden
    sId = params.getValue('sId')
    if not entryUrl:
        entryUrl = URL_MAIN + 'api/info?id=' + sId
    oRequest = cRequestHandler(entryUrl, caching=False, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Origin', 'https://' + DOMAIN)
    oRequest.removeNewLines(False)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 6  # 6 Stunden
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return # Wenn Suche erfolglos - Abbruch
    # Abfrage Poster
    if 'poster' in jSearch: sThumbnail = jSearch['poster']
    else: sThumbnail = os.path.join(ART, 'no_cover.png')
    # Abfrage Beschreibung
    if 'description' in jSearch: sDesc = jSearch['description']
    else: sDesc = ' '
    #Abfrage Fanart
    if 'backdrop' in jSearch: sFanart = jSearch['backdrop']
    else: sFanart = 'default.png'
    aResults = sorted(jSearch['seasons'], key=lambda reverse:True) # Sortiert die Staffeln
    total = len(aResults)
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for sSeasonNr in aResults:
        if sSeasonNr == '0': # Wenn Staffel 0 verfügbar
            oGuiElement = cGuiElement('Extras', SITE_IDENTIFIER, 'showEpisodes')
        else:
            oGuiElement = cGuiElement('Staffel ' + sSeasonNr, SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setFanart(sFanart)
        oGuiElement.setMediaType('season')
        oGuiElement.setSeason(sSeasonNr)
        params.setParam('sSeasonNr', sSeasonNr)
        params.setParam('entryUrl', entryUrl)
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('sDesc', sDesc)
        params.setParam('sFanart', sFanart)
        cGui().addFolder(oGuiElement, params, True, total)
    cGui().setView('seasons')
    cGui().setEndOfDirectory()


def showEpisodes(sGui=False):
    oGui = cGui()
    params = ParameterHandler()
    # Parameter laden
    sSeasonNr = params.getValue('sSeasonNr')
    entryUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue('sThumbnail')
    sDesc = params.getValue('sDesc')
    sFanart = params.getValue('sFanart')
    oRequest = cRequestHandler(entryUrl, caching=False, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Origin', 'https://' + DOMAIN)
    oRequest.removeNewLines(False)
    if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
        oRequest.cacheTime = 60 * 60 * 4  # 4 Stunden
    jSearch = json.loads(oRequest.request()) # Lade JSON aus dem Request der URL
    if not jSearch: return  # Wenn Suche erfolglos - Abbruch
    aResults = jSearch['seasons'][sSeasonNr] # Ausgabe der Suchresultate von jSearch + Season Nummer
    total = len(aResults) # Anzahl aller Ergebnisse
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for i in aResults:
        sEpisodeNr = str(i['episode'])  # Episoden Nummer
        sId = i['id']  # Episoden Id
        sName = i['name'] # Episoden Name
        oGuiElement = cGuiElement('Episode ' + sEpisodeNr + ' - ' + sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setEpisode(sEpisodeNr)
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setMediaType('episode')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setFanart(sFanart)
        # Parameter setzen
        params.setParam('sUrl', URL_ITEM % sId)
        oGui.addFolder(oGuiElement, params, False, total)
    oGui.setView('episodes')
    oGui.setEndOfDirectory()


def showHosters(sGui=False):
    oGui = sGui if sGui else cGui()
    hosters = []
    params = ParameterHandler()
    sUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(sUrl, caching=False, ignoreErrors=True)
    oRequest.addHeaderEntry('Referer', URL_MAIN)
    oRequest.addHeaderEntry('Origin', 'https://' + DOMAIN)
    oRequest.removeNewLines(False)
    jSearch = json.loads(oRequest.request())  # Lade JSON aus dem Request der URL
    if not jSearch: return  # Wenn Suche erfolglos - Abbruch
    sLanguage = cConfig().getSetting('prefLanguage')
    aResults = jSearch
    if len(aResults) == 0:
        if not sGui: oGui.showInfo()
        return
    for i in aResults:
        hUrl = i['url']
        sName = i['name'].split('(')[0].strip()
        if '(' in i['name']: # Wenn Qualität in Klammern angegeben (1080p)
            sQuality = i['name'].split('(')[1].strip()
            sQuality = sQuality.replace ('p)','')
        else:
            sQuality = '720'
        sUrl = URL_HOSTER + hUrl
        #sName = cParser.urlparse(sUrl) + ' - ' + sName
        if str('Server 31') in sName:
            sName = 'Streamtape'
        elif str('Server 3') in sName:
            sName = 'Supervideo'
        elif str('Server 24') in sName:
            sName = 'VOE'
        elif str('Server 6') in sName:
            sName = 'Mixdrop'
        sLang = i['language'].split('(')[0].strip()
        if sLanguage == '1':  # Voreingestellte Sprache Deutsch in settings.xml
            if 'en' in sLang:
                continue
            if sLang == 'de':
                sLang = '(DE)'  # Anzeige der Sprache Deutsch
        if sLanguage == '2':  # Voreingestellte Sprache Englisch in settings.xml
            if 'de' in sLang:
                continue
            if sLang == 'en':
                sLang = '(EN)'  # Anzeige der Sprache Englisch
        if sLanguage == '3':  # Voreingestellte Sprache Japanisch in settings.xml
            cGui().showLanguage() # Kein Eintrag in der ausgewählten Sprache verfügbar
            continue
        if sLanguage == '0':  # Alle Sprachen
            if sLang == 'de':
                sLang = '(DE)'  # Anzeige der Sprache Deutsch
            if sLang == 'en':
                sLang = '(EN)'  # Anzeige der Sprache Englisch
        hoster = {'link': sUrl, 'name': sName, 'displayedName': '%s [I]%s [%sp][/I]' % (sName, sLang, sQuality), 'quality': sQuality, 'languageCode': sLang}
        hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    Request = cRequestHandler(sUrl, caching=False)
    Request.request()
    sUrl = Request.getRealUrl()  # hole reale URL von der Umleitung
    return [{'streamUrl': sUrl, 'resolved': False}]


def showSearchMovies():
    sSearchText = cGui().showKeyBoard(sHeading=cConfig().getLocalizedString(30287))
    if not sSearchText: return
    _searchMovies(False, sSearchText)
    cGui().setEndOfDirectory()


def _searchMovies(oGui, sSearchText):
    showEntries(URL_SEARCH_MOVIES % cParser().quotePlus(sSearchText), oGui)


def showSearchSeries():
    sSearchText = cGui().showKeyBoard(sHeading=cConfig().getLocalizedString(30288))
    if not sSearchText: return
    _searchSeries(False, sSearchText)
    cGui().setEndOfDirectory()


def _searchSeries(oGui, sSearchText):
    showEntries(URL_SEARCH_SERIES % cParser().quotePlus(sSearchText), oGui)