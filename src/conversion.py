# conversion.py
"""
Module that convert RGB images to grayscale by:
- Replicating G band in B and R 
- Replicating the Y band of the YIQ system in R, G, and B 
"""

import numpy as np

def replicate_g(
    channelR, channelG, channelB,
):
    """
    Replicate G band in B and R
    Returns R, G, B results.
    """
    outR = channelG
    outG = channelG
    outB = channelG

    return outR, outG, outB

def replicate_y(
    channelR, channelG, channelB,    
):
    """
    Convert RGB to YIQ system
    Replicate Y band in R, G and B
    Returns R, G, B results.
    """

    channelY = 0.299*channelR + 0.587*channelG + 0.114*channelB

    outR = channelY
    outG = channelY
    outB = channelY

    return outR, outG, outB