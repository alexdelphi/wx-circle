import wx
"""Draw the flower of life"""


class View(wx.Panel):
    def __init__(self, parent):
        super(View, self).__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)

        self.radius = 100

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        w, h = self.GetClientSize()
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 3))
        dc.DrawCircle(w / 2, h / 2, self.radius)


class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('Circle')
        self.width = 400
        self.height = 400
        self.SetClientSize((self.width, self.height))
        self.Center()
        self.view = View(self)

    def on_close(self, event):
        event.Skip()
        self.Destroy()


def main():
    app = wx.App(False)
    frame = Frame()
    app.MainLoop()


if __name__ == '__main__':
    main()
