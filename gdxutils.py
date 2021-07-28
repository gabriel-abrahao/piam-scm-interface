import sys
import os
import pymagicc
import pandas as pd


# #TODO: Use low-level GDX libraries (gdxcc and its python wrapper)
# instead of calling the GAMS API like done here. Also check the environment
# for Python and GAMS versions/locations
gamsapi_path = '/p/system/packages/gams/35.1.0/apifiles/Python/api_39'
sys.path.append(gamsapi_path)
sys.path.append(os.path.dirname(gamsapi_path) + "/gams")
from gams import *


# TODO: Define functions in another file
# Writes a dict as a single parameter in a new GDX file
# vargamsname:
#   GAMS name of the variable
# vardict:
#   dictionary with the values. The keys define a new Set called gamssetname
# vartext:
#   explanatory text (optional)
# gamssetname:
#   name of the GAMS Set that will be built from vardict's keys
# outfname:
#   output GDX file name
def write_gdx_parameter_from_dict(vargamsname, vardict, gamssetname, outfname, vartext = ""):
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

# Gets a year:value dict for a variable from a pymagicc run
# results:
#   The pymagicc model object after being run
# varname:
#   The IAMC variable name (e.g. 'Surface Temperature')
# region:
#   Region to extract, defaults to 'World'
# TODO: Include units check/conversion using the pint backend. 
# REMIND expects the same units as IAMC for surface temperature (K) and radiative forcing (W m-2)
def get_variable_dict(results, varname, region = "World"):
    vardf = results.filter(region = region, variable = varname).to_iamdataframe().swap_time_for_year().as_pandas()
    vardf = vardf[["year","value"]]
    vardict = vardf.set_index("year").to_dict()["value"]
    return(vardict)

# Writes a dict as a single parameter in a new GDX file
# vargamsname:
#   GAMS name of the variable
# results:
#   The pymagicc model object after being run
# gamssetname:
#   name of the GAMS Set that will be built from vardict's keys
# outfname:
#   output GDX file name
# varname:
#   The IAMC variable name (e.g. 'Surface Temperature')
# region:
#   Region to extract, defaults to 'World'
def write_gdx_parameter_from_results(varname, vargamsname, results, gamssetname, outfname, region = "World"):
    vardict = get_variable_dict(results, varname, region = region)
    write_gdx_parameter_from_dict(vargamsname, vardict, gamssetname, outfname, vartext = varname)
    return(None)