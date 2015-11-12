# This handles lots of the abstraction used in the main program.
# Most things in here will be fairly self explanatory.
# Even lower-level abstraction is found in dialogs.py which sets bare layout of input boxes etc.

import wx
import dialogs
import cStringIO as StringIO
import cPickle as pickle

class DisplayAPI:
    
    text_font = None
    frame = None
    menus = None
    children = []
    
    def __init__(self, frame):
        self.frame = frame
        self.menus = []
        
    def add_menu_item(self, menu = '&Ciphers', caption = 'Untitled', function = (lambda(self): None), wx_id = wx.ID_ANY):
        item = None
        for title, menu_object in self.menus:
            if title == menu:
                item = menu_object.Append(wx_id, caption)
                break
        def wrapper(self, event = None):
            return function()
        self.frame.Bind(wx.EVT_MENU, wrapper, item)
        return item
    
    def add_menu(self, menu = 'New Menu'):
        self.menus.append((menu, wx.Menu()))
    
    def key_dialog(self, radioboxes = [], textboxes = [], title = 'Key', font = None):
        if font is None:
            font = self.text_font
        dialog = dialogs.InputDialog(None, radioboxes, textboxes, title, font = font)
        retval = dialog.ShowModal()
        if retval != wx.ID_OK:
            dialog.Destroy()
            return ([None], [None])
        rvalues, tvalues = dialog.get_values()
        dialog.Destroy()
        return rvalues, tvalues
    
    def get_input(self):
        return self.frame.cipher_text.GetValue()
    
    def get_output(self):
        return self.frame.plain_text.GetValue()
    
    def show_output(self, _output):
        self.frame.plain_text.SetValue(_output)
    
    def show_input(self, _input):
        self.frame.cipher_text.SetValue(_input)
        
    def show_image(self, image_data, title = 'Image', size = None, scale = False):
        stream = StringIO.StringIO(image_data)
        dialog = dialogs.ImageDialog(self.frame, stream, title, size = size, scale = scale)
        dialog.Show()
        self.children.append(dialog)
    
    def error_dialog(self, text, title = 'Error'):
        error_diag = wx.MessageDialog(self.frame, text, title, style = wx.OK|wx.ICON_ERROR)
        error_diag.ShowModal()
    
    def clear_children(self):
        for child in self.children:
            try:
                child.Destroy()
            except wx._core.PyDeadObjectError:
                pass
        self.children = []
    
    def reset_all(self):
        self.clear_children()
        self.frame.cipher_text.SetValue('')
        self.frame.plain_text.SetValue('')
    
    def swap_in(self):
        out = self.get_output()
        self.show_input(out)
        self.show_output('')

    def save(self):
        filters = 'ULTRA file (*.ultra)|*.ultra|All files (*.*)|*.*'
        save_diag = wx.FileDialog(None, style=wx.SAVE | wx.OVERWRITE_PROMPT, wildcard = filters)
        if save_diag.ShowModal() == wx.ID_OK:
            path = save_diag.GetPath()
            ciphertext = self.frame.cipher_text.GetValue()
            plaintext = self.frame.plain_text.GetValue()
            with open(path, 'w') as save_file:
                pickle.dump((ciphertext, plaintext), save_file)
            save_file.close()
        save_diag.Destroy()
        
    def open(self):
        filters = 'ULTRA file (*.ultra)|*.ultra|All files (*.*)|*.*'
        open_diag = wx.FileDialog(None, style=wx.OPEN, wildcard = filters)
        if open_diag.ShowModal() == wx.ID_OK:
            path = open_diag.GetPath()
            with open(path, 'r') as save_file:
                ciphertext, plaintext = pickle.load(save_file)
            save_file.close()
            self.frame.cipher_text.SetValue(ciphertext)
            self.frame.plain_text.SetValue(plaintext)
        open_diag.Destroy()
        
    def churn_dialog(self):
        churn_diag = dialogs.ChurnDialog(self.frame)
        if churn_diag.ShowModal() == wx.ID_OK:
            churn_diag.Destroy()
            return
    
