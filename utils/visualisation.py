import matplotlib.pyplot as plt
from numpy import array


def generate_heatmap(
    out_path: str, x: array, y: array, z: array, context: dict
) -> None:
    """
    Генерує теплову карту на основі меш-гріду **x**, **y** та значень **z** у кожній точці.
    Згенерована теплова карта експортується у файл за вказаним шляхом **out_path**.
    Вигляд карти редагується параметрами з **context**.
    """
    plt.figure(figsize=context["figsize"])
    plt.contourf(x, y, z, **context["contourf"])

    plt.axis("off")
    plt.gca().set_aspect("equal")
    plt.savefig(out_path)
    plt.close()
