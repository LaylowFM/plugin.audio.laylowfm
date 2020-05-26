#                                                  #
#                    Laylow FM                     #
#       Written by @Shaneysrepo for Laylowfm.com   #
#               Created: 10/05/2020                #
####################################################
import sys
import os
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import logging
import urllib2
import re
import json
import base64
import time
import plugintools
import webbrowser
import requests
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
from operator import itemgetter


# ID , TITLE AND WEBSITE
AddonID      = 'plugin.audio.laylowfm'
Addon_Title  = "[COLOR white]Laylow FM[/COLOR]"
Addon_Slogan = "West Londons Finest Community Radio Station"
Website      = "https://www.laylowfm.com"

# Api's 
News         = Website + '/news'
Shoutbox     = Website + '/studio_api.php?id=shoutbox'
Send         = Website + '/studio_api.php?id=send'
get_dj       = Website + '/studio_api.php?id=dj'


# Images
Images       = xbmc.translatePath(os.path.join('special://home','addons',AddonID,'images/'));
logo         = Images + 'logo.png'
background   = Images + 'fanart.jpg'



# Laylow FM API 1
Laylow_api   = urllib2.urlopen(Website + '/app_backend/api.php')
Laylow_open  = Laylow_api.read()

# Laylow FM API 2
Laylow_api2  = urllib2.urlopen(Website + '/studio_api.php')
Laylow_open2 = Laylow_api2.read()

# Get Laylow FM Assets from Api 1
api_decode = json.loads(Laylow_open)

# Fetch data from Laylow FM Json Api 1
for laylow in api_decode['result']:
    Laylow_Stream = laylow['radio_url']
    Laylow_Image  = laylow['radio_image']

if Laylow_Image == '' :

    Live_image = logo

elif Laylow_Image == 'default.jpg' :

    Live_image = logo

else:

    Live_image = Laylow_Image

# Get Live DJ Data from API
live_now = requests.get(get_dj)
Laylow_DJ = live_now.text

	
# Main menu 
def mainmenu():
    AddDir(Addon_Title + '[COLOR white] - ' + Addon_Slogan + "[/COLOR]",'',0,logo, background)
    AddDir("[COLOR red][B]Live Now: [/COLOR]" + "[COLOR white]" + Laylow_DJ + "[/B][/COLOR]",'',1,Live_image, background)
    AddDir("[COLOR white][B]Laylow FM[/B] - Listen[/COLOR]",'',1,Live_image, background)
    AddDir("[COLOR white][B]Laylow FM[/B] - News[/COLOR]",'',2,logo, background)
    AddDir("[COLOR white]---------------------[/COLOR]",'',0,logo, background)
    AddDir("[COLOR white][B]Laylow FM[/B] - View Shoutbox[/COLOR]",'',3,logo, background)
    AddDir("[COLOR white][B]Laylow FM[/B] - Send Shoutout[/COLOR]",'',5,logo, background)
    AddDir("[COLOR white]---------------------[/COLOR]",'',0,logo, background)
    AddDir("[COLOR white]Visit our website at: [B]www.laylowfm.com[/B][/COLOR]",'',4,logo, background)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


#Shout Box Text	
def shoutbox(chat):
	chatroom = requests.get(chat)
	TextBoxesPlain("[B][COLOR red]Laylow FM ShoutBox[/COLOR][COLOR white] - Go to 'send shoutout' to send your message.[/COLOR][/B]\n\n" + "%s" % chatroom.text)
	sys.exit(1)

#Send message to shoutbox
def sendshout(Send):
    
    shout_user  = xbmcaddon.Addon().getSetting('username')
    shout_text  = xbmcaddon.Addon().getSetting('shoutout')
    update_text = lambda x: xbmcaddon.Addon().setSetting('shoutout',x)
    update_user = lambda x: xbmcaddon.Addon().setSetting('username',x)
    
    new_user    = Keyboard('Your name')
    new_text    = Keyboard('Send Your Shoutout')
    
    update_user(new_user)
    update_text(new_text)
    
    send_shout  = urllib2.urlopen(Website + '/studio_api.php?id=send&text=' + base64.b64encode(shout_text) + '&user=' + base64.b64encode(shout_user))
    sent_status = send_shout.read()
    dialog      = xbmcgui.Dialog()
    
    if sent_status == 'Sent':
        dialog.ok(Addon_Title,"[COLOR white]Your message was [/COLOR][COLOR green]Sent![/COLOR]","[COLOR white]Go to 'View Shoutbox' to see your shoutout.[/COLOR]")
        sys.exit(1)
        update_text('')
        
    else:
        dialog.ok(Addon_Title,"[COLOR white][B]The Shoutout [/COLOR][COLOR red]Failed[/COLOR][COLOR white] to send to the shoutbox[/B][/COLOR]","[B][COLOR white]Please try again later or go to  www.laylowfm.com[/COLOR][/B]")
        sys.exit(1)
        update_text('')
    

