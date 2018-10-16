"""Draw overlapping circles"""
import wx
import typing
import inspection


class Canvas(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.SetMinSize(wx.Size(__class__.width(), __class__.height()))

    # Constants
    @staticmethod
    def width():
        return 400

    @staticmethod
    def height():
        return 400

    @staticmethod
    def radius():
        return 100

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.DrawCircle(__class__.width() / 2, __class__.height() / 2, __class__.radius())


class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('Overlapping circles pattern')
        self.Center()
        self.on_load()

    def on_load(self) -> None:
        """Initialize the interface"""
        main_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)

        # Top controls
        header_panel: wx.Panel = wx.Panel(self)
        header_panel.SetSizer(self._top_controls(header_panel))
        main_sizer.Add(header_panel, wx.SizerFlags()
                       .Align(wx.ALIGN_TOP | wx.EXPAND))

        # Bottom: drawing canvas
        canvas_sizer: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        canvas_sizer.Add(Canvas(self), wx.SizerFlags().Align(wx.EXPAND))
        main_sizer.Add(canvas_sizer, wx.SizerFlags().Align(wx.EXPAND))
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

    def _top_controls(self, parent: wx.Panel) -> wx.GridBagSizer:
        """
        Initialize the main panel and all its children.
        TODO: none of the controls change their sizes when resizing the window
        :returns The result (the BoxSizer grid), should be attached back to the panel
        """
        sizer_vgap, sizer_hgap = 10, 5
        sizer: wx.GridBagSizer = wx.GridBagSizer(sizer_vgap, sizer_hgap)
        # Style for the text boxes
        label_style = wx.ALIGN_LEFT | wx.ST_ELLIPSIZE_END
        for pos, name in enumerate(['Size:', 'Radius:']):
            label_size: wx.StaticText = wx.StaticText(parent, label=name, style=label_style)
            # A new sizer for our label to help it center normally
            help_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
            help_sizer.Add(label_size, wx.SizerFlags(1).Expand().Border(wx.ALL, 5))
            sizer.Add(help_sizer,
                      wx.GBPosition(pos, 0),
                      flag=wx.EXPAND,
                      border=10)

        # Text controls
        self.text_ctrl_size = self._add_text_ctrl(parent, self.on_text_ctrl_size_enter)
        self.text_ctrl_radius = self._add_text_ctrl(parent, self.on_text_ctrl_radius_enter)
        for pos, ctrl in enumerate([self.text_ctrl_size, self.text_ctrl_radius]):
            sizer.Add(ctrl, wx.GBPosition(pos, 1), flag=wx.EXPAND, border=10)

        # Draw button
        button_draw: wx.Button = wx.Button(parent, label='Draw')
        button_draw.Bind(wx.EVT_BUTTON, self.draw_canvas)
        button_sizer: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)  # A sizer to hold the button itself
        button_sizer.Add(button_draw, wx.SizerFlags(1).Center())
        button_grid_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)  # A sizer to occupy the 2 grid columns
        button_grid_sizer.Add(button_sizer, wx.SizerFlags(1).Expand())
        sizer.Add(button_grid_sizer, wx.GBPosition(0, 2), wx.GBSpan(2, 1), flag=wx.EXPAND, border=10)
        return sizer

    def on_close(self, event) -> None:
        event.Skip()
        self.Destroy()

    def on_text_ctrl_size_enter(self, event) -> None:
        print('Entered size: {}'.format(self.text_ctrl_size.GetValue()))

    def on_text_ctrl_radius_enter(self, event) -> None:
        print('Entered radius: {}'.format(self.text_ctrl_radius.GetValue()))

    def draw_canvas(self, event) -> None:
        pass


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
