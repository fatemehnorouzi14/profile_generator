import os

import pandas as pd
from PIL import Image


def PathToResource(filename = None):
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    pathToResourcefolderwithFileNameIfSpecified = os.path.join(parent_path,'resources')
    if filename != None:
        return os.path.join(pathToResourcefolderwithFileNameIfSpecified,filename)
    else:
        return pathToResourcefolderwithFileNameIfSpecified


def readCSVasDataFrame(filename) :
    df = pd.read_csv(PathToResource(filename))
    return df

def readImage(filename) -> Image:
    resourcePath = PathToResource (filename)
    image = Image.open(resourcePath)
    return image