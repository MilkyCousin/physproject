import json
import os
from utils import formulas, visualisation
import numpy as np

path_to_json = os.path.join("input_json", "input.json")
with open(path_to_json, "r") as input_json:
    input_given = json.load(input_json)

array_params = input_given["parameters"]
nzones = len(array_params)
matr_coefs = [1] * nzones

for elem in array_params:
    Tempvalue = elem["T"]

# alpha=[0.5,8]
# beta=[20,200]
# T=[0.001,0.025]
# C=[0.01,0.05]
# P=[0.02,0.05]
# G=[0.01,0.5]
# wc=[0.0001,0.3]
# w0=[-0.1,0]

ss = formulas.SpectraSum(array_params, matr_coefs)

kvals = np.linspace(-0.5, 0.5, 100)
wvals = np.linspace(-0.4, 0.2, 100)
K, W = np.meshgrid(kvals, wvals)

f = lambda k, w: ss(k, w) * formulas.fermi_dirac(w, Tempvalue)

contextb = {
    "figsize": (6, 7),
    "contourf": {
        "levels": 100,
        "cmap": "terrain",
    },
}

Z = f(K, W)
Z_noisy = visualisation.apply_noise(Z, 0, 10e-2)

visualisation.generate_heatmap(input_given["image"], K, W, Z_noisy, contextb)
