#!/usr/bin/env python
# coding: utf-8

# # # Controls
# 
# # ### StoreRevert and removeClickHandlers 

# In[1]:


#standalone
from ipywidgets import * 
output=Output()

def removeClickHandlers(button):
    button._click_handlers.callbacks=[]

def doStore(e):
    with output:
        print('doStore', str(e))
    
def doRevert(e):
    with output:
        print('doRevert', str(e))

def StoreRevert():
    Store= Button(description='Store')
    Store.on_click(doStore)
    Store.style.button_color = 'lightyellow'

    Revert= Button(description='Revert')
    Revert.on_click(doRevert)
    Revert.style.button_color = 'lightyellow'

    return Store, Revert

TESTING=0
if TESTING:
    Store, Revert = StoreRevert()
    display(Store, Revert, output)
#removeClickHandlers(Revert) 


# ### ControlBox and disableCB


# In[2]:


#standalone
from ipywidgets import *
output=Output()

"""
This is the [-]_RecNum_[+] controlbox.
"""

def dec(e):
    global recNum
    recNum.value -= 1
        
def inc(e):
    global recNum
    recNum.value += 1

fullWidth = widgets.Layout(width='100%')

    
recNum = widgets.BoundedIntText(
    value=7,
    min=1,
    max=2000,
    step=1,
    disabled=False,
    layout = widgets.Layout(width='60%'))

def disableCB(disable=False):
    global controlBox
    colors={True:'yellow', False:None}
    for child in controlBox.children:
        child.disabled = disable
        child.style.background=colors[disable]     #for recNum
        child.style.button_color=colors[disable]   #for minus and plus

    
def ControlBox():
    minus =Button(description = '-', layout=Layout(width = '10%'))
    plus  =Button(description = '+', layout=Layout(width = '10%'))
    minus.on_click(dec)
    plus.on_click(inc)
    controlBox = HBox((minus,recNum,plus))
    controlBox.disabled=False        
    return controlBox

TESTING=0
if TESTING:
    controlBox = ControlBox()
    display(controlBox)      #controls should work
    display(output)
    #disableCB(True)


# ### The next cells build upon each other

# #### Twitcher


# In[3]:


#standalone
from ipywidgets import *
TESTING=1
output = Output()

def onTwitch(e):
    with output:
        print('overwrite me')

def twitch(e):
    e['owner'].style.background='yellow'
    onTwitch(e)
    with output:
        print('twitch', str(e))

def Twitcher(description = 'change me',
             value='and I should turn yellow'):
    T= Text(description=description,value=value)
    T.observe(twitch, type='change', names='value')
    return(T)

TESTING=0
if TESTING:
    display(output)
    T=Twitcher()
    display(T)


# # ## Twitchers and Three Columns

# In[4]:


#requires Twitch

#Create 3 columns: Twitchers, TextEditor, HTML
#uses Twitch

from collections import OrderedDict

fields=OrderedDict(a='one',b='two',c='three')

#populate a dictionary of Twitchers from the fields
def Twitchers(fields=fields):
    """
        twitchers['a'] will be a twitcher with a value of 'one'
    """
    twitchers=OrderedDict()
    for description, value in fields.items():
        twitchers[description] = Twitcher(description,value)
    return twitchers

def BottomPanel(twitchers):
    left = VBox(list(twitchers.values()),layout=widgets.Layout(height="1000px", width="20%"))
    middle = Textarea(value=10*'init\n',layout=widgets.Layout(height="1000px", width="40%"))
    right  = HTML(value=10*'<i>init</i>\n',layout=widgets.Layout(height="1000px", width="40%"))
    Bot = HBox([left, middle, right])
    Bot.left=left
    Bot.middle=middle
    Bot.right=right
    return Bot
               
    
TESTING=0
if TESTING: #twitchers should twitch.  don't expect HTML panel to't update

    twitchers=Twitchers()
    bottomPanel=BottomPanel(twitchers)
    display(bottomPanel)


# # ## pygSheets  getRowData(), putRowData() 

# In[5]:


#standalone
"""make sure the credentials file (enablebadger...) is present"""
from collections import OrderedDict

import pygsheets
CREDENTIALSFILE = 'enablebadger-b31383b767ef.json'
sheetURL = 'https://docs.google.com/spreadsheets/d/140rX3pg1s69xxEh6dTse4Gkjv1bmcEi3ECK26KMZrAc/edit#gid=1364324556'
googleClient = pygsheets.authorize(service_file=CREDENTIALSFILE)
gs=googleClient.open_by_url(sheetURL)
sheet=gs.worksheets()[0]

def getRowData(rowNum=2): # usually to come from recNum.value):
    s = f'get {rowNum=}'
    try:
        msg.value = s
    except NameError:
        pass
    keys=sheet.get_row(1)
    values = sheet.get_row(rowNum)
    ret = OrderedDict()
    for i,key in enumerate(keys):
        ret[key]=values[i]
    return ret
#rowData = getRowData(20)

        
TESTING=0
if TESTING:
    print(sheet.title)
    rowData = getRowData()
    print(rowData)


# # ## Twitchers <-> Content, updateHTML, loadRow, putRow
# 
# #  ## Imagery

# In[6]:


#standalone
from IPython.display import Image
import json
def getImageDict():
    return json.loads(open('imgDict.json').read())

def putImageDict():
    f=open('imgDict.json','w')
    f.write(json.dumps(imgDict))
    print('savedImgDict')
            
import cloudinary
import cloudinary.uploader
import cloudinary.api
import cloudinary.utils


svgURL='http://www.ingafoundation.org/wp-content/themes/hueman-docandtee/images/inga-logo.svg'
filePath = jpgPath='tmp2.jpg'


def enCloud(filePath=filePath,public_id=None):
    """ upload the pre-existing imagefile at filePath, 'tmp2.jpg'
        return a URL that uses the same 'first name' as the imagefile (e.g, tmp2)
    
    """
    if not public_id:
        public_id = filePath.split('.')[-1]
    
    cloudinary.config(
      cloud_name = 'e-nable-org',  
      api_key = '784995798559293',  
      api_secret = 'L-A0R81r4FoLPZEgA7kdXi4e9AI'  
    )
    resp = cloudinary.uploader.upload(file=filePath, public_id=public_id)
    #print('image now at', resp['url'])
    print(resp)
    return resp['url']
    
            
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from IPython.utils.io import capture_output

