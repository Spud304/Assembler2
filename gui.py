import os
import wx

class MyPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.my_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        btn = wx.Button(self, label='Open Text File')
        btn.Bind(wx.EVT_BUTTON, self.onOpen)

        save = wx.Button(self, label='Save as .Hack')
        save.Bind(wx.EVT_BUTTON, self.OnSaveAs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.my_text, 1, wx.ALL|wx.EXPAND)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        sizer.Add(save, 0, wx.ALL|wx.CENTER, 5)

        self.SetSizer(sizer)

    def OnSaveAs(self, event):
        with wx.FileDialog(self, "Save .hack file", wildcard="XYZ files (*.hack)|*.hack",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.doSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def onOpen(self, event):
        wildcard = "ASM files (*.asm)|*.asm"
        dialog = wx.FileDialog(self, "Open ASM Files", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()

        if os.path.exists(path):
            with open(path) as fobj:
                for line in fobj:
                    self.my_text.WriteText(line)


class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title='Assembler')

        panel = MyPanel(self)

        self.Show()