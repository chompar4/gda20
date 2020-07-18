from constants import cm_mga_zone, cm_zone1, zone0_edge, zone_width, central_scale_factor

import math
import numpy as np

tan = math.tan
cos = math.cos
cosh = math.cosh
sin = math.sin
sinh = math.sinh
atan = math.atan 
atanh = math.atanh
asinh = math.asinh
sqrt = math.sqrt

def get_zone(dLng):
    """
    gives the tranverse mercator zone containing 
    longitude 'lng', using parameters defined in constants
    zones have the range [west, east).
    """
    return math.floor((dLng - zone0_edge) / zone_width)

def get_cm(lng):
    """
    # TODO: update cm_mga_zone with values outside MGA zones
    gives the central meridian longitude of the zone
    containing 'lng'
    """
    return cm_mga_zone[get_zone(lng)]

def TM_n_component(α, r, _ε, _N):
    return α[2*r] * cos(2*r*_ε) * sinh(2*r*_N)

def TM_e_component(α, r, _ε, _N):
    return α[2*r] * sin(2*r*_ε) * cosh(2*r*_N)

def rectifying_radius(a, n):
    """
    gives the rectifying radius A of a circle having 
    the same circumference as the meridian ellipse with:
        a: semi major axis
        n: 3rd flattening
    """
    return (
        a / (1 + n) * (
            1 
            + (1/4) * n**2 
            + (1/64) * n**4
            + (1/256) * n**6 
            + (25/ 16384) * n**8
        )
    )

def ellipsoidal_constants(_f):
    """
    gives the required ellipsoidal constants
    of an ellipse with:
        _f : inverse flattening
    returns: 
        f: flattening
        e: eecentricity
        e2: eecentricity^2
        n: 3rd flattening
    """
    f = 1/_f
    e2 = f * (2-f)
    e = sqrt(e2)
    n = f / (2-f)
    return f, e, e2, n   

def transverse_mercator(_N, _ε, α): 
    """
    Compute normalised TM coordinates (N, E)
    Accepts: 
        _N: normalised gauss-schreiber northing
        _ε: normalised gauss-schreiber easting
        α: krueger_coefficients
    returns
        N: normalised TM northing
        E: normalised TM easting
    """
    N = _N + sum(TM_n_component(α, r, _ε, _N) for r in np.linspace(start=1, stop=8, num=8))
    E = _ε + sum(TM_e_component(α, r, _ε, _N) for r in np.linspace(start=1, stop=8, num=8))
    return N, E

def gauss_schreiber(_t, ω, a):
    """
    gives a gauss-schreiber projection
    accepts:
        - t: tan of conformal latitude
        - ω: longitudal difference
        - a: ellipsoidal semi major axis
    returns: 
        - _ε, _N : normalised gauss-schreiber coords
    """

    u = a * atan(_t/cos(ω))
    v = a * asinh(sin(ω) / sqrt(_t**2 + (cos(ω)**2)))

    _ε = u / a 
    _N = v / a
    return _ε, _N

def q_component(α, r, _ε, _N):
    return 2*r*α[2*r] * sin(2*r*_ε)*sinh(2*r*_N)

def p_component(α, r, _ε, _N):
    return 2*r*α[2*r]*cos(2*r*_ε)*cosh(2*r*_N)

def pq_coefficients(α, _ε, _N):
    """
    gives the p, q coefficients for eq (70-75)
    accepts: 
        _N: normalised gauss-schreiber northing
        _ε: normalised gauss-schreiber easting
        α: krueger_coefficients
    returns:
        p, q: coeffs
    """
    q = - sum(
        q_component(α, r, _ε, _N) 
        for r in np.linspace(start=1, stop=8, num=8)
        )
    p = 1 + sum(
        p_component(α, r, _ε, _N)
        for r in np.linspace(start=1, stop=8, num=8)
        )
    return q, p


def conformal_latitude(φ, e):
    """
    gives the latitude of the conformal sphere 
    with radius a. Accepts: 
        φ: geographical latitude in radians
        e: ellipsoidal eecentricity
    returns 
        t, σ : geographical properties
        _t, _σ: conformal properties

    """
    t = tan(φ)
    σ = sinh(e * atanh(e * t / sqrt(1 + t**2)))
    _t = t*sqrt(1 + σ**2) - σ*sqrt(1 + t**2)
    _φ = atan(_t)
    return t, σ, _t, _φ

def grid_convergence(q, p, _t, ω):
    """
    gives the angle between the meridian
    and the grid-line parallel to the u-axis
    """
    return (
        atan(abs(q/p))
        + atan(
            abs(_t * tan(ω))/ sqrt(1 + _t**2)
        )
    )

def point_scale_factor(rLat, A, a, q, p, t, _t, e2, ω):
    """
    gives the point scale factor
    """
    return central_scale_factor * (A/a) * sqrt(q**2 + p**2) * (
        sqrt(1 + t**2)*sqrt(1-e2*sin(rLat)**2)
        /
        sqrt(_t**2 + cos(ω)**2)
    )

def krueger_coefficients(n):
    """
    Compute the coefficients (α) required for Kruegers eq'n.
    See docs in reference for these. AFAIK know general form
    of these has been presented. TODO: fit a formula for them
    """

    n2 = n ** 2
    n3 = n ** 3
    n4 = n ** 4
    n5 = n ** 5
    n6 = n ** 6 
    n7 = n ** 7
    n8 = n ** 8

    α2 = (
        1/2*n 
        - 2/3*n2 
        + 5/16*n3 
        + 41/180*n4 
        - 127/288*n5 
        + 7891/37800*n6 
        + 72161/387072*n7
        - 18975107/50803200*n8 
    )

    α4 = (
        13/48*n2 
        -3/5*n3 
        + 557/1440*n4
        +281/630*n5
        -1983433/1935360*n6 
        +13769/28800*n7
        +148003883/174182400*n8
    )
    α6 = (
        61/240*n3
        - 103/140*n4
        +15061/26880*n5
        + 167603/181440*n6 
        - 67102379/29030400*n7
        +79682431/79833600*n8
    )
    α8 = (
        49561/161280*n4 
        - 179/168*n5 
        + 6601661/7257600*n6 
        + 97445/49896*n7 
        - 40176129013/7664025600*n8
    )
    α10 = (
        34729/80640*n5
        - 3418889/1995840*n6
        +14644087/9123840*n7 
        + 2605413599/622702080*n8
    )
    α12 = (
        212378941/319334400*n6
        -30705481/10378368*n7 
        + 175214326799/58118860800*n8
    )
    α14 = (
        1522256789/1383782400*n7 
        - 16759934899/3113510400*n8
    )
    α16 = (
        1424729850961/743921418240*n8
    )

    return {
        2: α2, 
        4: α4, 
        6: α6, 
        8: α8, 
        10: α10, 
        12: α12, 
        14: α14, 
        16: α16, 
    }




    