import time
import pyinterp.bivariate
import pyinterp.bicubic
import scipy.interpolate
import numpy as np


def generate_2d(step=1):
    x = np.arange(-180, 180, step) + step
    y = np.arange(-90, 90, step) + step
    x = x[(x >= -180) & (x < 180)]
    y = y[(y >= -90) & (y < 90)]
    mx, my = np.meshgrid(x, y)
    z = np.sin(np.pi * np.radians(mx) * 0.5) * np.exp(np.radians(my) * 0.5)

    return x, y, z


def scipy_interp2d(x, y, z, xp, yp, kind='linear'):
    f = scipy.interpolate.interp2d(x, y, z, kind=kind, copy=False)
    return f(xp, yp)


def scipy_regular_grid_interpolator(x, y, z, xp, yp, method='linear'):
    f = scipy.interpolate.RegularGridInterpolator((x, y),
                                                  z,
                                                  method=method,
                                                  bounds_error=False)
    return f((xp, yp))


def pyinterp_linear(x, y, z, xp, yp):
    x = pyinterp.core.Axis(x, is_circle=True)
    y = pyinterp.core.Axis(y, is_circle=False)
    f = pyinterp.bivariate.Bivariate(x, y, z)
    return f.evaluate(xp.flatten(),
                      yp.flatten(),
                      interpolator='bilinear',
                      num_threads=1).reshape(xp.shape)


def pyinterp_bicubic(x, y, z, xp, yp):
    x = pyinterp.core.Axis(x, is_circle=True)
    y = pyinterp.core.Axis(y, is_circle=False)
    f = pyinterp.bicubic.Bicubic(x, y, z)
    return f.evaluate(xp.flatten(),
                      yp.flatten(),
                      nx=3,
                      ny=3,
                      fitting_model='c_spline',
                      num_threads=0).reshape(xp.shape)


def timeit(func, *args, num=10, **kwargs):
    delta = []
    for _ in range(num):
        t0 = time.time()
        _ = func(*args, **kwargs)
        delta.append(time.time() - t0)
    delta = np.array(delta)
    return f"{delta.mean()} ± {delta.std()}"


def main():
    # print(f'step, interp2d, RegularGridInterpolator, pyinterp.bivariate')
    # for step in [1.0, 4.0, 8.0, 16.0]:
    #     step = 1 / step
    #     x, y, z = generate_2d(step)
    #     xp, yp = x + step, y + step
    #     mx, my = np.meshgrid(xp, yp)
    #     a = timeit(scipy_interp2d, x, y, z, xp, yp)
    #     b = timeit(scipy_regular_grid_interpolator, x, y, z.T, mx, my)
    #     c = timeit(pyinterp_linear, x, y, z.T, mx, my)
    #     print(f'{1/step}, {a}, {b}, {c}')

    print(f'step, interp2d, RegularGridInterpolator, pyinterp.bivariate')
    for step in [1.0, 4.0, 8.0, 16.0]:
        step = 1 / step
        x, y, z = generate_2d(step)
        xp, yp = x + step, y + step
        mx, my = np.meshgrid(xp, yp)
        #a = timeit(scipy_interp2d, x, y, z, xp, yp, kind="cubic")
        c = timeit(pyinterp_bicubic, x, y, z.T, mx, my)
        print(f'{1/step}, a, {c}')


if __name__ == "__main__":
    main()

#

# import matplotlib.pyplot as plt
# plt.imshow(scipy_interp2d(x, y, z, x + 0.25, y + 0.25))
# plt.show()
# plt.imshow(scipy_regular_grid_interpolator(x, y, z.T, x + 0.25, y + 0.25))
# plt.show()
# plt.imshow(pyinterp_linear(x, y, z.T, x + 0.25, y + 0.25))
# plt.show()
