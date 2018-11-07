"""
Draw overlapping circles
TODO refactor using variable sizes for drawing but not _less_ than 400x400 -> implicit radius
"""
import wx
import typing
import inspection


class Canvas(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        # self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetMinSize(wx.Size(__class__.width(), __class__.height()))
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)

    # Constants
    @staticmethod
    def width():
        return 330

    @staticmethod
    def height():
        return 330

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.DrawCircle(__class__.width() / 2, __class__.height() / 2, 100)


class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None)
        self.title = 'Overlapping circles pattern'
        self.SetTitle(self.title)
        self.Center()
        self._init_gui()

    def _init_gui(self) -> None:
        """Initialize the interface"""
        main_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)

        # Top controls
        header_panel: wx.Panel = wx.Panel(self)
        header_panel.SetSizer(self._top_controls(header_panel))
        main_sizer.Add(header_panel, wx.SizerFlags()
                       .Align(wx.ALIGN_TOP | wx.EXPAND))

        # Bottom: drawing canvas
        main_sizer.Add(Canvas(self), wx.SizerFlags(1).Align(wx.EXPAND))
        self.SetSizerAndFit(main_sizer)

        # Fix widths or else header_sizer will show the wrong distance
        _, header_height = header_panel.GetEffectiveMinSize()
        header_panel.SetMinSize(wx.Size(Canvas.width(), header_height))
        header_panel.Layout()

    def _add_text_ctrl(self, parent, edit_handler: typing.Callable) -> wx.SpinCtrl:
        spin_style = wx.SP_VERTICAL | wx.SP_ARROW_KEYS | wx.SP_WRAP
        ctrl: wx.SpinCtrl = wx.SpinCtrl(parent, min=2, max=10, initial=3, style=spin_style)
        ctrl.Bind(wx.EVT_TEXT, edit_handler)
        ctrl.Bind(wx.EVT_SPIN, edit_handler)
        return ctrl

    def _top_controls(self, parent: wx.Panel) -> wx.BoxSizer:
        """
        Initialize the main panel and all its children.
        :returns The result (the BoxSizer grid), should be attached back to the panel
        """
        border = 10
        sizer: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddSpacer(border)
        # Style for the text boxes
        label_style = wx.ALIGN_LEFT | wx.ST_ELLIPSIZE_END
        label_size: wx.StaticText = wx.StaticText(parent, label='Size:', style=label_style)
        # A new sizer for our label to help it center normally
        help_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        help_sizer.Add(label_size, wx.SizerFlags())
        sizer.Add(help_sizer, wx.SizerFlags().Center())
        sizer.AddSpacer(border)

        # Text controls
        self.text_ctrl_size = self._add_text_ctrl(parent, self.on_text_ctrl_size_enter)
        sizer.Add(self.text_ctrl_size, wx.SizerFlags(1).Expand())
        sizer.AddSpacer(border)
        # Draw button
        button_draw: wx.Button = wx.Button(parent, label='Draw')
        button_draw.Bind(wx.EVT_BUTTON, self.draw_canvas)
        button_grid_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)  # A sizer to occupy the 2 grid columns
        button_grid_sizer.Add(button_draw, wx.SizerFlags().Expand())
        sizer.Add(button_grid_sizer, wx.SizerFlags(1).Expand())
        sizer.AddSpacer(border)

        # Frame sizer: adding vertical borders
        sizer_frame: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        sizer_frame.AddSpacer(border)
        sizer_frame.Add(sizer, wx.SizerFlags(1).Expand())
        sizer_frame.AddSpacer(border)
        return sizer_frame

    def on_close(self, event) -> None:
        event.Skip()
        self.Destroy()

    def on_text_ctrl_size_enter(self, _) -> None:
        print('Entered size: {}'.format(self.text_ctrl_size.GetValue()))

    def on_text_ctrl_radius_enter(self, _) -> None:
        print('Entered radius: {}'.format(self.text_ctrl_radius.GetValue()))

    def draw_canvas(self, _) -> None:
        dlg: wx.MessageDialog = wx.MessageDialog(self, 'Not implemented yet', caption=self.title, style=wx.OK)

        dlg.ShowModal()


def main() -> None:
    """Entry point"""
    app: wx.App = inspection.InspectionApp(lambda: Frame())
    app.MainLoop()
    """
    app = wx.App(False)
    frame = Frame()
    frame.Show()
    app.MainLoop()
    """


if __name__ == '__main__':
    main()