svgURL='http://www.ingafoundation.org/wp-content/themes/hueman-docandtee/images/inga-logo.svg'
jpgPath='tmp2.jpg'

def svg_to_jpg(svgURL=svgURL, jpgPath=jpgPath):
    capture_output(stderr=True, display=False) #gets some, usually
    drawing = svg2rlg(svgURL)
    renderPM.drawToFile(drawing,jpgPath, fmt='jpg')
    return(jpgPath)

TESTING=0
if TESTING:
    imgPath = svg_to_jpg(svgURL=svgURL, jpgPath=jpgPath)
    print('got ', imgPath, 'expect warnings and then image')
    display(Image(imgPath))




# # data-filled BottomPanel

# In[7]:


#requires Twitchers, pyGsheets
"""update html  whenever 
    (1) a twitcher twitches (thanks to onTwitch)
    (2) OR when the TA changes (thanks to TA.observe)
"""

twitchers=Twitchers()

def putRowData(rowNum=2): #recNum.value):
    global twitchers
    print(f'{twitchers.keys()}')
    twitchers['Description'].value = bottomPanel.middle.value 
    data = [twitcher.value for twitcher in twitchers.values()]  #twichers.values are the indivdual widgets.  *Their* values are what we want.
    sheet.update_row(recNum.value, data)
    ret = f'Stored row {recNum.value} back to spreadsheet'
    return ret

def html():
    """generate html based on an amalgam of twitcher values and middle value"""
    return 'Dummy <b>HTML</b>'

def html():
    thumb = f"<img src={twitchers['Thumbnails'].value} align=right width='25%'/>"
    title =  f"<h2>{twitchers['Project Name'].value}</h2>"
    location = f"<h4>{twitchers['Location'].value}</h4>"
    
    EditorContent = bottomPanel.middle.value
    pictureURL = twitchers['Picture'].value
    if pictureURL:
        imgHTML = f"<img src={pictureURL} width=100%></img>"
    else:
        imgHTML = ''
        
    button = f'<button style="background-color: lightgreen; width: 100%;">{twitchers["Source"].value}</button>'
    
    html = thumb + title +  location + imgHTML + EditorContent + button
    return html    

def updateHTML(e):
    bottomPanel.right.value= html()
    with output:
        print('updateHTML', str(e)) 

def onTwitch(e):                   # < - when a twitch occurs
    with output:
        print('NEW on Twitch')
    updateHTML(e)

def loadRow(rowData):  #assume rowData exists
    global bottomPanel
    for key in rowData:
        twitchers[key].value=rowData[key]
    bottomPanel.middle.value = rowData['Description']
    bottomPanel.right.value = html()

def editorChange(e):
    twitchers['Description'].value = bottomPanel.middle.value
    updateHTML(e)
    
TESTING=0
if TESTING:
    rowData = getRowData(3)
    twitchers=Twitchers(rowData)
    bottomPanel = BottomPanel(twitchers)
    bottomPanel.middle.observe(editorChange, type='change')

    loadRow(rowData)
    display(bottomPanel)




# ### Include spreadsheet IO

# In[ ]:





# In[8]:


#requres Twitchers, pygsheets, control Box StoreRevert, 

#Need to wire in store, revert and + and - actions

def noYellow(e): #      # <--doStore, doRevert
    disableCB(False)
    for item in twitchers.values():
        item.style.background = None

def doStore(e): 
    rowNum=recNum.value
    msg.value = putRowData(rowNum)
    noYellow(e) #-->
    resetCheckers()


def doRevert(e): 
    rowNum=recNum.value
    msg.value = 'Retrieving row #{rowNum}'
    loadRow(getRowData(rowNum))
    noYellow(e) #-->
    resetCheckers()
    
def onTwitch(e):                   # < - when a twitch occurs
    updateHTML(e)    #-->
    disableCB(True)  #-->
    with output:
        print('NEW on Twitch')
        
        
def recNummer(e):
    global msg
    msg.value=f'should retrieve record #{recNum.value}'
    loadRow(getRowData(recNum.value))
    noYellow(e)
    updateHTML(e)
    try:
        resetCheckers()
    except NameError:
        pass
        #resetCheckers is in a subsequent cell
        
        
recNum.value=2
recNum.max = sheet.rows

rowData = getRowData(recNum.value)
twitchers=Twitchers(rowData)
bottomPanel = BottomPanel(twitchers)
bottomPanel.middle.observe(editorChange, type='change')
msg=Textarea('one\ngwo', layout=fullWidth)

Store, Revert = StoreRevert()
controlBox = ControlBox()

loadRow(rowData)

RunChecksBtn = Button(description='Run checks?')
ImageSourcesBtn = Button(description='Image Sources?')
ImageWidthsBtn =  Button(description='Image Widths?')
ReportsBox=msg #Textarea(value='Reports will go here.', layout= widgets.Layout(width='30%'))


###ReportsBox now piggybacking on msg

output.clear_output()

bottomPanel.middle.observe(editorChange, type='change')
recNum.observe(recNummer, type='change', names='value')
twitchers['Description'].disabled=True
#twitchers['Source'].disabled=True

geturlT=Text(value='Source goes here')
geturlT.style.background='lightblue'

#####################################

TESTING=0
if TESTING:
    #display(HBox([Store, Revert, RunChecksBtn, ImageSourcesBtn, ImageWidthsBtn, ReportsBox]))      #controls should work
    display(HBox([Store, Revert, RunChecksBtn, ImageSourcesBtn, ImageWidthsBtn]))      #controls should work
    display(HBox([controlBox,geturlT]))
    display(msg)
    display(bottomPanel)

# ## imgUploader


# In[ ]:





# In[9]:


#standalone
from ipywidgets import FileUpload, Text, HBox, widgets

uploadT=Text(value = 'Copy uploaded image URL from here', layout = widgets.Layout(width='100%'))
#uploadT.style.background='lightblue'

