import tkinter as tk
from tkinter import filedialog
import os
import json
import jmespath
from PIL import ImageTk, Image


def do_selection(data: dict) -> None:
    select_content(data)
    if "path" in data:
        pathdata.insert(0, data["path"])
        print(data["path"])


def select_content(data: dict) -> None:
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        data["path"] = folder_selected


def do_export(data: dict) -> None:
    export_content(data)
    objectsbox.delete(0, tk.END)
    for j, obj in enumerate(data["objects"]):
        objectsbox.insert(j, obj["image"])


def export_content(data: dict) -> None:
    path = data["path"]
    path_img = os.path.join(path, "images")
    path_meta = os.path.join(path, "meta.json")
    assert os.path.exists(path_img)
    assert os.path.exists(path_meta)
    with open(path_meta, "r") as src:
        data["objects"] = json.load(src)
    print(data)


def do_deletion(data: dict) -> None:
    delete_content(data)
    pathdata.delete(0, tk.END)
    objectsbox.delete(0, tk.END)
    paramsbox.delete("1.0", tk.END)
    image.delete(tk.ALL)

    top.imgi = None
    top.img = None

    print("done")


def delete_content(data: dict) -> None:
    data.clear()
    print(data)


def do_visualisation(event, data: dict) -> None:
    widget = event.widget
    j0 = int(widget.curselection()[0])
    selected = widget.get(j0)
    result = jmespath.search(f"objects[?image=='{selected}']", data)
    print(result)

    if len(result) > 0:
        print("hello")
        obj = result[0]
        imgi = Image.open(obj["image"])
        img = ImageTk.PhotoImage(imgi)
        top.imgi = imgi
        top.img = img
        image.create_image(375, 375, image=img)

        paramsbox.delete("1.0", tk.END)

        text_items = []
        for i, param in enumerate(obj["parameters"]):
            text_items_local = []
            text_items_local.extend([f"Доданок №{i+1}:"])
            text_items_local.extend(
                [f"{variable} = {value}" for variable, value in param.items()]
            )
            text_items.append("\n".join(text_items_local))
        text_to_paste = "\n\n".join(text_items)
        print(text_to_paste)
        paramsbox.insert("1.0", text_to_paste)


def zoom(delta):
    if top.img is None or top.imgi is None:
        return
    imgi = top.imgi
    w, h = imgi.size
    wn, hn = int(w * delta), int(h * delta)
    imgi_new = imgi.resize((wn, hn))
    img_new = ImageTk.PhotoImage(imgi_new)
    top.imgi = imgi_new
    top.img = img_new
    image.create_image(375, 375, image=img_new)


def zoom_in():
    zoom(1.25)


def zoom_out():
    zoom(1 / 1.25)


if __name__ == "__main__":
    top = tk.Tk()
    top.resizable(False, False)

    ## Дані про папку з об'єктами
    data = dict()

    ## Рамка з віджетами вибору даних
    frame_path = tk.Frame(top)
    frame_path.grid(row=0, column=1, sticky="nsew")

    # Назва рамки
    pathlabel = tk.Label(frame_path, text="Зазначте шлях до даних:")
    pathlabel.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Поле зі шляхом до папки
    pathdata = tk.Entry(frame_path, width=50)
    pathdata.grid(row=0, column=2, columnspan=2, sticky="nsew")

    # Кнопка навігації по папкам
    lookdata = tk.Button(
        frame_path, text="Навігація", command=lambda: do_selection(data)
    )
    lookdata.grid(row=1, column=1, sticky="nsew")

    # Кнопка підвантаження даних з папки
    loaddata = tk.Button(
        frame_path, text="Завантаження", command=lambda: do_export(data)
    )
    loaddata.grid(row=1, column=2, sticky="nsew")

    # Кнопка очищення даних з інтерфейсу
    deletedata = tk.Button(
        frame_path, text="Очищення", command=lambda: do_deletion(data)
    )
    deletedata.grid(row=1, column=3, sticky="nsew")

    ## Рамка з віджетами вибору об'єктів
    frame_objects = tk.Frame(top)
    frame_objects.grid(row=1, column=0, sticky="nsew")

    # Назва фрейму
    objectslabel = tk.Label(frame_objects, text="Перелік об'єктів:")
    objectslabel.grid(row=0, column=1, sticky="nsew")

    # Перелік об'єктів
    objectsbox = tk.Listbox(frame_objects, width=50)
    objectsbox.grid(row=1, column=1, sticky="nsew")
    objectsbox.bind("<<ListboxSelect>>", lambda evt: do_visualisation(evt, data))

    objectsboxsby = tk.Scrollbar(frame_objects, command=objectsbox.yview)
    objectsboxsby.grid(row=1, column=0, sticky="nsew")

    objectsboxsbx = tk.Scrollbar(
        frame_objects, command=objectsbox.xview, orient=tk.HORIZONTAL
    )
    objectsboxsbx.grid(row=2, column=1, sticky="nsew")

    objectsbox.configure(
        xscrollcommand=objectsboxsbx.set, yscrollcommand=objectsboxsby.set
    )

    ## Рамка з відображенням параметрів об'єкту
    frame_params = tk.Frame(top)
    frame_params.grid(row=1, column=2, sticky="nsew")

    # Назва фрейму
    paramslabel = tk.Label(frame_params, text="Параметри об'єкта:")
    paramslabel.grid(row=0, column=1, sticky="nsew")

    # Перелік параметрів
    paramsbox = tk.Text(frame_params, width=50)
    paramsbox.grid(row=1, column=1, sticky="nsew")

    paramsboxsby = tk.Scrollbar(frame_params, command=paramsbox.yview)
    paramsboxsby.grid(row=1, column=0, sticky="nsew")

    paramsboxsbx = tk.Scrollbar(
        frame_params, command=paramsbox.xview, orient=tk.HORIZONTAL
    )
    paramsboxsbx.grid(row=2, column=1, sticky="nsew")

    paramsbox.configure(
        xscrollcommand=paramsboxsbx.set, yscrollcommand=paramsboxsby.set
    )

    ## Рамка з віджетами для відображення об'єкту
    frame_image = tk.Frame(top)
    frame_image.grid(row=1, column=1, sticky="nsew")

    # Зображення, що відповідає об'єкту
    image = tk.Canvas(frame_image, width=750, height=750, bg="gray")
    image.grid(row=0, column=0, columnspan=2, sticky="nsew")

    top.imgi = None
    top.img = None

    # Кнопки навігації по відображенню
    zoomin = tk.Button(frame_image, text="Збільшити", command=zoom_in)
    zoomin.grid(row=1, column=0, sticky="nsew")

    zoomout = tk.Button(frame_image, text="Зменшити", command=zoom_out)
    zoomout.grid(row=1, column=1, sticky="nsew")

    ## Конфігурування
    frame_path.columnconfigure(1, weight=1)
    frame_path.rowconfigure(1, weight=1)

    frame_objects.columnconfigure(1, weight=1)
    frame_objects.rowconfigure(1, weight=1)

    frame_params.columnconfigure(1, weight=1)
    frame_params.rowconfigure(1, weight=1)

    top.title("Перегляд візуалізацій")

    top.mainloop()
