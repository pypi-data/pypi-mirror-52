import pandas as pd

def get_extension(file=None):
    """returns file extension"""
    ext = file.split(".")
    if len(ext)> 1:
        return ext[-1]
    return None

def file_extentions():
    """returns dict of file types"""
    return {'blob': ['csv', 'txt', 'json'],
            'matrix': ['xls', 'xlsx']}

def ext_handler(handler):
    """receives an extension argument
    and returns a pandas object handler"""
    ext = {'csv': pd.read_csv,
            'xls': pd.read_excel,
            'xlsx': pd.read_excel,
            'txt': pd.read_csv,
            'json': pd.read_json}
    return ext.get(handler)