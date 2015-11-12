#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# ULTRA
# LIKE
# TOTALLY
# RADICAL
# AWESOME
# 
# DAMN STRAIGHT

import wx
import cipher
import displayapi
import pdb
import cipher.config as config

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(640,480))
        # DisplayAPI abstraction
        self.display = displayapi.DisplayAPI(self)
        
        # Menus and event handlers
        menubar = wx.MenuBar()
        
        # Tuply menu abstraction thingie
        menu_layout = [
            ('&File', 
                [
                    ('&Save As', self.display.save, wx.ID_SAVE),
                    ('&Open', self.display.open, wx.ID_OPEN),
                    ('&Quit', self.quit, wx.ID_EXIT)
                ]
            ),
            ('&Text Operations', []),
            ('&Ciphers', []),
            ('&Solve', []),
            ('&Analysis', []),
            ('&Help',
                [
                    ('&About', self.about, wx.ID_ABOUT)
                ]
            )
        ]
        
        # Deal with the menu
        for title, items in menu_layout:
            self.display.add_menu(title)
            for caption, function, wx_id in items:
                self.display.add_menu_item(menu = title, caption = caption, function = function, wx_id = wx_id)
        
        # If you make a new cipher class, gotta add it in here
        ciphers = [
            cipher.caesar.Caesar(self.display),
            cipher.affine.Affine(self.display),
            cipher.monoalphabetic.Monoalphabetic(self.display),
            cipher.transposition.Transposition(self.display),
            cipher.vigenere.Vigenere(self.display),
            cipher.porta.Porta(self.display),
            cipher.adfgvx.ADFGVX(self.display),
            cipher.hill.Hill(self.display),
            cipher.playfair.Playfair(self.display)
        ]
        
        # Likewise
        analyses = [
            cipher.frequencies.Frequencies(self.display),
            cipher.autocorrelation.AutoCorrelation(self.display),
            cipher.digraphs.Digraphs(self.display)
        ]
        
        textops = cipher.textops.textops(self.display)
        
        for caption, menu in self.display.menus:
            menubar.Append(menu, caption)

        self.SetMenuBar(menubar)
        
        #Controls
        self.cipher_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.plain_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        clear_dialogs = wx.Button(self, label = 'Clear windows')
        reset_all = wx.Button(self, label = 'Reset all')
        swap_in = wx.Button(self, label = 'Use output as new input')
        
        #Fonts
        self.display.text_font = self.plain_text.GetFont()
        self.display.text_font.SetFaceName('Monospace')
        self.plain_text.SetFont(self.display.text_font)
        self.cipher_text.SetFont(self.display.text_font)
        
        #Sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.cipher_text, 1, wx.EXPAND)
        self.sizer.Add(self.plain_text, 1, wx.EXPAND)
        self.bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bottom_sizer.Add(swap_in)
        self.bottom_sizer.Add(reset_all)
        self.bottom_sizer.Add(clear_dialogs)
        self.sizer.Add(self.bottom_sizer, 0, wx.ALIGN_RIGHT)
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        
        self.cipher_text.SetFocus()
        
        #Event handlers
        self.Bind(wx.EVT_BUTTON, self.swap_in, swap_in)
        self.Bind(wx.EVT_BUTTON, self.clear_dialogs, clear_dialogs)
        self.Bind(wx.EVT_BUTTON, self.reset_all, reset_all)
        #Gogogo!
        self.Show(True)
    
    # Move the contents of the output textbox to the input textbox for reuse.
    def swap_in(self, event = None):
        self.display.swap_in()
    
    # We generate lots of useful things in seperate windows, so this clears them up.
    def clear_dialogs(self, event = None):
        self.display.clear_children()
        
    # Fairly obvious
    def reset_all(self, event = None):
        self.display.reset_all()
        
    def about(self, event=None):
        wx.MessageBox('ULTRA: Like Totally Radical Awesome\n\n By Joe MacMahon and Ben Ward', 'About')    
            
    def quit(self, event=None):
        self.Close()
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(0)
    frame = MainFrame(None, 'ULTRA Cipher Tool')
    app.MainLoop()
