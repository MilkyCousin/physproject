from numpy import array
from typing import Callable


def fermi_dirac(w: array, T: float, Ef: float = 0) -> array:
    """
    При заданому значенню температури **T** в eV, обчислюється функція Фермі-Дірака
    при кожному значенні енергії в eV з масиву **w**.

    Рівень Фермі по замовчуванню дорівнює нулю.
    """
    from numpy import exp

    return 1 / (1 + exp((w - Ef) / T))


def epsilon(w0: float) -> Callable[[array], array]:
    """
    При заданому значенні параметра **w0** повертається функція Epsilon(k) для виклику.
    """
    from numpy import cos, pi

    kF = 0.15
    t1a = w0 / (cos(2 * pi * kF) - 1)
    t0a = t1a + w0

    def eps(k: array) -> array:
        """
        Власне реалізація функції Epsilon(k) при заданому імпульсі **k**.
        """
        return t0a - t1a * cos(2 * pi * k)

    return eps


def SigmasNum(
    alpha: float,
    beta: float,
    P: float,
    G: float,
    C: float,
    w0: float,
    wc: float,
    T: float,
) -> dict[str, Callable]:
    """
    При заданих значеннях параметрів повертаються функції Sigma1, Sigma2
    для виклику. Форми для Sigma1, Sigma2 обрані спеціальним чином.
    """
    wc2 = wc * wc
    T2 = T * T
    PG = P * G
    G2 = G * G

    def Sigma1(k: array, w: array) -> array:
        """
        Підрахунок при заданому імпульсі **k** та енергії **w** значення Sigma1 (себто зсув)
        """
        dw0 = w - w0
        w2 = w * w
        s = -(alpha * w * wc) / (1 + w2 / wc2) + (PG * dw0) / (dw0 * dw0 + G2)
        return s

    def Sigma2(k: array, w: array) -> array:
        """
        Підрахунок при заданому імпульсі **k** та енергії **w** значення Sigma2 (себто ширина по eV)
        """
        dw0 = w - w0
        w2 = w * w
        s = C + (alpha * w2) / (1 + w2 / wc2) + beta * T2 + (PG * G) / (dw0 * dw0 + G2)
        return s

    return {"Sigma1": Sigma1, "Sigma2": Sigma2}


def Afunc(
    sigma1: Callable[[array, array], array],
    sigma2: Callable[[array, array], array],
    eps: Callable[[array], array],
) -> Callable[[array, array], array]:
    """
    При заданих функціях Sigma1(k, w), Sigma2(k, w) та Epsilon(k) повертається
    спектральна функція A(k, w) для підрахунку.
    """
    from numpy import pi

    def A(k: array, w: array) -> array:
        """
        Власне реалізація спектральної функції при заданому імпульсі **k** та енергії **w**.
        """
        s1 = sigma1(k, w)
        s2 = sigma2(k, w)
        e = eps(k)
        return (1 / pi) * s2 / ((w - e - s1) ** 2 + s2**2)  # but -1!

    return A


def ANumfunc(
    alpha: float,
    beta: float,
    P: float,
    G: float,
    C: float,
    w0: float,
    wc: float,
    T: float,
) -> Callable[[array, array], array]:
    """
    Реалізація спектральної функції A(k,w) при спеціальних формах для Sigma1(k, w), Sigma2(k, w), Epsilon(k).
    """
    epsf = epsilon(w0)
    Sigmas = SigmasNum(alpha, beta, P, G, C, w0, wc, T)
    return Afunc(Sigmas["Sigma1"], Sigmas["Sigma2"], epsf)


def SpectraSum(
    array_params: list, matr_coefs: array
) -> Callable[[array, array], array]:
    """
    Реалізація суми спектральних функцій в ARPES.
    Кількість доданків визначається кількістю елементів у масиві.

    **array_params** є масивом зі словників -- набору параметрів для кожного доданка
    (спектральної функції).

    **matr_coefs** є масивом з матричних елементів.
    """
    assert len(matr_coefs) == len(array_params)
    L = len(matr_coefs)
    array_ANumfunc = list(map(lambda params: ANumfunc(**params), array_params))

    def SumA(k: array, w: array) -> array:
        sumA = 0
        for j in range(L):
            sumA += array_ANumfunc[j](k, w) * matr_coefs[j]
        return sumA

    return SumA