def onFile(e):
    if FU.value:
        content = FU.value[0]['content']
        extension = '.' + FU.value[0]['name'].split('.')[-1]
        infName = FU.value[0]['name']
        FU.description = infName
        outName = "saved-output" + extension
        baseName = infName.split('.')[-2]
        #print(f'{infName=}, {content=}, {outName=}, {baseName=}')
        f= open(outName, "wb")
        f.write(content.tobytes())
        #print('saved', outName)
        res = enCloud(outName,public_id = baseName)
        uploadT.value = str(res)
        FU.value=[]
        FU.description = 'New Image to Cloudinary?'


FU = FileUpload(description='New Image to Cloudinary?', layout = widgets.Layout(width='40%'),
    accept='image/*',  # Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
    multiple=False)    # True to accept multiple files upload else False)

FU.observe(onFile, 'value')
imgUploader = HBox([FU,uploadT])

TESTING=0
if TESTING:
    display(imgUploader)


# In[ ]:





# In[ ]:





# ## incorporate ImgUploader

# In[10]:


from ipywidgets import *
def resetCheckers(): 
    RunChecksBtn.description='Run checks?'
    ImageSourcesBtn.description='Image Sources?'
    ImageSourcesBtn.style.button_color=None
    ImageWidthsBtn.style.description='Image Widths?'
    ImageWidthsBtn.button_color=None
    ReportsBox.value='Reports will go here.'
    ReportsBox.style.background = None
    uploadT.value= '        copy uploaded image URL from here'
    ImageSourcesBtn.style.button_color=None
    ImageSourcesBtn.description = 'Image Sources?'
    msg.style.background=None

    msg.value=''
    msg.style.background = None
    try:
        geturlT.value = twitchers['Source'].value
    except NameError:
        pass #geturlT is not defined yet



def cloudinize():
    print('cloudinizing')
    msg.value='Cloudinizing'
    ImageSourcesBtn.style.button_color=None
    ImageSourcesBtn.description = 'Image Sources?'
    ReportsBox.value=''
    for key in ['Thumbnails', 'Picture']: #update with cloudinary
        imgURL = twitchers[key].value
        print('I am  here')
        if 'cloudinary'not in imgURL: #update with imageDict or with enCloud
            if imgURL in imageDict:
                newURL = imageDict[imgURL]
                public_id = 'FromDict: ' +  newURL 
            else:
                public_id = twitchers['Project Name'].value[:40].replace(' ','_')+ key
                print(public_id)
                newURL = enCloud(imgURL,public_id=public_id)
                imageDict[imgURL] = newURL
                putImageDict()
                
            twitchers[key].value = newURL
            ReportsBox.value = ReportsBox.value + public_id + '\n'
    ReportsBox.style.background = None

def ImageSourcesClick(e):
    B=ImageSourcesBtn
    ret = []
    
    if B.description != 'Cloudinize?':
        OK=True
        #not OK if any image files are not cloudinized
        for key in ['Thumbnails', 'Picture']:
            imgURL = twitchers[key].value
            if 'cloudinary'not in imgURL:
                OK=False
                twitchers[key].style.background = 'pink'
                ret.append(f'{key}:{imgURL}')
                
        if OK:
            ReportsBox.value= 'all cloudinary'
            ReportsBox.style.background = None
            B.button_color= None

        else:
            ReportsBox.value='\n'.join(ret)
            ReportsBox.style.background = 'pink'
            B.description = 'Cloudinize?'
            B.style.button_color= 'orange'
            
    else: #not OK. Cloudinize!
        cloudinize()

def ImageWidthsClick(e):
    ReportsBox.value= ReportsBox.value + '\n' + str(e)
    

def addRow(e):
    sheet.add_rows(1)
    recNum.max = sheet.rows
    newRowBtn.description = f'Max = {sheet.rows};  Inc?'
newRowBtn = Button(description=f'Max = {sheet.rows};  Inc?')
newRowBtn.on_click(addRow)

    
TESTING=1
if TESTING:
    display(imgUploader)
    #display(HBox([Store, Revert, msg, RunChecksBtn, ImageSourcesBtn,  ReportsBox]))      #controls should work
    display(HBox([Store, Revert, RunChecksBtn, ImageSourcesBtn, ImageWidthsBtn]))      #controls should work

    display(HBox([controlBox, newRowBtn], layout=Layout(width = '100%')))
    display(msg)
    display(bottomPanel)

imageDict = getImageDict()
NEEDED=True #THIS IS needed for the Image Buttons
if NEEDED:
    resetCheckers()
    noYellow('init')

    removeClickHandlers(ImageSourcesBtn)
    removeClickHandlers(ImageWidthsBtn)
    ImageWidthsBtn.on_click(ImageWidthsClick)
    ImageSourcesBtn.on_click(ImageSourcesClick)


# # latlon

# In[11]:


from ipywidgets import *
latlonQ = Text(value='Gaithersburg')
latlonA = Text(value='39.1399187, -77.1929215', continuous_update=False)
latlonB = Button(description = '--get Lat, Lon-->')
spacer = Button(disabled=True)
spacer.style.button_color='white'
latlonQ.style.background = 'beige'
latlonA.style.background = 'beige'
latlonB.style.button_color = 'beige'


import requests
import json
from time import sleep

def getLatLon(e):
    print(str(e))
    place = latlonQ.value.split(':')[0]
    place=place.replace(',','')
    response=requests.get(f'https://nominatim.openstreetmap.org/search?q={place}&format=json')
    data = json.loads(response.text)
    try:
        lat = data[0]['lat']
        lon = data[0]['lon']
        latlonA.value= f'{lat}, {lon}'
        latlonA.style.background= 'beige'
    except (KeyError, IndexError):
        latlonA.style.background='pink'
        latlonA.value='LatLon Failed'
        sleep(1)
        latlonA.style.background= None

latlonB.on_click(getLatLon)
latlon = HBox([spacer, latlonQ,latlonB, latlonA])

TESTING=1
if TESTING:
    display(latlon)


# # # add Selenium and Summer

# In[12]:


#!python -m pip install selenium

from selenium import webdriver
import time
from ipywidgets import *
import validators

from bs4 import BeautifulSoup
def prettify(someHTML):
    soup=BeautifulSoup(someHTML)
    return str(soup.prettify())

