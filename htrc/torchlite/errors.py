class TorchliteError(Exception):
    """Torchlite error of some kind"""
    pass


class WidgetImplementationError(TorchliteError):
    """Error raised when widget implementation doesn't follow defined guidelines"""
    pass
