from geodesy.datums import GDA94, AGD66
from projections import lambert_conformal_conic
from geodesy.points import VICPoint, GeoPoint, PlanePoint
from geodesy.grids import VICGRID, VICGRID94

"""

The VICGRID94 Map Projection was specified and adopted
by Land Victoria on the 7th of February 2000 at a Land 
Information Group Technical Meeting in response to user need.
VICGRID94 is a projection created to cater for the needs of 
spatial data users with large regional area interests in and 
beyond the state of Victoria1 and who also wish to use the
Geocentric Datum of Australia 1994 (GDA94) as the underlying 
datum (rather than the Australian Geodetic Datum 1966 (AGD66) 
on which the original VICGRID was based).

It should be noted that the VICGRID94 projection incorporates 
a different origin specification to VICGRID in order to avoid 
confusion between coordinates generated by the two projections. 
The northing false origin for VICGRID94 has been adopted as 2,500,000
metres south of the intersection of the parallel of latitude 37S 
and the central meridian rather than the 4,500,000 specified for
the original VICGRID. The easting false origin remains unchanged 
at 2,500,000 metres west of the intersection of the parallel of 
latitude 37o S and the central meridian.

The formulae to compute Eastings and Northings for VICGRID / VICGRID94
are the same. However it should be noted that different ellipsoids apply
to the datum's relating to VICGRID and VICGRID94. VICGRID uses the
Australian Geodetic Datum 1966, which adopts the Australian National
Spheroid (ANS). VICGRID94 uses the Geocentric Datum of Australia,
which adopts the Geodetic Reference System 1980 (GRS80) ellipsoid.
The constants for the semi major axis and inverse flattening are 
different for ANS and GRS80.

"""


def geo_to_vicgrid94(point):
    """
    Perform a transformation from GDA94 datum to 
    VICGRID94 grid coordinates using a Lambert 
    conformal conic projection.
    """

    assert isinstance(point, GeoPoint), "Please provide a GeoPoint() instance"

    dLat, dLng, datum = point.dLat, point.dLng, point.datum

    assert datum == GDA94, "Please specify your coordinates in GDA94"

    print("({}, {}) -> VICGRID94 from {} coordinates".format(dLat, dLng, datum.name))
    E, N, m, γ = lambert_conformal_conic(dLat, dLng, datum.ellipsoid, grid=VICGRID94)

    return VICPoint(E, N, grid=VICGRID94)


def geo_to_vicgrid(point):

    """
    Perform a transformation from AGD66 datum to 
    VICGRID grid coordinates using a Lambert 
    conformal conic projection.
    """

    assert isinstance(point, GeoPoint), "Please provide a GeoPoint() instance"

    dLat, dLng, datum = point.dLat, point.dLng, point.datum

    assert datum == AGD66, "Please specify your coordinates in GDA94"

    print("({}, {}) -> VICGRID94 from {} coordinates".format(dLat, dLng, datum.name))
    E, N, m, γ = lambert_conformal_conic(dLat, dLng, datum.ellipsoid, grid=VICGRID)
    return VICPoint(E, N, grid=VICGRID)


def vicgrid_to_geo():
    pass


def vicgrid94_to_geo():
    pass