TESTING = 0
if TESTING:
    s="""<div class="_1dwg _1w_m _q7o" data-visualcompletion="ignore-dynamic" style="font-family: inherit; padding: 12px 12px 0px;"><div style="font-family: inherit;"><div class="l_c3pyo2v0u _5eit i_c3pynyi2f clearfix" style="zoom: 1; margin-bottom: -1px; font-family: inherit;"><div class="clearfix y_c3pyo2ta3" style="zoom: 1; margin-bottom: -6px; font-family: inherit;"><div class="clearfix _42ef" style="overflow: hidden; zoom: 1; font-family: inherit;"><div class="u_c3pyo2ta4" style="padding-bottom: 6px; font-family: inherit;"><div style="font-family: inherit;"><div class="_6a _5u5j" style="display: inline-block; width: 620px; font-family: inherit;"><div class="_6a _5u5j _6b" style="display: inline-block; vertical-align: middle; width: 620px; font-family: inherit;"><h5 class="_7tae _14f3 _14f5 _5pbw _5vra" data-ft="{&quot;tn&quot;:&quot;C&quot;}" id="js_0" style="line-height: 1.38; color: rgb(28, 30, 33); margin: 0px 0px 2px; padding: 0px 22px 0px 0px;"><span class="fwn fcg" style="color: rgb(97, 103, 112); font-family: inherit;"><span class="fwb" style="font-weight: 600; font-family: inherit;"><a class="profileLink" href="https://www.facebook.com/duen.yen?hc_ref=ARSiUf4krzS0e4WN2gzX3TNWE-3g3iEyeD8n5UO1R7Bm-rG5eQPZSUzXVwMvO4suFS4&amp;ref=nf_target" data-ft="{&quot;tn&quot;:&quot;l&quot;}" style="color: rgb(56, 88, 152); cursor: pointer; font-family: inherit;">Duen Hsi Yen</a></span>&nbsp;is&nbsp;<i class="_51mq img sp_tw8Jgo0hhsp_2x sx_020ecc" style="margin-right: 3px; vertical-align: -2.9px; background-image: url(&quot;/rsrc.php/v3/y8/r/NZG1EPwHono.png&quot;); background-size: 17px 68px; background-repeat: no-repeat; display: inline-block; height: 16px; width: 16px; background-position: 0px -34px;"></i>feeling blessed.</span></h5><div class="_5pcp _5lel _2jyu _232_" id="feed_subtitle_782077523;10163220813702524;;9" data-testid="story-subtitle" style="position: relative; color: rgb(97, 103, 112); font-size: 12px; font-family: inherit;"><span class="z_c3pyo1brp" style="font-family: inherit;"><span class="fsm fwn fcg" style="color: rgb(144, 148, 156); font-family: inherit;"><a class="_5pcq" href="https://www.facebook.com/duen.yen/posts/pfbid0Z3d7hzPP5NbEGu1HWDVyMiPhfjy4hwb7j3vcvCKxVedunAQkXgTxfhWbrDL2rYTMl" target="" style="color: rgb(97, 103, 112); cursor: pointer; font-family: inherit;">December 18, 2022</a></span></span><span class="_6spk" role="presentation" aria-hidden="true" style="font-family: inherit;">&nbsp;·&nbsp;</span><div class="_6a _29ee _4f-9 _43_1" data-hover="tooltip" data-tooltip-content="Shared with: Public" role="img" aria-label="Shared with: Public" style="vertical-align: middle; position: relative; display: inline-block; padding: 3px 0px; font-family: inherit;"><span style="font-family: inherit;"><i class="_1lbg img sp_lgtFXQRlG9h_2x sx_13e945" style="background-image: url(&quot;/rsrc.php/v3/yC/r/wdjMXy7QpPG.png&quot;); background-size: 28px 338px; background-repeat: no-repeat; display: block; height: 12px; width: 12px; margin-top: -1px; background-position: 0px -312px;"></i></span></div></div></div></div></div></div></div></div></div><div data-testid="post_message" class="_5pbx userContent _3576" data-ft="{&quot;tn&quot;:&quot;K&quot;}" id="js_2" style="line-height: 1.38; margin-top: 6px; font-family: inherit;"><p style="margin-bottom: 6px; font-family: inherit;">This coming of age story was written by AI ChatGPT based on a young man who contacted me on FB Messenger just yesterday or the day before. After chatting with him I was granted permission to feature him in this story. His name is&nbsp;<a title="Jacob Kayando" class="profileLink" href="https://www.facebook.com/people/Jacob-Kayando/100084044456444/?fref=mentions" style="color: rgb(56, 88, 152); cursor: pointer; font-family: inherit;">Jacob Kayando</a>. The photos are from his timeline or sent to me directly.</p><p style="margin-top: 6px; margin-bottom: 6px; font-family: inherit;">“Growing up in Homa Bay, Kenya, a young boy named Jacob always had a passion for helping others. He lived in a small village near Lake Victoria, and from a young age, he enjoyed volunteering to assist those in need, particularly widows, orphans, and elderly members of the community.<br>In 2018, Jacob joined a project in his village called Kawiya, a community-based farm that grew a variety of organic produce, including kale, spinach, tomatoes, onions, pumpkins, black night shade, mangoes, pawpaws, soursop, jackfruit, bananas, oranges, avocados, and passion fruit.<br>Aside from his work on the farm, Jacob had a number of hobbies that kept him busy. He enjoyed animal training, vegetable gardening, and animal keeping, and he was also an avid bonsai enthusiast. In his spare time, he liked to whittle small wooden figurines, using the skills he had learned from his grandfather.<br>Despite his love for his community and his hobbies, life was not always easy for Jacob. He lived far from the nearest well, and had to pay someone with a donkey to bring him water. Additionally, the area was prone to drought, and Jacob had unfortunately lost some of his animals due to a lack of rainfall.<br>Despite these challenges, Jacob never let his spirits be dampened. He always remembered a motto that he had come up with: "Don't stop helping others, no matter how small your effort may be." Jacob believed that helping others was the quickest way to find true happiness, and he often said: "I am a farmer who believes that helping others is the quick way to find true happiness. Making someone's day a little bit brighter will in turn make your own day that much better."<br>As he grew older, Jacob continued to work on the farm and assist those in need in his community. He became known as a kind and compassionate young man, always willing to lend a helping hand. And although he faced many challenges, Jacob never lost sight of his purpose in life – to make a difference in the world, no matter how small his efforts may seem.<br>As the years passed, Jacob's farm grew and flourished, providing organic produce to the community and beyond. He continued to follow his mottos, always looking for ways to help those in need and bring joy to those around him. And even though life wasn't always easy, Jacob knew that by following his passions and making a positive impact on the world, he could find true happiness and fulfillment.</p><p style="margin-top: 6px; margin-bottom: 0px; display: inline; font-family: inherit;"><a class="_58cn" href="https://www.facebook.com/hashtag/chatgpt?__eep__=6&amp;source=feed_text&amp;epa=HASHTAG" data-ft="{&quot;type&quot;:104,&quot;tn&quot;:&quot;*N&quot;}" style="color: rgb(56, 88, 152); cursor: pointer; font-family: inherit;"><span class="_5afx" style="direction: ltr; unicode-bidi: isolate; font-family: inherit;"><span aria-label="hashtag" class="_58cl _5afz" style="unicode-bidi: isolate; color: rgb(54, 88, 153); font-family: inherit;">#</span><span class="_58cm" style="font-family: inherit;">ChatGPT</span></span></a></p></div><div class="_3x-2" data-ft="{&quot;tn&quot;:&quot;H&quot;}" style="font-family: inherit;"><div data-ft="{&quot;tn&quot;:&quot;H&quot;}" style="font-family: inherit;"><div class="mtm" style="margin-top: 10px; font-family: inherit;"><div class="_2a2q _65sr" style="overflow: hidden; position: relative; margin-left: -12px; margin-right: -12px; font-family: inherit; width: 500px; height: 417px;"><a rel="theater" ajaxify="https://www.facebook.com/photo.php?fbid=10163220804292524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARDGqP1SXr6VpsEHwVjJXIggl-C3wIcOlu5-9eUNm9LV8WhGBXGE21Nh56g4-nSf4QVnLFxB5a_x3-i6&amp;size=1224%2C1224&amp;source=13&amp;player_origin=unknown" data-ploi="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/319316821_3041045526191362_3840468508286522633_n.jpg?_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=36a2c1&amp;_nc_ohc=P1HlTqfAGsIAX8K5mFw&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfAuELBgJU6l4cvqRhmpcXpC64CnASFI7Bmie1s5B8PHXQ&amp;oe=63CE2120" data-plsi="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/319316821_3041045526191362_3840468508286522633_n.jpg?stp=dst-jpg_p960x960&amp;_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=36a2c1&amp;_nc_ohc=P1HlTqfAGsIAX8K5mFw&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfBnVGz5E2YyE9OjBRpONmxNYERdLBtQM2-nzO67iL_NwA&amp;oe=63CE2120" class="_5dec _xcx" href="https://www.facebook.com/photo.php?fbid=10163220804292524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARDGqP1SXr6VpsEHwVjJXIggl-C3wIcOlu5-9eUNm9LV8WhGBXGE21Nh56g4-nSf4QVnLFxB5a_x3-i6" data-render-location="permalink" id="u_0_i_gc" style="color: rgb(56, 88, 152); cursor: pointer; display: block; position: absolute; font-family: inherit; top: 0px; left: 0px; width: 249px; height: 249px;"><div class="uiScaledImageContainer" style="position: relative; overflow: hidden; font-family: inherit; width: 249px; height: 249px;"><img class="scaledImageFitWidth img" src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/319316821_3041045526191362_3840468508286522633_n.jpg?stp=dst-jpg_p526x296&amp;_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=P1HlTqfAGsIAX8K5mFw&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfC1-GCIDoNpyU7elzSfGbQsgJuJZYt92hNn995eKpmGAw&amp;oe=63CE2120" data-src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/319316821_3041045526191362_3840468508286522633_n.jpg?stp=dst-jpg_p526x296&amp;_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=P1HlTqfAGsIAX8K5mFw&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfC1-GCIDoNpyU7elzSfGbQsgJuJZYt92hNn995eKpmGAw&amp;oe=63CE2120" alt="May be an image of 1 person, outdoors and text" width="249" height="249" caption="May be an image of 1 person, outdoors and text" style="height: auto; min-height: initial; position: relative; width: 249px;"></div></a><a rel="theater" ajaxify="https://www.facebook.com/photo.php?fbid=10163220805202524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARDOjeDhobbw2P6shMIwb43-cYvyKvjcRvEPv4IpZoGEKNPCjKE7BaEOw7yef4RzJ5pnh66oz__2kt5-&amp;size=612%2C816&amp;source=13&amp;player_origin=unknown" data-ploi="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/320702606_705008744348260_7362387626096659040_n.jpg?_nc_cat=105&amp;ccb=1-7&amp;_nc_sid=36a2c1&amp;_nc_ohc=_Lcd2qUMpKYAX_dvZ5c&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfC879oBiWkRrrbjAYrwsr97EhHkfv0NugB0Nnm82n1siA&amp;oe=63CDC141" class="_5dec _xcx" href="https://www.facebook.com/photo.php?fbid=10163220805202524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARDOjeDhobbw2P6shMIwb43-cYvyKvjcRvEPv4IpZoGEKNPCjKE7BaEOw7yef4RzJ5pnh66oz__2kt5-" data-render-location="permalink" id="u_0_j_yL" style="color: rgb(56, 88, 152); cursor: pointer; display: block; position: absolute; font-family: inherit; top: 0px; left: 251px; width: 249px; height: 249px;"><div class="uiScaledImageContainer" style="position: relative; overflow: hidden; font-family: inherit; width: 249px; height: 249px;"><img class="scaledImageFitWidth img" src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/320702606_705008744348260_7362387626096659040_n.jpg?stp=dst-jpg_p526x296&amp;_nc_cat=105&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=_Lcd2qUMpKYAX_dvZ5c&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfBNJ6MoHgjkNMRP2y0dWtJTUBPUmv6ARMpgTvgSBfudXg&amp;oe=63CDC141" data-src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/320702606_705008744348260_7362387626096659040_n.jpg?stp=dst-jpg_p526x296&amp;_nc_cat=105&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=_Lcd2qUMpKYAX_dvZ5c&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfBNJ6MoHgjkNMRP2y0dWtJTUBPUmv6ARMpgTvgSBfudXg&amp;oe=63CDC141" alt="May be an image of 1 person, tree and outdoors" width="249" height="332" caption="May be an image of 1 person, tree and outdoors" style="height: auto; min-height: initial; position: relative; width: 249px;"></div></a><a rel="theater" ajaxify="https://www.facebook.com/photo.php?fbid=10163220804627524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARBqeWaT88oEMLoPzCRZ6gaBpa2BFNHA3T_oq8eQ-MhxsArfhcCvmDz7z1nwLP9DUyRWRkfIHxtM6z_m&amp;size=720%2C960&amp;source=13&amp;player_origin=unknown" data-ploi="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/320579028_845022716743239_2596568702770239451_n.jpg?_nc_cat=108&amp;ccb=1-7&amp;_nc_sid=36a2c1&amp;_nc_ohc=9uenjXKD4u4AX_OVAHB&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfAHv2wLbPkgc7RYEc-DmM8UwYn7U2NQavekK8Y82lM_4A&amp;oe=63CCD4AA" class="_5dec _xcx" href="https://www.facebook.com/photo.php?fbid=10163220804627524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARBqeWaT88oEMLoPzCRZ6gaBpa2BFNHA3T_oq8eQ-MhxsArfhcCvmDz7z1nwLP9DUyRWRkfIHxtM6z_m" data-render-location="permalink" id="u_0_k_pN" style="color: rgb(56, 88, 152); cursor: pointer; display: block; position: absolute; font-family: inherit; top: 251px; left: 0px; width: 166px; height: 166px;"><div class="uiScaledImageContainer" style="position: relative; overflow: hidden; font-family: inherit; width: 166px; height: 166px;"><img class="scaledImageFitWidth img" src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/320579028_845022716743239_2596568702770239451_n.jpg?stp=dst-jpg_p350x350&amp;_nc_cat=108&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=9uenjXKD4u4AX_OVAHB&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfACVPdmgGSJKUsKw4sjvezku65fvsOYmXGfaqFrwJfgnw&amp;oe=63CCD4AA" data-src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/320579028_845022716743239_2596568702770239451_n.jpg?stp=dst-jpg_p350x350&amp;_nc_cat=108&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=9uenjXKD4u4AX_OVAHB&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfACVPdmgGSJKUsKw4sjvezku65fvsOYmXGfaqFrwJfgnw&amp;oe=63CCD4AA" alt="May be an image of food and outdoors" width="166" height="222" caption="May be an image of food and outdoors" style="height: auto; min-height: initial; position: relative; width: 166px;"></div></a><a rel="theater" ajaxify="https://www.facebook.com/photo.php?fbid=10163220804897524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARA1Hys6vWMbmDVYbr8_u5Bm9BT8paVIvP8e23W0p2bR0OjkMmuZJtuddWCCi0G2C_9D-nkXVepk7VBj&amp;size=612%2C816&amp;source=13&amp;player_origin=unknown" data-ploi="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/319771629_490914659697507_3243250828830712702_n.jpg?_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=36a2c1&amp;_nc_ohc=u0a3z-539mUAX98Bnds&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfBggwH7SafkpSUrbWghdPdvacXJ0gY_X07RSsvjx1ducA&amp;oe=63CD204D" class="_5dec _xcx" href="https://www.facebook.com/photo.php?fbid=10163220804897524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARA1Hys6vWMbmDVYbr8_u5Bm9BT8paVIvP8e23W0p2bR0OjkMmuZJtuddWCCi0G2C_9D-nkXVepk7VBj" data-render-location="permalink" id="u_0_h_dH" style="color: rgb(56, 88, 152); cursor: pointer; display: block; position: absolute; font-family: inherit; top: 251px; left: 168px; width: 165px; height: 166px;"><div class="uiScaledImageContainer" style="position: relative; overflow: hidden; font-family: inherit; width: 165px; height: 166px;"><img class="scaledImageFitWidth img" src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/319771629_490914659697507_3243250828830712702_n.jpg?stp=dst-jpg_p350x350&amp;_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=u0a3z-539mUAX98Bnds&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfD5xfsNRfQ73o4yRMc42XD5I_5hs1_wZzKMc9AQYso5rQ&amp;oe=63CD204D" data-src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/319771629_490914659697507_3243250828830712702_n.jpg?stp=dst-jpg_p350x350&amp;_nc_cat=110&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=u0a3z-539mUAX98Bnds&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfD5xfsNRfQ73o4yRMc42XD5I_5hs1_wZzKMc9AQYso5rQ&amp;oe=63CD204D" alt="May be an image of 1 person and outdoors" width="165" height="221" caption="May be an image of 1 person and outdoors" style="height: auto; min-height: initial; position: relative; width: 165px;"></div></a><a rel="theater" ajaxify="https://www.facebook.com/photo.php?fbid=10163220804402524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARCXvzqbM303765sdTuZpq3y2JqhjaS4mUrooA14jM4S5hKjinuaiLCl75rmRQmj8fRW2kk86MTJrQxm&amp;size=720%2C480&amp;source=13&amp;player_origin=unknown" data-ploi="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/320589843_1337820197071424_665201545721093224_n.jpg?_nc_cat=103&amp;ccb=1-7&amp;_nc_sid=36a2c1&amp;_nc_ohc=muDrvqjSsNkAX_fE6Xs&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfAGjs8DetDY57-mwmRbpo0HzUIchURJlxshOs7zlEQyXA&amp;oe=63CD937C" class="_5dec _xcx" href="https://www.facebook.com/photo.php?fbid=10163220804402524&amp;set=pcb.10163220813702524&amp;type=3&amp;__tn__=HH-R&amp;eid=ARCXvzqbM303765sdTuZpq3y2JqhjaS4mUrooA14jM4S5hKjinuaiLCl75rmRQmj8fRW2kk86MTJrQxm" data-render-location="permalink" id="u_0_l_6c" style="color: rgb(56, 88, 152); cursor: pointer; display: block; position: absolute; font-family: inherit; top: 251px; left: 335px; width: 165px; height: 166px;"><div class="uiScaledImageContainer" style="position: relative; overflow: hidden; font-family: inherit; width: 165px; height: 166px;"><img class="scaledImageFitHeight img" src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/320589843_1337820197071424_665201545721093224_n.jpg?stp=dst-jpg_p235x350&amp;_nc_cat=103&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=muDrvqjSsNkAX_fE6Xs&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfDR5bmIfLF2UMQfGB7d4pNi8ITMkyjWZuqVdCiJZJAqMw&amp;oe=63CD937C" data-src="https://scontent-lga3-2.xx.fbcdn.net/v/t39.30808-6/320589843_1337820197071424_665201545721093224_n.jpg?stp=dst-jpg_p235x350&amp;_nc_cat=103&amp;ccb=1-7&amp;_nc_sid=110474&amp;_nc_ohc=muDrvqjSsNkAX_fE6Xs&amp;_nc_ht=scontent-lga3-2.xx&amp;oh=00_AfDR5bmIfLF2UMQfGB7d4pNi8ITMkyjWZuqVdCiJZJAqMw&amp;oe=63CD937C" alt="May be an image of animal and outdoors" width="249" height="166" caption="May be an image of animal and outdoors" style="height: 166px; min-height: initial; position: relative; width: auto; left: -41px;"></div><div class="_52d9" style="background-color: rgba(0, 0, 0, 0.4); inset: 0px; color: rgb(255, 255, 255); font-size: 35px; position: absolute; font-family: inherit;"><div class="_52da" style="display: table; height: 166px; width: 165px; font-family: inherit;"><div class="_52db" style="display: table-cell; text-align: center; vertical-align: middle; font-family: inherit;">+31</div></div></div></a></div></div></div></div><div style="font-family: inherit;"></div></div></div><div style="font-family: inherit;"><form rel="async" class="commentable_item collapsed_comments" method="post" data-ft="{&quot;tn&quot;:&quot;]&quot;}" id="u_0_g_Yu" style="margin: 0px; padding: 0px;"><div style="font-family: inherit;"><div style="font-family: inherit;"></div></div><div class="_7f6e" style="border-radius: 0px 0px 3px 3px; color: rgb(28, 30, 33); display: flex; flex-direction: column; font-size: 13px; width: 692px; font-family: inherit;"><div class="_5vsi" style="margin-top: 0px; font-family: inherit;"></div><div class="_7a9u" style="font-family: inherit;"><div class="_68wo" style="position: relative; font-family: inherit;"><div class="_3vum" style="align-items: center; border-bottom: 1px solid rgb(218, 221, 225); color: rgb(96, 103, 112); display: flex; line-height: 20px; margin: 10px 12px 0px; padding: 0px 0px 10px; font-family: inherit;"><div class="_66lg" style="align-items: center; display: flex; flex-grow: 1; overflow: hidden; font-family: inherit;"><span aria-label="See who reacted to this" class="_1n9r _66lh" role="toolbar" style="margin-bottom: -2px; margin-right: 2px; margin-top: -2px; align-items: center; display: flex; font-family: system-ui, -apple-system, &quot;system-ui&quot;, &quot;.SFNSText-Regular&quot;, sans-serif;"><span class="_1n9k" tabindex="-1" data-hover="tooltip" style="background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; border-radius: 12px; display: inline-block; font-size: 11px; line-height: 16px; margin: 0px 0px 0px -2px; outline: none; padding: 2px; position: relative; z-index: 3; font-family: inherit;"><a ajaxify="/ufi/reaction/profile/dialog/?ft_ent_identifier=ZmVlZGJhY2s6MTAxNjMyMjA4MTM3MDI1MjQ%3D&amp;reaction_type=1&amp;av=0" href="https://www.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier=ZmVlZGJhY2s6MTAxNjMyMjA4MTM3MDI1MjQ%3D&amp;av=0" rel="dialog" aria-label="5 Like" class="_1n9l" tabindex="0" role="button" style="color: rgb(56, 88, 152); font-family: inherit;"><i data-visualcompletion="css-img" class="sp_1_kEbr5BZSO_2x sx_e6e274 x1rg5ohu x1n2onr6 xmix8c7 x1xp8n7a x16dsc37" style="background-image: url(&quot;/rsrc.php/v3/yY/r/II0qYWKXcK3.png&quot;); background-size: 97px 1314px; background-repeat: no-repeat; display: inline-block; height: 18px; width: 18px; vertical-align: top; position: relative; background-position: -49px -997px;"></i></a></span><span class="_1n9k" tabindex="-1" data-hover="tooltip" style="background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; border-radius: 12px; display: inline-block; font-size: 11px; line-height: 16px; margin: 0px 0px 0px -4px; outline: none; padding: 2px; position: relative; z-index: 2; font-family: inherit;"><a ajaxify="/ufi/reaction/profile/dialog/?ft_ent_identifier=ZmVlZGJhY2s6MTAxNjMyMjA4MTM3MDI1MjQ%3D&amp;reaction_type=3&amp;av=0" href="https://www.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier=ZmVlZGJhY2s6MTAxNjMyMjA4MTM3MDI1MjQ%3D&amp;av=0" rel="dialog" aria-label="2 Wow" class="_1n9l" tabindex="-1" role="button" style="color: rgb(56, 88, 152); font-family: inherit;"><i data-visualcompletion="css-img" class="sp_1_kEbr5BZSO_2x sx_04582a x1rg5ohu x1n2onr6 xmix8c7 x1xp8n7a x16dsc37" style="background-image: url(&quot;/rsrc.php/v3/yY/r/II0qYWKXcK3.png&quot;); background-size: 97px 1314px; background-repeat: no-repeat; display: inline-block; height: 18px; width: 18px; vertical-align: top; position: relative; background-position: -68px -1035px;"></i></a></span><span class="_1n9k" tabindex="-1" data-hover="tooltip" style="background-image: initial; background-position: initial; background-size: initial; background-repeat: initial; background-attachment: initial; background-origin: initial; background-clip: initial; border-radius: 12px; display: inline-block; font-size: 11px; line-height: 16px; margin: 0px 0px 0px -4px; outline: none; padding: 2px; position: relative; z-index: 1; font-family: inherit;"><a ajaxify="/ufi/reaction/profile/dialog/?ft_ent_identifier=ZmVlZGJhY2s6MTAxNjMyMjA4MTM3MDI1MjQ%3D&amp;reaction_type=2&amp;av=0" href="https://www.facebook.com/ufi/reaction/profile/browser/?ft_ent_identifier=ZmVlZGJhY2s6MTAxNjMyMjA4MTM3MDI1MjQ%3D&amp;av=0" rel="dialog" aria-label="1 Love" class="_1n9l" tabindex="-1" role="button" style="color: rgb(56, 88, 152); font-family: inherit;"><i data-visualcompletion="css-img" class="sp_1_kEbr5BZSO_2x sx_78a873 x1rg5ohu x1n2onr6 xmix8c7 x1xp8n7a x16dsc37" style="background-image: url(&quot;/rsrc.php/v3/yY/r/II0qYWKXcK3.png&quot;); background-size: 97px 1314px; background-repeat: no-repeat; display: inline-block; height: 18px; width: 18px; vertical-align: top; position: relative; background-position: -68px -997px;"></i></a></span></span></div></div></div></div></div></form></div>"""
    print(prettify(s))