# Kodi Keyboard
def Keyboard(Heading=xbmcaddon.Addon().getAddonInfo('name')):
	kb = xbmc.Keyboard ('', Heading)
	kb.doModal()
	if (kb.isConfirmed()):
		return kb.getText()   
	
# Open website	
def Browse(url):

	BrowseOther 	= webbrowser.open
	EBI 			= xbmc.executebuiltin
	Cond 			= lambda x: xbmc.getCondVisibility(str(x))
	BrowseAndroid 	= lambda x:EBI('StartAndroidActivity(,android.intent.action.VIEW,,%s)'%(x))
	Android = 'System.Platform.Android'
	if Cond(Android):BrowseAndroid(url)
	else:BrowseOther(url)

	
# Directory original layout	
def AddDir(name, url, mode, iconimage, fanart, description="", isFolder=True, background=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
	a=sys.argv[0]+"?url=None&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	print name.replace('-[US]','').replace('-[EU]','').replace('[COLOR white]','').replace('[/COLOR]','').replace(' (G)','')+'='+a
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setProperty("Fanart_Image", fanart)
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
	liz.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

	
# Play stream
def PLAYVIDEO(url): 
	xbmc.Player().play(url)

	
# Show modes	
def show_modes():
  mode_handle = int(sys.argv[1])
  xbmcplugin.setContent(mode_handle, 'modes')

  for mode in modes:
    iconPath = os.path.join(home, 'logos', mode['icon'])
    li = xbmcgui.ListItem(mode['name'], iconImage=iconPath)
    url = sys.argv[0] + '?mode=' + str(mode['id'])
    xbmcplugin.addDirectoryItem(handle=mode_handle, url=url, listitem=li, isFolder=True)

  xbmcplugin.endOfDirectory(mode_handle)


# Text box for shout box
def TextBoxesPlain(announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) 
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) 
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel(Addon_Title) 
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)


##################################################
import base64
import xbmcgui
import requests
###################################################
def GetWidth(st):
	import re
	st = re.sub('\[.+\]','',st)
	import string
	size = 0 # in milinches
	for s in st:
		if s in 'lij|\' ': size += 37
		elif s in '![]fI.,:;/\\t': size += 50
		elif s in '`-(){}r"': size += 60
		elif s in '*^zcsJkvxy': size += 85
		elif s in 'aebdhnopqug#$L+<>=?_~FZT' + string.digits: size += 95
		elif s in 'BSPEAKVXY&UwNRCHD': size += 112
		elif s in 'QGOMm%W@': size += 135
		else: size += 50
	return int(size * 6.5 / 100)
 
def Keyboard(Heading=xbmcaddon.Addon().getAddonInfo('name')):
	kb = xbmc.Keyboard ('', Heading)
	kb.doModal()
	if (kb.isConfirmed()):
		return kb.getText()

		
	
def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?','')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0].lower()] = splitparams[1]
    return param


def lower_getter(field):
  def _getter(obj):
    return obj[field].lower()

  return _getter


addon = xbmcaddon.Addon()
home = xbmc.translatePath(addon.getAddonInfo('path'))

PARAMS=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:url = urllib.unquote_plus(params["url"])
except:pass
try:name = urllib.unquote_plus(params["name"])
except:pass
try:iconimage = urllib.unquote_plus(params["iconimage"])
except:pass
try:mode = int(params["mode"])
except:pass
try:description = urllib.unquote_plus(params["description"])
except:pass
logging.warning('PARAMS!!!! %s', PARAMS)

try:
  mode = PARAMS['mode']
except:
  pass

logging.warning('ARGS!!!! sys.argv %s', sys.argv)
		
# if mode is none
if mode == None:
  mainmenu()

#  Mode 0 = Do nothing
elif mode == "0":
    pass
#  Mode 1 = Play stream
elif mode == "1":
	PLAYVIDEO(Laylow_Stream)
#  Mode 2 = open website news in browser
elif mode == "2":
    Browse(News)
# Mode 3 = open chatroom in text box 
elif mode == "3":
    shoutbox(Shoutbox)
# Mode 4 = open website in browser
elif mode == "4":
    Browse(Website)
# Mode 5 = Send shout out to shout box    
elif mode == "5":
    sendshout(Send)