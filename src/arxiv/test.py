#%%
import re

#%%
line = "follow the $\\chi^2$ distribution so that the threshold values can be easily calibrated from this distribution"
re.sub(r"(\${1,2})(?:(?!\1)[\s\S])*\1", '', line)
# %%