try:
    source.close()
except:
    pass
    
try:
    summer.close()
except:
    pass

def CreateDriver(URL,x=0,y=0,width=100, height=2000):
    source = webdriver.Chrome('chromedriver')  ### path of chrome driver should be passed as argument
    source.get(URL) 
    source.set_window_position(x, y, windowHandle='current')
    source.set_window_size(width,height)
    return source
    
interestingPost ='https://www.facebook.com/duen.yen/posts/pfbid02cbGJdA1jvZmviUwLFHpTwSA9w9zv8tFnyJKfaJwZhsW72FYU2v64key428oFDL1Nl'

from pathlib import Path

def getChromes(src=interestingPost):
    print('getting Chromes')
    global source, summer
    source=CreateDriver(src) #default position 
    summerFile= 'file://'+str(Path('summernote.html').absolute())
    summer = CreateDriver(summerFile,500,0,200,2000) #custom position
    ReportsBox.value=''
    return (source, summer)

#source, summer = chromes()

def getSummer():
    js="""
    return $('#summernote').summernote('code')
    """
    #js='alert()'
    ret = summer.execute_script(js)
    return prettify(ret)


def removeAttrs(someHTML):
    soup= BeautifulSoup('<body>' + someHTML)
    for tag in soup():
        for attribute in ["html","body","class", "style", "span", 'data', 'data-ft', 'id']: # You can also add id,style,etc in the list
            del tag[attribute]
    ret = str(soup.prettify())
    for tag in '<html> </html> <body> </body>'.split():
        ret = ret.replace(tag,'')
    return '<style>p {line-height:1.3; </style>\n' + ret

