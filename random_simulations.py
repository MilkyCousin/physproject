from utils import formulas, transformations, visualisation, miscellaneous

import os
import numpy as np
import json


root = miscellaneous.init_directory("./results", rmfiles=False)
root_meta = root
root_images = miscellaneous.init_directory(os.path.join(root, "images"))

###

np.random.seed(0)

###

L = 20
w0_range = np.linspace(-0.1, 0, L)
wc_range = np.linspace(0, 0.5, L)
P_range = np.linspace(0.01, 0.05, L)
G_range = np.linspace(-0.01, 0.2, L)
C_range = np.linspace(0.01, 0.05, L)
T_range = np.linspace(0.001, 0.025, L)
alpha_range = np.linspace(-1, 8, L)
beta_range = np.linspace(20, 200, L)

###

rL = lambda: np.random.randint(0, L)

###

kvals = np.linspace(-0.5, 0.5, 100)
wvals = np.linspace(-0.4, 0.2, 100)
K, W = np.meshgrid(kvals, wvals)

###

B = 1000
S = 3

###

meta_data = []
for b in range(B):
    if not (b + 1) % 100:
        print(f"Photo #{b+1}")

    M = np.random.randint(1, S + 1)

    Aparams = []
    l = rL()
    for m in range(M):
        params = dict(
            alpha=alpha_range[rL()],
            beta=beta_range[rL()],
            P=P_range[rL()],
            G=G_range[rL()],
            C=C_range[rL()],
            w0=w0_range[rL()],
            wc=wc_range[rL()],
            T=T_range[l],
        )
        Aparams.append(params)

    Mcoefs = [1] * len(Aparams)

    SS = formulas.SpectraSum(Aparams, Mcoefs)
    f = lambda k, w: SS(k, w) * formulas.fermi_dirac(w, T_range[l])

    contextb = {
        "figsize": (5, 3),
        "contourf": {
            "levels": 100,
            "cmap": "terrain",
        },
    }

    Z = f(K, W)
    Z_noisy = transformations.apply_noise(Z, 0, 10e-2)

    image_name = f"figure_{b+1}.png"
    image_path = os.path.join(root_images, image_name)

    visualisation.generate_heatmap(image_path, K, W, Z_noisy, contextb)

    meta_data.append(miscellaneous.generate_object(image_path, M, Aparams))


with open(os.path.join(root_meta, "meta.json"), "w") as out:
    json.dump(meta_data, out)
