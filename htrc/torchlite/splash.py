import datetime
year = datetime.datetime.utcnow().year

__splash = """
_|_|_|_|_|    _|_|    _|_|_|      _|_|_|  _|    _|  _|        _|_|_|  _|_|_|_|_|  _|_|_|_|  
    _|      _|    _|  _|    _|  _|        _|    _|  _|          _|        _|      _|        
    _|      _|    _|  _|_|_|    _|        _|_|_|_|  _|          _|        _|      _|_|_|    
    _|      _|    _|  _|    _|  _|        _|    _|  _|          _|        _|      _|        
    _|        _|_|    _|    _|    _|_|_|  _|    _|  _|_|_|_|  _|_|_|      _|      _|_|_|_|  
"""
__splash_footer = "{:-^90s}".format(" Built with ♡ at HathiTrust Research Center (%d) " % year)


def print_splash() -> None:
    print(__splash)
    print(__splash_footer)