halfwidth = widgets.Layout(height="1000px", width="40%")
    
TESTING = 0
if TESTING:
    source, summer = getChromes()
    stripB=Button(description = 'Strip tags')
    stripB.on_click(onStrip)

    T=Textarea(getSummer(),layout=halfwidth )
    H=HTML(T.value, layout=halfwidth )
    T.observe(update)

    twoButtons = HBox([capB,stripB])
    twoViews=HBox([T,H])
    combo=VBox([twoButtons,twoViews])

    display(twoButtons, twoViews)

def onStrip(e): ######now
    print('onStrip')
    T.value = removeAttrs(T.value)
    #twitchers['Description'].value = removeAttrs(T.value)
    #T.value = twitchers['Description'].value
    #updateHTML('onStrip')

def update(e):
    print('update')
    H.value=T.value

def onNewCap(e):
    global getChromesB
    print('capture Button')
    try:
        T.value = getSummer()
    except:
        ReportsBox.value += '\n restart Chromes first'
        getChromesB.style.button_color = 'lightgreen'

    
def getChromery(T,H):
    global getChromesB, geturlT 
    global source, summer
    #source, summer = getChromes()

    stripB=Button(description = 'Strip tags')
    newCap=Button(description = 'Capture WYSIWYG')

    stripB.on_click(onStrip)    
    newCap.on_click(onNewCap)    

    #T.value=getSummer()
    #H.value = T.value
    #T.observe(update)
    
    sourceURL= interestingPost
    #geturlT.value = sourceURL

    loadB = Button(description = 'Load:')
    loadB.style.button_color='lightblue'
    
    def doLoad(e):
        global ReportsBox
        src=geturlT.value
        print('doLoad', str(e))
        if not validators.url(src):
            print(f'INVALID URL "{src}"')
            return
        try:
            source.get(src)
        except:
            ReportsBox.value='start Chromes first!>>>>'
            getChromesB.style.button_color = 'lightgreen'
            
    loadB.on_click(doLoad)
    

    def chromesGetter(e):
        print('chromesGetter')
        getChromes()

    getChromesB=Button(description = 'restartChromes')
    getChromesB.on_click(chromesGetter)
    getChromesB.style.button_color = 'lightgreen'


    buttonRow = HBox([newCap,stripB, loadB, geturlT, getChromesB])
    combo = VBox([buttonRow])
    return combo

def getLatLon():
    placename=uploadT.value
    get



TESTING=1
if TESTING:
    print('version Tue 24 Jan 2023 10:26  The Row Editor guide is at https://docs.google.com/presentation/d/1MFklijSNKSA-b6I_aksKshn0KDon1LDEEXy5-V3qhZg/edit')
    display(imgUploader)

    display(HBox([Store, Revert, spacer, ImageSourcesBtn, latlon]))      #ImageWidthsBtn REMOVED for the moment
    
    T=bottomPanel.middle
    H=bottomPanel.right
    
    #fromSelenium and Summer
    combo = getChromery(T,H)
    display(HBox([controlBox, newRowBtn,  combo]))
    
    display(msg)

    display(bottomPanel)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:






