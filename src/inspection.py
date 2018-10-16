"""
Inspection utilities
"""
import wx
import wx.lib.mixins.inspection
import typing


class InspectionApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    """
    Optional class to be used instead of wx.App
    Example:
        app: wx.App = inspection.InspectionApp(lambda: Frame())
        app.MainLoop()
    """
    def __init__(self, frame_init: typing.Callable[[], wx.Frame]):
        """
        A constructor to "parameterize" the app
        :param frame_init: a callable to initialize the contents
        """
        self.frame_init: typing.Callable[[], wx.Frame] = frame_init
        super().__init__()

    def OnInit(self):
        self.Init()  # initialize the inspection tool
        frame: wx.Frame = self.frame_init()
        self.SetTopWindow(frame)
        frame.Show()
        return True
