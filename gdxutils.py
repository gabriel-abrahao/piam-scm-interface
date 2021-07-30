import sys
import os
import shutil
import pymagicc
import pandas as pd


# Import the GAMS API
# #TODO: Use low-level GDX libraries (gdxcc and its python wrapper)
# instead of calling the GAMS API like done here.
# The API is in a folder like '/p/system/packages/gams/35.1.0/apifiles/Python/api_39'
gams_root = os.path.dirname(shutil.which("gams"))
gamsapi_path = os.path.join(gams_root,"apifiles","Python","api_" + str(sys.version_info[0]) + str(sys.version_info[1]))
sys.path.append(gamsapi_path)
sys.path.append(os.path.dirname(gamsapi_path) + "/gams")
from gams import *


def write_gdx_parameter_from_dict(vargamsname, vardict, gamssetname, outfname, vartext = ""):
    """Writes a dict as a single parameter in a new GDX file

    Parameters
    ----------
    vargamsname: str
        GAMS name of the variable
    vardict: dict
        Dictionary containing the values. The keys define a new Set called gamssetname.
    gamssetname: str
        Name of the GAMS Set that will be built from vardict's keys
    outfname: str
        output GDX file name
    vartext: str, default=""
        Optional string describing the variable. 'Explanatory text' in the GAMS documentation.
    """
    # Start GAMS. The working directory is not the same as python's
    ws = GamsWorkspace()

    # so make sure we have an explicit full path
    outfname = os.path.realpath(outfname)

    gdxdb = ws.add_database()

    gamsset = gdxdb.add_set(gamssetname, 1, gamssetname)
    for rec in vardict.keys():
        gamsset.add_record(str(rec))

    gamspar = gdxdb.add_parameter_dc(vargamsname, [gamsset], vartext)
    for rec in vardict.keys():
        gamspar.add_record(str(rec)).value = vardict[rec]

    gdxdb.export(outfname)
    return(None)

def get_variable_dict(results, varname, region = "World"):
    """Gets a year:value dict for a variable from a pymagicc run.
    TODO: Include units check/conversion using the pint backend. 
    REMIND expects the same units as IAMC for surface temperature (K) and radiative forcing (W m-2).

    Parameters
    ----------
    results: scmdata.ScmRun
        Results from a successfully finished SCM run
    varname: str
        Name of the variable to get
    region: str, default="World"
        Region from which to get the variable. Defaults to "World"
    Return
    ------
    vardict: dict
        Dictionary containing year:value pairs of variable `varname` from `results` on `region`
    """
    vardf = results.filter(region = region, variable = varname).to_iamdataframe().swap_time_for_year().as_pandas()
    vardf = vardf[["year","value"]]
    vardict = vardf.set_index("year").to_dict()["value"]
    return(vardict)

def write_gdx_parameter_from_results(varname, vargamsname, results, gamssetname, outfname, region = "World"):
    """Writes a variable from a single region taken from a scmdata.ScmRun object
     as a single parameter in a new GDX file

    Parameters
    ----------
    varname: str
        Name of the variable to get in `results`
    vargamsname: str
        GAMS name to give the variable
    results: scmdata.ScmRun
        Results from a successfully finished SCM run
    gamssetname: str
        Name to give the GAMS Set that will be built from the years
    outfname: str
        output GDX file name
    region: str, default="World"
        Region from which to get the variable. Defaults to "World"
    """
    vardict = get_variable_dict(results, varname, region = region)
    # Use the variable's long name in results as explanatory text
    write_gdx_parameter_from_dict(vargamsname, vardict, gamssetname, outfname, vartext = varname)
    return(None)