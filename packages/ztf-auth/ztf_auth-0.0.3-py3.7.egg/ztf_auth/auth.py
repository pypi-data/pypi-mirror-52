"""
Basic module to deal with authentication for ZTF
"""
__all__ = ['get_ztf_auth']

import json
import os


def get_ztf_auth(authfilename='ztffps_auth.json', ztfdir=None):
    """
    reads authorization file at ${HOME}/.ztf/ztf/authfilename for a JSON file
    to obtain a dictionary of `username`, `password` and `email`
    
    Parameters
    ----------
    authfilename: string, defaults to 'ztffps_auth'
        filename of JSON authorization file to use in `ztfdir`
   
    ztfdir: string, defaults to None
        if `None`, the default `ztfdir` is `${HOME}/.ztf/`. This can be changed
        by providing an explicit absolute path to a directory.
    Returns
    -------
    mydict:  dictionary with keys `username`, `password` and `email`
    """
    # Set the default ztfdir
    if ztfdir is None:
        home = os.environ.get('HOME')
        ztfdir =  os.path.join(home, '.ztf')
    fname = os.path.join(ztfdir, authfilename)
    with open(fname, 'r') as fh:
        mydict = json.load(fh)
    return mydict
