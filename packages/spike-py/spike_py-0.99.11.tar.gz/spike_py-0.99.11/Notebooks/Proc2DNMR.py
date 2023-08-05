#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Initialization" data-toc-modified-id="Initialization-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Initialization</a></span><ul class="toc-item"><li><span><a href="#Choose-the-file" data-toc-modified-id="Choose-the-file-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Choose the file</a></span></li><li><span><a href="#Import-dataset" data-toc-modified-id="Import-dataset-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Import dataset</a></span></li></ul></li><li><span><a href="#Basic-Processing" data-toc-modified-id="Basic-Processing-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Basic Processing</a></span><ul class="toc-item"><li><span><a href="#Fourier-Transform---modulus-mode!" data-toc-modified-id="Fourier-Transform---modulus-mode!-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Fourier Transform - modulus mode!</a></span></li><li><span><a href="#Advanced-Phase-sensitive-processing" data-toc-modified-id="Advanced-Phase-sensitive-processing-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Advanced Phase sensitive processing</a></span></li><li><span><a href="#Rephasing" data-toc-modified-id="Rephasing-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Rephasing</a></span></li></ul></li><li><span><a href="#Peak-Picker" data-toc-modified-id="Peak-Picker-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Peak-Picker</a></span></li><li><span><a href="#Save-the-data-set" data-toc-modified-id="Save-the-data-set-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Save the data-set</a></span></li><li><span><a href="#Export-a-bucket-list" data-toc-modified-id="Export-a-bucket-list-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Export a bucket list</a></span></li></ul></div>

# ** *This notebook is unfinished and still under development* **
# 
# # 2D NMR Processing and Display
# 
# a simplified environment for processing 2D Bruker NMR datasets with `SPIKE`.
# 
# Run each python cell in sequence by using the ⇥Run button above (or typing *shift* Enter).
# 
# Cells are meant to be used in order, taking you to the complete analysis, but you can go back at any time.
# 
# The SPIKE code used for processing is visible in the cells, and can be used as a minimal tutorial.
# 
# ***Remark*** *to use this program, you should have installed the following packages:*
# 
# - *a complete scientific python environment* ( *tested with python 3.6 - [anaconda](https://www.anaconda.com/) 
#  but it should also work in python 2.7*)
# - [`spike`](https://www.bitbucket.org/delsuc/spike) ( *version 0.99.9 minimum* )
# - [`ipywidgets`](https://ipywidgets.readthedocs.io/en/latest/)  ( *tested with version 7.1* )
# 
# ## Initialization
# the following cell should be run only once, at the beginning of the processing

# In[1]:


# load all python and interactive tools
from __future__ import print_function, division
from IPython.display import display, HTML, Markdown, Image
display(Markdown('## STARTING Environment...'))
get_ipython().run_line_magic('matplotlib', 'notebook')
import os.path as op
import spike
from spike.File.BrukerNMR import Import_2D
from spike.Interactive import INTER as I
from spike.Interactive.ipyfilechooser import FileChooser
display(Markdown('## ...program is Ready'))
I.hidecode()


# ### Choose the file
# The `FileChooser()` tool creates a dialog box which allows to choose a file on your disk
# 
# - use the `Select` button
# - modify the ( *optional* ) `path` argument, to start the exploration on a given location
# - After the selection, the selected filename is found in `FC.selected`

# In[2]:


FC = FileChooser(path='/DATA/PFDA_190625_6/capucine/',filename='ser')
display(FC)


# ### Import dataset
# 
# This is simply done with the `Import_2D()` tool, which returns a `SPIKE` object.
# 
# We store the dataset into a variable, typing the variable name shows a summary of the dataset. 

# In[3]:


print('Reading file ',FC.selected)
d2 = Import_2D(FC.selected)
d2.filename = FC.selected
d2.pulprog = d2.params['acqu']['$PULPROG']
print (d2.params['acqu']['title'])
d2.set_unit('sec').display(title="%s %s"%(FC.nmrname,d2.pulprog), scale='auto')


# In the current set-up, the figure can be explored *(zoom, shift, resize, etc)* with the jupyter tools displayed  below the dataset.
# The figure can also be saved as a `png` graphic file.
# 
# At anytime, the figure can be frozen by clicking on the blue button on the upper right corner, just rerun the cell to make it interactive again.
# 
# ## Basic Processing
# We are going to use a basic processing set-up, check the documentation for advanced processing
# 
# ### Fourier Transform - modulus mode!

# In[6]:


D2 = d2.copy() # copy the imported data-set to another object for processing
# bk_ftF2 and bk_ftF1 (define in the Bruker plugin) find which FT to apply depending on FnMODE
D2.apod_sin(maxi=0.5,axis='F2').zf(1,2).bk_ftF2()  # chaining  apodisation - zerofill - FT
D2.apod_sin(maxi=0.5,axis='F1').zf(2,1).bk_ftF1()  # chaining  apodisation - zerofill - FT
D2.modulus().set_unit('ppm').rem_ridge()
D2.display(scale="auto", autoscalethresh=6.0, title="%s %s"%(FC.nmrname,d2.pulprog))  # chain  set to ppm unit - and display


# ### Advanced Phase sensitive processing
# 
# 

# In[7]:


D2 = d2.copy() # copy the imported data-set to another object for processing
# bk_ftF2 and bk_ftF1 (define in the Bruker plugin) find which FT to apply depending on FnMODE
D2.apod_sin(maxi=0,axis='F2').zf(1,2).bk_ftF2().bk_pk()  # chaining  apodisation - zerofill - FT - phase
D2.apod_sin(maxi=0,axis='F1').zf(2,1).bk_ftF1()  # chaining  apodisation - zerofill - FT
D2.set_unit('ppm').rem_ridge()
D2.display(scale="auto",  autoscalethresh=6.0, title="%s %s"%(FC.nmrname,d2.pulprog))  # chain  set to ppm unit - and display


# ### Rephasing

# In[8]:


from importlib import reload
reload(I)
I.Phaser2D(D2)


# # An interactive Display

# In[10]:


from importlib import reload
reload(I)
I.Show2D(D2, title="%s %s"%(FC.nmrname,d2.pulprog))


# # The following entries or not finished yet

# ## Peak-Picker
# - moving the threshold determines the minimum peak intensity
# - peaks are searched only in the selected zoom window

# ## Save the data-set
# either as stand alone native SPIKE files, (there are other formats)

# In[13]:


D2.save('example1.gs2')


# ## Export a bucket list

# In[16]:


# adapt the parameters below
Zoom = ((0.5,8),(0.5,8))                    # zone to bucket       - in ppm
BucketSize = (0.1,0.1)                 # width of the buckets - in ppm
Output = 'screen'                   # 'screen'  or  'file'  determines output
BucketFileName = 'bucket.csv'     #  the filename if Output (above) is 'file'  - don't forget the .csv extension.


# In[18]:


# the following cell executes the bucketing
if Output == 'file':
    with open(BucketFileName,'w') as F:
        D2.bucket2d(zoom=Zoom, bsize=BucketSize, file=F)
    print('buckets written to %s\n'%op.realpath(BucketFileName))
else:
    D2.bucket2d(zoom=Zoom, bsize=BucketSize)


# *Tools in this page is under intensive development - things are going to change rapidly.*
