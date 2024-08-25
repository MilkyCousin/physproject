import tkinter as tk
from PIL import ImageTk, Image
import json
import os
from utils import formulas, visualisation, transformations
import numpy as np


def do_generation():
    values = dict()
    for param in param_labels:
        param_value = param_elements[param]["entry"].get()
        param_value = float(param_value) if param_value else float(0)
        print(param_value)
        values[param] = param_value

    ss = formulas.SpectraSum([values], [1])
    f = lambda k, w: ss(k, w) * formulas.fermi_dirac(w, values["T"])

    ##

    kvals = np.linspace(-0.5, 0.5, 100)
    wvals = np.linspace(-0.4, 0.2, 100)
    K, W = np.meshgrid(kvals, wvals)

    Z = f(K, W)

    # testing, so it is fixed
    np.random.seed(0)
    Z_noisy = transformations.apply_noise(Z, 0, 10e-2)

    ##

    contextb = {
        "figsize": (6, 7),
        "contourf": {
            "levels": 100,
            "cmap": "terrain",
        },
    }

    temp_path = "./temp.png"
    visualisation.generate_heatmap(temp_path, K, W, Z_noisy, contextb)

    imgi = Image.open(temp_path)
    img = ImageTk.PhotoImage(imgi)
    top.imgi = imgi
    top.img = img
    image.create_image(375, 375, image=img)


def do_deletion():
    for param in param_labels:
        param_elements[param]["entry"].delete(0, tk.END)

    image.delete(tk.ALL)


if __name__ == "__main__":
    top = tk.Tk()
    top.resizable(False, False)

    frame_image = tk.Frame(top)
    frame_image.grid(row=0, column=0, sticky="nsew")

    frame_params = tk.Frame(top)
    frame_params.grid(row=0, column=1, sticky="nsew")

    frame_image.columnconfigure(1, weight=1)
    frame_image.rowconfigure(1, weight=1)

    frame_params.columnconfigure(1, weight=1)
    # frame_params.rowconfigure(1, weight=1)

    ###

    image = tk.Canvas(frame_image, width=750, height=750, bg="gray")
    image.grid(row=0, column=0, sticky="nsew")

    ###

    param_labels = ["alpha", "beta", "P", "G", "C", "w0", "wc", "T"]
    param_elements = dict()

    for j, param in enumerate(param_labels):
        label = tk.Label(frame_params, text=param)
        label.grid(row=j, column=0, sticky="ew")

        entry = tk.Entry(frame_params)
        entry.grid(row=j, column=1, sticky="ew")

        param_elements[param] = {"label": label, "entry": entry}

    generate_button = tk.Button(frame_params, text="Згенерувати", command=do_generation)
    generate_button.grid(row=len(param_labels), column=0, columnspan=2, sticky="ew")

    clear_button = tk.Button(frame_params, text="Очистити", command=do_deletion)
    clear_button.grid(row=len(param_labels) + 1, column=0, columnspan=2, sticky="ew")

    top.title("Симулятор одного спектру")

    top.mainloop()
