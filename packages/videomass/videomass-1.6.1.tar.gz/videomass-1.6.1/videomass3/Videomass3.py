#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#########################################################
# Name: Videomass3.py
# Porpose: bootstrap for the videomass
# Compatibility: Python3, wxPython Phoenix
# Author: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2018/2019 Gianluca Pernigoto <jeanlucperni@gmail.com>
# license: GPL3
# Rev: Dec 27 2018, Aug.28 2019
#########################################################

# This file is part of Videomass.

#    Videomass is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Videomass is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Videomass.  If not, see <http://www.gnu.org/licenses/>.

#########################################################
import wx
import os
from videomass3.vdms_SYS.ctrl_run import system_check
from videomass3.vdms_SYS.appearance import Appearance

# add translation macro to builtin similar to what gettext does
#import locale
import builtins
builtins.__dict__['_'] = wx.GetTranslation
from videomass3.vdms_SYS import app_const as appC

class Videomass(wx.App):
    """
    Before starting the application, check for the essentials
    and send to main frame.
    TODO:Make a logging with python standard library logging
    """
    def __init__(self, redirect=True, filename=None):
        """
        Creating attributes that will be used after in 
        other class with wx.GetApp()
    
        """
        self.DIRconf = None # set pathname folder
        self.FILEconf = None
        self.WORKdir = None
        self.OS = None
        
        print ("App __init__")

        wx.App.__init__(self, redirect, filename) # constructor
    #-------------------------------------------------------------------
        
    def OnInit(self):
        """
        This is a bootstrap interface. The 'setui' calls the function that 
        prepares the environment configuration. The 'setui' take all 
        values of the file configuration.
        
        """
        setui = system_check() # user-space and interface settings
        
        lang = ''
        self.locale = None
        wx.Locale.AddCatalogLookupPathPrefix(setui[5])
        self.updateLanguage(lang)
        
        if setui[2]: # if source /share is missing and videomass is corrupted
            wx.MessageBox(_('Can not find the configuration file\n\n'
                            'Sorry, cannot continue..'),
                             'Videomass: Fatal Error', wx.ICON_STOP)
            print ('Videomass: Fatal Error, file configuration not found')
            return False
        
        icons = Appearance(setui[3], setui[4][12])# set appearance instance
        pathicons = icons.icons_set() # get paths icons
        self.OS = setui[0] # set OS type
        self.FILEconf = setui[6] # set file conf. pathname 
        self.WORKdir = setui[7] # set PWD current dir
        self.DIRconf = setui[8] # set dir conf pathname

        if setui[0] == 'Darwin':
            os.environ["PATH"] += "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
            for link in [setui[4][7],setui[4][9],setui[4][11]]:
                if os.path.isfile("%s" % link):
                    binaries = False
                else:
                    binaries = True
                    break
            if binaries:
                self.firstrun(pathicons[23])
                return True
            else:
                ffmpeg_link = setui[4][7]
                ffprobe_link = setui[4][9]
                ffplay_link = setui[4][11]

        elif setui[0] == 'Windows':
            for link in [setui[4][7],setui[4][9],setui[4][11]]:
                if os.path.isfile("%s" % link):
                    binaries = False
                else:
                    binaries = True
                    break
            if binaries:
                self.firstrun(pathicons[23])
                return True
            else:
                ffmpeg_link = setui[4][7]
                ffprobe_link = setui[4][9]
                ffplay_link = setui[4][11]
                
        else: # is Linux 
            ffmpeg_link = setui[4][7]
            ffprobe_link = setui[4][9]
            ffplay_link = setui[4][11]
            # --- used for debug only ---#
            #self.firstrun(pathicons[23])
            #return True
            
        from videomass3.vdms_MAIN.main_frame import MainFrame
        main_frame = MainFrame(setui, 
                               ffmpeg_link, 
                               ffprobe_link, 
                               ffplay_link,
                               pathicons
                               )
        main_frame.Show()
        self.SetTopWindow(main_frame)
        return True
    #-------------------------------------------------------------------
    
    def firstrun(self, icon):
        """
        Start a temporary dialog: this is showing during first time 
        start the Videomass application on MaOS and Windows.
        """
        from videomass3.vdms_DIALOGS.first_time_start import FirstStart
        main_frame = FirstStart(icon)
        main_frame.Show()
        self.SetTopWindow(main_frame)
        return True
    #------------------------------------------------------------------
    
    def updateLanguage(self, lang):
        """
        Update the language to the requested one.
        
        Make *sure* any existing locale is deleted before the new
        one is created.  The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.
        
        :param string `lang`: one of the supported language codes
        
        """
        # if an unsupported language is requested default to English
        if lang in appC.supLang:
            selLang = appC.supLang[lang]
            #print ('set a custom language: %s' % selLang)
        else:
            selLang = wx.LANGUAGE_DEFAULT
            #print ("Set language default\n%s" % appC.supLang)
        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale
        
        # create a locale object for this language
        self.locale = wx.Locale(selLang)
        if self.locale.IsOk():
            self.locale.AddCatalog(appC.langDomain)
        else:
            self.locale = None
    #-------------------------------------------------------------------

    def OnExit(self):
        """
        """
        print ("OnExit")
        return True
    #-------------------------------------------------------------------    

def main():
    app = Videomass(False)
    #app.MainLoop()
    fred = app.MainLoop()
    print ("after MainLoop", fred)
    

