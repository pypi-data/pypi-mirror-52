import numpy as np

from . import misc


def gaussian(x, a, x0, fwhm, offset):
    """ Compute Gaussian function.
    http://mathworld.wolfram.com/GaussianFunction.html

    Parameters
    ----------
    x : float
        parameter at which the Gaussian function is computed
    a : float
        amplitude
    x0 : float
        offset on x-axis
    fwhm : float
        Full-width-at-half-maximum (FWHM)
    offset : float
        amplitude offset

    Returns
    -------
    float
        Value of Gaussian function for x

    Notes
    -----
    If x is an np.array, a corresponding array is returned.
    """
    s = fwhm/(2*np.sqrt(2*np.log(2)))
    return a*np.exp(-(x-x0)**2/(2*s**2)) + offset


def gaussian2d(x, y, a, x0, y0, fwhm_x, fwhm_y, offset):
    """ Compute two-dimensioanl Gaussian function.

    Parameters
    ----------
    x : float
        x coordinate at which the Gaussian function is computed
    y : float
        y coordinate at which the Gaussian function is computed
    a : float
        amplitude
    x0 : float
        offset on x-axis
    y0 : float
        offset on y-axis
    fwhm_x : float
        Full-width-at-half-maximum (FWHM) along x axis
    fwhm_y : float
        Full-width-at-half-maximum (FWHM) along y axis
    offset : float
        amplitude offset

    Returns
    -------
    float
        Value of Gaussian function at coordinates x,y

    Notes
    -----
    If x is an np.mgrid (or meshgrid), a corresponding mgrid is returned.
    """
    s_x = fwhm_x/(2*np.sqrt(2*np.log(2)))
    s_y = fwhm_y/(2*np.sqrt(2*np.log(2)))

    return a*np.exp(-(x-x0)**2/(2*s_x**2) - (y-y0)**2/(2*s_y**2)) + offset


def lorentzian(x, a, x0, fwhm, offset):
    """ Compute Lorentzian function.
    http://mathworld.wolfram.com/LorentzianFunction.html
    The function is normalized not to its area, but to the amplitude a.

    Parameters
    ----------
    x : float
        parameter at which the Lorentzian function is computed
    a : float
        amplitude
    x0 : float
        offset on x-axis
    fwhm : float
        Full-width-at-half-maximum (FWHM)
    offset : float
        amplitude offset

    Returns
    -------
    float
        Value of Lorentzian function for x

    """
    return a*fwhm**2/4/((x-x0)**2 + (fwhm/2)**2) + offset


#def airy_fpi(length, wl, finesse):
#    delta = 4*np.pi*length/wl
#    return 1/(1+finesse*np.sin(delta/2)**2)

def airy_fpi(delta, r1, r2):
    """ Compute Airy function of a Fabry-Perot interferometer

    Parameters
    ----------
    delta : float
        Round-trip phase inside the cavity (in radians)
    r1 : Reflection coefficient (field value) for mirror 1
    r2 : Reflection coefficient (field value) for mirror 1

    Returns
    -------
    float
        Value of Airy function

    """
    #delta = 4*np.pi*length/wl  # round-trip phase shift
    f = 4*r1*r2/(1-r1*r2)**2  # f: "finesse coefficient", note: finesse=pi*sqrt(f)/2=pi*sqrt(r1*r2)/(1-r1*r2)
    a = 1/(1-r1*r2)**2
    #a = r1*r2
    #a=1
    return a/(1+f*np.sin(delta/2)**2)


def boxcar(x_array, center, width):
    """ Compute boxcar (rectangular) function
    https://en.wikipedia.org/wiki/Boxcar_function

    Parameters
    ----------
    x_array : np.ndarray
        Array containing the x values of the function
    center : float
        Center of the box (rectangular pulse) in units of x_array
    width : float
        Center of the box (rectangular pulse) in units of x_array

    Returns
    -------
    np.ndarray
        Boxcar function
    """
    r = np.zeros(len(x_array))
    for idx, x in enumerate(x_array):
        if center-width/2 <= x <= center+width/2:
            r[idx] = 1
        else:
            r[idx] = 0
    return r


def boxcar_inverse(x_array, center, width):
    """ Compute inverse boxcar (rectangular) function

    Parameters
    ----------
    x_array : np.ndarray
        Array containing the x values of the function
    center : float
        Center of the box (rectangular pulse) in units of x_array
    width : float
        Center of the box (rectangular pulse) in units of x_array

    Returns
    -------
    np.ndarray
        Inverse boxcar function
    """
    r = np.zeros(len(x_array))
    for idx, x in enumerate(x_array):
        if center-width/2 <= x <= center+width/2:
            r[idx] = 0
        else:
            r[idx] = 1
    return r


def scale(value, mode):
    """ Scale value

    Parameters
    ----------
    value : float or array-like
        Value or array to be scaled
    mode : str
        'log': scale to log10(value)*10
        'linear': scale to linear from log10

    Returns
    -------
    float or array-like
        Scaled value
    """
    if mode == 'linear':
        return 10**(value/10)
    elif mode == 'log':
        return np.log10(value) * 10


def initial_fit_values(data_x, data_y, mode):
    """ Guess initial values for a fit procedure

    Parameters
    ----------
    data_x : np.array
        x data
    data_y : np.array
        y_data
    mode : str
        Defines which function is assumed for fitting procedure. Can be one of the following:
        'gaussian', 'lorentzian'

    Returns
    -------
    List of initial values. Content of the list depends on "mode".
    mode == 'gaussian' or 'lorentzian': [amplitude (a), offset on x-axis (x0), full-width-at-half-maximum (fwhm),
        amplitude offset (offset)]
    """
    if mode == 'gaussian' or mode == 'lorentzian':
        max_index = np.argmax(data_y)
        x0_0 = data_x[max_index]
        a_0 = data_y[max_index]

        _, idx_right = misc.find_nearest(data_y[max_index:-1], a_0 / 2)
        _, idx_left = misc.find_nearest(data_y[0:max_index], a_0 / 2)
        y_right = data_y[max_index + idx_right]
        y_left = data_y[idx_left]
        fwhm_0 = np.abs(y_right - y_left)

        offset_0 = np.amin(data_y)

        return [a_0, x0_0, fwhm_0, offset_0]
