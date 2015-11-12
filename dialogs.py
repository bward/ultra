import wx
import os

class InputDialog(wx.Dialog):
    def __init__(self, parent, radioboxes, textboxes, title, font):
        wx.Dialog.__init__(self, parent, title=title)
        #Sizers
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        #Controls
        self.labels = []
        self.tboxes = []
        self.rboxes = []
        self.sizers = []
        
        for radiobox in radioboxes:
            self.rboxes.append(wx.RadioBox(self, choices = radiobox))
            self.sizers.append(wx.BoxSizer(wx.HORIZONTAL))
            self.sizers[-1].Add(self.rboxes[-1], 1, wx.EXPAND)
            self.mainSizer.Add(self.sizers[-1], 1, wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND, border = 5)
        
        for textbox in textboxes:
            self.labels.append(wx.StaticText(self, wx.ID_ANY, textbox[0]))
            self.tboxes.append(wx.TextCtrl(self))
            self.tboxes[-1].SetValue(textbox[1])
            self.tboxes[-1].SetFont(font)
            self.sizers.append(wx.BoxSizer(wx.HORIZONTAL))
            self.sizers[-1].Add(self.labels[-1], 1)
            self.sizers[-1].Add(self.tboxes[-1], 1)
            self.mainSizer.Add(self.sizers[-1], 1, wx.ALL, 5)
        
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, wx.ID_OK, label='OK')
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, label='Cancel')
        self.button_sizer.Add(self.ok_button, 1)
        self.button_sizer.Add(self.cancel_button, 1)
        
        self.mainSizer.Add(self.button_sizer, 1, wx.ALL, 5)
        self.mainSizer.Fit(self)
        self.SetSizer(self.mainSizer)
        
        try:
            self.tboxes[0].SetFocus()
        except IndexError:
            try:
                self.rboxes[0].SetFocus()
            except IndexError:
                pass
        
    def get_values(self):
        tvalues = []
        rvalues = []
        for radiobox in self.rboxes:
            rvalues.append(radiobox.GetSelection())
        for textbox in self.tboxes:
            tvalues.append(textbox.GetValue())
        return rvalues, tvalues
    
class ImageDialog(wx.Frame):
    bmp = None
    
    def __init__(self, parent, stream, title, size = None, scale = False):
        image = wx.ImageFromStream(stream, wx.BITMAP_TYPE_ANY)
        if size == None:
            size = (image.GetWidth(), image.GetHeight())
        width, height = size
        if scale:
            image.Rescale(width, height)
        if os.name == 'nt': # Windows fail at drawing shit JOE - This still doesn't work :P. Love Ben. xx
            # Should work now... test it on your computer then delete these comments.
            width = width + 15
            height = height + 35
        wx.Frame.__init__(self, parent, title=title, size = (width, height))
        self.Bind(wx.EVT_SIZE, self.draw, self)
        self.bmp = wx.BitmapFromImage(image)
        self.draw()
        
    def draw(self, event = None):
        wx.StaticBitmap(self, -1, self.bmp)

# For the Churn algorithm
class ChurnDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Churning")
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.stop_button = wx.Button(self, wx.ID_OK, label='Stop Churning')
        self.sizer.Add(self.stop_button, 0, wx.EXPAND)
        self.sizer.Fit(self)
        self.SetSizer(self.sizer)

