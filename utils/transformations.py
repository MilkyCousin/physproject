from numpy import array


def apply_noise(z: array, mean: float = 0, sdev: float = 1) -> array:
    """
    Повертає масив **z** із додаванням до елементів гауссового шуму
    з математичним сподіванням **mean** та середньоквадратичним відхиленням **sdev**.
    """
    from numpy.random import normal

    return z + normal(mean, sdev, z.shape)
