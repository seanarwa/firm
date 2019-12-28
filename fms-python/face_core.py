import os
import time
import logging as log
import numpy as np
from scikit-learn.preprocessing import normalize

# local modules
import config

def process(encoding):

    normalized_encoding = get_quantized_features(encoding)

    return normalized_encoding

def get_median_values_for_bins(bins):
    median_values = {}
    for binidx in range(1, bins.shape[0]):
        binval = bins[binidx]
        binval_prev = bins[binidx - 1]
        median_values[binidx] = binval_prev

    median_values[bins.shape[0]] = bins[bins.shape[0]-1]
    return median_values

def get_quantized_features(features, quantization_factor=30):
    normalized_features = normalize(features, axis=1)
    offset = np.abs(np.min(normalized_features))
    offset_features = normalized_features + offset # Making all feature values positive

    # Let's proceed to quantize these positive feature values
    min_val = np.min(offset_features)
    max_val = np.max(offset_features)

    bins = np.linspace(start=min_val, stop=max_val, num=quantization_factor)
    median_values = get_median_values_for_bins(bins)
    original_quantized_features = np.digitize(offset_features, bins)

    quantized_features = np.apply_along_axis(lambda row: map(lambda x: median_values[x], row), 1, original_quantized_features)
    quantized_features = np.floor(quantization_factor*quantized_features)
    return quantized_features