#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from scipy.interpolate import interp1d, splprep, splev
import shutil
import os

from astropy.time import Time, TimeDelta
from astropy import units as u
from astropy import coordinates as coord

try:
    from geopy.geocoders import Nominatim
    USE_GEOPY = True
except:
    USE_GEOPY = False

__author__ = ['Alan Loh']
__copyright__ = 'Copyright 2018, celespy'
__credits__ = ['Alan Loh']
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Alan Loh'
__email__ = 'alan.loh@obspm.fr'
__status__ = 'WIP'
__all__ = [ 'getLoc', 'getSrc', 'getAltaz', 'getTime', 'getMeridianTransit',
            'getTransit', 'getSep', 'riseTime', 'setTime',
            'meridianTime', 'plotElevation', 'plotElevations',
            'plotSeparation', 'toRadec', 'visibleSky']


# =================================================================================== #
# ------------------------------------- getLoc -------------------------------------- #
# =================================================================================== #
def getLoc(loc, unit='deg'):
    """ Get the a location

        Parameters
        ----------
        * **loc** : tuple or str
            Location query (can be a tuple or a string).
            If tuple, expects (longitude, latitude).
            If string, expects an address, typically `'Paris, France'` and queries Google.
        * **unit** : str, optional
            If `loc` is a tuple of lon/lat, unit can be either `'deg'` or `'rad'`

        Returns
        -------
        * **loc** : ``astropy.coord.EarthLocation``
            EarthLocation object
    """
    if isinstance(loc, str):
        if loc.lower() == 'nenufar':
            old_loc = coord.EarthLocation(lat=47.376511*u.deg, lon=2.1924002*u.deg)
            loc = coord.EarthLocation(lat=47.375944*u.deg, lon=2.193361*u.deg, height=136.195*u.m)
            # latitude=47.375944            ; 47deg22'33.39729" N
            # longitude=2.193361         ; 2deg11'36.09956" E
            # altitude=136.195             ; 136,195 m
            # X_LAMBERT93=639133.971
            # Y_LAMBERT93=6697600.364
            # Z_LAMBERT93=182.096
        else:
            if not USE_GEOPY:
                loc = coord.EarthLocation.of_address(loc)
            else:
                geoloc = Nominatim(user_agent='my-application')
                gloc = geoloc.geocode(loc)
                loc = coord.EarthLocation(lat=gloc.latitude*u.deg, lon=gloc.longitude*u.deg)
    elif isinstance(loc, tuple):
        assert len(loc)==2, 'Only length 2 tuple is understood.'
        if not unit.lower() == 'deg':
            loc = np.degrees(loc)
        loc = coord.EarthLocation(lat=loc[0]*u.deg, lon=loc[1]*u.deg)
    elif isinstance(loc, coord.EarthLocation):
        pass
    else:
        raise ValueError('loc must be aither a tuple: (lon, lat) in degrees or a string adress.')

    return loc


# =================================================================================== #
# ------------------------------------- getSrc -------------------------------------- #
# =================================================================================== #
def getSrc(source, time=None, loc=None, unit='deg'):
    """ Find a specific source
        
        Parameters
        ----------
        * **source** : str, tuple
            Soure name / cooodinates to be resolved
        * **time** : str, number or ``astropy.time.Time``
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`

        Returns
        -------
        * **src** : ``astropy.coord.SkyCoord``
            SkyCoord object
    """
    if isinstance(source, str):
        if source.lower() in ['sun', 'moon', 'jupiter', 'saturn', 'mars', 'venus']:
            time = getTime(time)
            loc  = getLoc(loc)
            with coord.solar_system_ephemeris.set('builtin'):
                src = coord.get_body(source, time, loc)
        else:
            src = coord.SkyCoord.from_name(source)
    elif isinstance(source, tuple):
        assert len(source)==2, 'Only length 2 tuple is understood.'
        if not unit.lower() == 'deg':
            ra, dec = np.degrees(source)
        else:
            ra, dec = source
        src = coord.SkyCoord(ra*u.deg, dec*u.deg, frame='icrs')
    elif isinstance(source, coord.SkyCoord):
        src = source
    else:
        raise ValueError('source parameter not understood.')

    return src


# =================================================================================== #
# ------------------------------------ getAltaz ------------------------------------- #
# =================================================================================== #
def getAltaz(source, time, loc, unit='deg'):
    """ Convert Equatorial coordinates (in deg) to the Horizontal (alt-az) system

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or ``astropy.time.Time``
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`

        Returns
        -------
        * **altaz** : ``astropy.coord.SkyCoord``
            SkyCoord object in alt az coordinates
    """
    if isinstance(source, str):
        source = getSrc(source=source, time=time, loc=loc, unit=unit)
        ra, dec = source.ra.deg, source.dec.deg
    elif isinstance(source, tuple):
        assert len(source)==2, 'Only length 2 tuple is understood.'
        ra, dec = source
        if not unit.lower() == 'deg':
            ra, dec = np.degrees(ra), np.degrees(dec)
    elif isinstance(source, coord.SkyCoord):
        ra, dec = source.ra.deg, source.dec.deg
    else:
        raise ValueError('source parameter not understood.')

    time  = getTime(time)
    loc   = getLoc(loc) 
    radec = coord.SkyCoord(ra*u.deg, dec*u.deg, frame='icrs')
    frame = coord.AltAz(obstime=time, location=loc)
    altaz = radec.transform_to(frame)

    return altaz


# =================================================================================== #
# ------------------------------------ toRadec -------------------------------------- #
# =================================================================================== #
def toRadec(source, time, loc, unit='deg'):
    """ Convert Equatorial coordinates (in deg) to the Horizontal (alt-az) system

        Parameters
        ----------
        * **source** : tuple
            (az, alt)
        * **time** : str, number or ``astropy.time.Time``
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`

        Returns
        -------
        * **altaz** : ``astropy.coord.SkyCoord``
            SkyCoord object in alt az coordinates
    """
    if isinstance(source, tuple):
        az, alt = source
        if not unit.lower() == 'deg':
            az, alt = np.degrees(az), np.degrees(alt)
    else:
        raise ValueError('source parameter not understood.')
    time  = getTime(time)
    loc   = getLoc(loc) 
    azel  = coord.SkyCoord(alt=alt*u.deg, az=az*u.deg, obstime=time, location=loc, frame='altaz')
    
    return azel.fk5


# =================================================================================== #
# ------------------------------------- getTime ------------------------------------- #
# =================================================================================== #
def getTime(time, unit=None):
    """ Convert time to a astropy.Time object

        Parameters
        ----------
        * **time** : ``astropy.time.Time``, number or str
            Time to parse (`'YYYY-MM-DD hh:mm:ss'`)
            Understands also `'now'`, `'tomorrow'`, `'yesterday'`
        * **unit** : str, optional
            If `time` is a number, unit can be `'jd'` or `'mjd'`

        Returns
        -------
        * **time** : ``astropy.time.Time``
            Time object
    """
    if isinstance(time, Time):
        pass
    elif isinstance(time, str):
        if time.lower() == 'now':
            time = Time.now()
        elif time.lower() == 'tomorrow':
            time = Time.now() + TimeDelta(1, format='jd')
        elif time.lower() == 'yesterday':
            time = Time.now() - TimeDelta(1, format='jd')
        else:
            time = Time(time)
    elif isinstance(time, (int, float, np.number)):
        if unit is None:
            unit = 'jd'
        time = Time(time, format=unit.lower())
    else:
        raise ValueError('time parameter not understood.')

    return time


# =================================================================================== #
# ----------------------------------- getTransit ------------------------------------ #
# =================================================================================== #
def getMeridianTransit(source, time, loc, transit='upper'):
    """
        Parameters
        ----------
        
    """
    
    import ephem
    
    time   = getTime(time)
    loc    = getLoc(loc)
    src_name = source
    source = getSrc(source=src_name, time=time, loc=loc, unit='deg')

    observatory = ephem.Observer()
    observatory.lon = str(loc.lon.deg)
    observatory.lat = str(loc.lat.deg)
    observatory.elevation = loc.height.value
    observatory.date = time.iso.replace('-', '/')#'1999/6/27'
    observatory.epoch = '2000'

    if src_name.lower() not in ['jupiter', 'moon', 'mars', 'saturn', 'uranus', 'sun']:
        xephem = ','.join([
            src_name,
            'f',
            ':'.join([str(unit) for unit in source.ra.hms]),
            ':'.join([str(unit) for unit in source.dec.dms]),
            '2',
            '2000'
            ])
        src = ephem.readdb(xephem)
    else:
        if src_name.lower() == 'jupiter':
            src = ephem.Jupiter()
        elif src_name.lower() == 'moon':
            src = ephem.Moon()
        elif src_name.lower() == 'sun':
            src = ephem.Sun()
        elif src_name.lower() == 'mars':
            src = ephem.Mars()
        elif src_name.lower() == 'saturn':
            src = ephem.Saturn()
        elif src_name.lower() == 'uranus':
            src = ephem.Uranus()
        else:
            raise ValueError('Name of celestial body not understood')
    src.compute(observatory)

    if src.neverup:
        print('{} is below the horizon'.format(src_name))
        return np.nan
    elif src.circumpolar:
        return Time(observatory.next_transit(src).datetime(), format='datetime')
    else:
        return Time(observatory.next_transit(src).datetime(), format='datetime')

def getTransit(source, time, loc, az=None, el=None, unit='deg', way='rise', t_step=120):
    """
    """
    time   = getTime(time)
    loc    = getLoc(loc)
    source = getSrc(source=source, time=time, loc=loc, unit=unit)
    day = TimeDelta(86400, format='sec')
    dt = TimeDelta(t_step, format='sec')
    
    azim = []
    elev = []
    ti = []
    end = time + day
    
    while time <= end:
        s = getAltaz(source, time, loc)
        azim.append( s.az.deg )
        elev.append( s.alt.deg )
        ti.append(time.jd)
        time += dt
    
    azim = np.array(azim)
    elev = np.array(elev)
    ti = np.array(ti)
    azim[azim > 180] -= 360

    az_interp = interp1d(ti, azim, kind='linear')
    el_interp = interp1d(ti, elev, kind='linear')
    t_ext = np.arange(ti[0], ti[-1], 5e-6)
    azim_ext = az_interp(t_ext)
    elev_ext = el_interp(t_ext)

    if (az is not None) & (el is None):
        # Define azimuth-based transit
        if az > 180:
            az -= 360
        
        # Roughly find local minima (diff < 1 deg)
        az_diffs = np.abs(azim_ext - az)
        az_mins = az_diffs < az_diffs.min() + 1
        
        # Separate different minima (group by consecutive time)
        condition = np.where(np.diff(t_ext[az_mins]) >= 0.1)[0]
        t_split = np.split(t_ext[az_mins], condition+1)
        azdiff_split = np.split(az_diffs[az_mins], condition+1)
        elev_split = np.split(elev_ext[az_mins], condition+1)

        # Sort the minima by elevations
        t = []
        e = []
        for i in range(len(t_split)):
            if azdiff_split[i].size == 0:
                continue
            id_min = np.argmin(azdiff_split[i])
            t.append(t_split[i][id_min])
            e.append(elev_split[i][id_min])

        if way.lower() == 'rise':
            # Looking at 'higher elevation' transit
            transit = Time(t[np.argmax(e)], format='jd')
        elif way.lower() == 'set':
            # Looking at 'lower elevation' transit
            transit = Time(t[np.argmin(e)], format='jd')
        else:
            transit = Time(t[np.argmax(e)], format='jd')


    elif (el is not None) & (az is None):
        # Define elevation-based transit
        ti_interp = interp1d(ti, elev, kind='linear')
        print( Time(ti_interp(el), format='jd').iso )
    else:
        raise ValueError('either az or el parameters should not be None')
        
    
    # Once approximate transit is found, we will look at a more precise value
    duration = TimeDelta(1200, format='sec') # 10 min
    sdt = TimeDelta(1, format='sec') # this is the maximum precision
    time = transit - duration/2.
    final_az = []
    final_el = []
    final_t = []
    while time < transit + duration/2.:
        s = getAltaz(source, time, loc) 
        final_az.append( s.az.deg )
        final_el.append( s.alt.deg )
        final_t.append( time )
        time += sdt
    final_az = np.array(final_az)
    final_az[final_az > 180] -= 360
    final_el = np.array(final_el)
    final_t = np.array(final_t)

    if (az is not None) & (el is None):
        if az > 180:
            az -= 360
        ind = np.argmin(np.abs(final_az - az))
        return final_t[ind]
    elif (el is not None) & (az is None):
        return
    else:
        return


def getTransit_v1(source, time, loc, az=None, el=None, unit='deg', way='rise', t_step=1800):
    """ Get the *next* transit time for a particular source/position
        at a given position (obs site) since a given time.
        Transit may be defined by the next crossing of a particular azimuth *or* elevation.

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or Time
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **az** : number, optional
            Azimuth at which look for the transit (degrees)
        * **el** : number, optional
            Elevation at which look for the transit (degrees)
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`
        * **way** : str, optional
            If `el` corssing is defined, precise the direction `'rise'` or `set`
        * **t_step** : float, optional
            Time step to look for transit

        Returns
        -------
        * **transit_time** : ``astropy.time.Time`
            Transit time (precision : +/- 2.5 sec)

        Example
        -------
        To get the meridian transit time of Cyg A
            >>> getTransit('Cyg A', 'now', 'nenufar', az=180)
    """
    time   = getTime(time)
    loc    = getLoc(loc)
    source = getSrc(source=source, time=time, loc=loc, unit=unit)

    assert (way.lower() == 'rise') or (way.lower() == 'set'), 'way must be either rise or set'

    def find_time_interval(start, dt, source, az, el):
        while start <= start + dt:
            if (az is not None) & (el is None):
                c1 = getAltaz(source, start, loc).az.deg
                c2 = getAltaz(source, start+dt, loc).az.deg
                if source.dec.deg > loc.lat.deg:
                    deltaaz = np.degrees(np.arccos((90-source.dec.deg)/loc.lat.deg)) # az span
                    # circumpolar
                    if (0. < az <= 0.+deltaaz):
                        if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                            pass
                        elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                            if (c2 <= az <= c1):
                                break
                        else:
                            if (270. <= c2 <= 360.) & (c1 >= az):
                                break
                    elif (az == 0.) or (az == 360.):
                        if (c2 - c1 > 180):
                            break
                    elif (360.-deltaaz <= az < 360.):
                        if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                            if (c2 <= az <= c1):
                                break
                        elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                            pass
                        else:
                            if (0. <= c1 <= 90.) & (c2 <= az):
                                break
                    else:
                        raise ValueError('Azimuth {} not valid for a circumpolar source, only 0.+/-{}'.format(az, deltaaz))
                    
                else:
                    if (c1 <= az <= c2):
                        break
            elif (el is not None) & (az is None):
                c1 = getAltaz(source, start, loc).alt.deg
                c2 = getAltaz(source, start+dt, loc).alt.deg
                if way.lower() == 'rise':
                    if (c1 <= el <= c2):
                        break
                elif way.lower() == 'set':
                    if (c2 <= el <= c1):
                        break
            else:
                raise ValueError('either az or el parameters should not be None')
            start += dt
        return start

    bigdt = TimeDelta(t_step, format='sec') 
    new_start = find_time_interval(start=time, dt=bigdt, source=source, az=az, el=el)
    middt = TimeDelta(t_step/6., format='sec')
    new_start = find_time_interval(start=new_start, dt=middt, source=source, az=az, el=el)
    smalldt = TimeDelta(t_step/360, format='sec')
    new_start = find_time_interval(start=new_start, dt=smalldt, source=source, az=az, el=el)
    smallestdt = TimeDelta(t_step/1800., format='sec')
    new_start = find_time_interval(start=new_start, dt=smallestdt, source=source, az=az, el=el)

    return new_start + smallestdt/2.


# =================================================================================== #
# ----------------------------------- getTransit ------------------------------------ #
# =================================================================================== #
def getTransit_v0(source, time, loc, az=None, el=None, unit='deg', way='rise', t_step=1800):
    """ Get the *next* transit time for a particular source/position
        at a given position (obs site) since a given time.
        Transit may be defined by the next crossing of a particular azimuth *or* elevation.

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or Time
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **az** : number, optional
            Azimuth at which look for the transit (degrees)
        * **el** : number, optional
            Elevation at which look for the transit (degrees)
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`
        * **way** : str, optional
            If `el` corssing is defined, precise the direction `'rise'` or `set`
        * **t_step** : float, optional
            Time step to look for transit

        Returns
        -------
        * **transit_time** : ``astropy.time.Time`
            Transit time (precision : +/- 2.5 sec)

        Example
        -------
        To get the meridian transit time of Cyg A
            >>> getTransit('Cyg A', 'now', 'nenufar', az=180)
    """
    time   = getTime(time)
    loc    = getLoc(loc)
    source = getSrc(source=source, time=time, loc=loc, unit=unit)

    assert (way.lower() == 'rise') or (way.lower() == 'set'), 'way must be either rise or set'

    # Find rough time intervald
    bigdt = TimeDelta(t_step, format='sec') 
    while time <= time + TimeDelta(1, format='jd'):
        if (az is not None) & (el is None):
            c1 = getAltaz(source, time, loc).az.deg
            c2 = getAltaz(source, time+bigdt, loc).az.deg
            if source.dec.deg > loc.lat.deg:
                deltaaz = np.degrees(np.arccos((90-source.dec.deg)/loc.lat.deg)) # az span
                # circumpolar
                if (0. < az <= 0.+deltaaz):
                    if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                        if (c1 <= az <= c2):
                            break
                    elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                        if (c2 <= az <= c1):
                            break
                    else:
                        if (c1 + 360. >= 360. - az >= c2):
                            break
                elif (az == 0.) or (az == 360.):
                    if (c2 - c1 > 180):
                        break
                elif (360.-deltaaz <= az < 360.):
                    if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                        if (c2 <= az <= c1):
                            break
                    elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                        if (c1 <= az <= c2):
                            break
                    else:
                        if (c2 <= az <= c1+360.):
                            break
                else:
                    raise ValueError('Azimuth {} not valid for a circumpolar source, only 0.+/-{}'.format(az, deltaaz))
                
            else:
                if (c1 <= az <= c2):
                    break
        elif (el is not None) & (az is None):
            c1 = getAltaz(source, time, loc).alt.deg
            c2 = getAltaz(source, time+bigdt, loc).alt.deg
            if way.lower() == 'rise':
                if (c1 <= el <= c2):
                    break
            elif way.lower() == 'set':
                if (c2 <= el <= c1):
                    break
        else:
            raise ValueError('either az or el parameters should not be None')
        time += bigdt

    # mid search
    middt = TimeDelta(t_step/6., format='sec')
    while time <= time + bigdt:
        if (az is not None) & (el is None):
            c1 = getAltaz(source, time, loc).az.deg
            c2 = getAltaz(source, time+middt, loc).az.deg
            if source.dec.deg > loc.lat.deg:
                # circumpolar
                if (0. < az <= 0.+deltaaz):
                    if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                        if (c1 <= az <= c2):
                            break
                    elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                        if (c2 <= az <= c1):
                            break
                    else:
                        if (c1 + 360. >= 360. - az >= c2):
                            break
                elif (az == 0.) or (az == 360.):
                    if (c2 - c1 > 180.):
                        break
                elif (360.-deltaaz <= az < 360.):
                    if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                        if (c2 <= az <= c1):
                            break
                    elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                        if (c1 <= az <= c2):
                            break
                    else:
                        if (c2 <= az <= c1+360.):
                            break
                else:
                    pass
            else:
                if (c1 <= az <= c2):
                    break
        elif (el is not None) & (az is None):
            c1 = getAltaz(source, time, loc).alt.deg
            c2 = getAltaz(source, time+middt, loc).alt.deg
            if way.lower() == 'rise':
                if (c1 <= el <= c2):
                    break
            elif way.lower() == 'set':
                if (c2 <= el <= c1):
                    break
        time += middt

    # finer search
    smalldt = TimeDelta(t_step/360, format='sec')
    while time <= time + middt:
        if (az is not None) & (el is None):
            c1 = getAltaz(source, time, loc).az.deg
            c2 = getAltaz(source, time+smalldt, loc).az.deg
            if source.dec.deg > loc.lat.deg:
                # circumpolar
                if (0. < az <= 0.+deltaaz):
                    if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                        if (c1 <= az <= c2):
                            break
                    elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                        if (c2 <= az <= c1):
                            break
                    else:
                        if (c1 + 360. >= 360. - az >= c2):
                            break
                elif (az == 0.) or (az == 360.):
                    if (c2 - c1 > 180.):
                        break
                elif (360.-deltaaz <= az < 360.):
                    if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                        if (c2 <= az <= c1):
                            break
                    elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                        if (c1 <= az <= c2):
                            break
                    else:
                        if (c2 <= az <= c1+360.):
                            break
                else:
                    pass
            else:
                if (c1 <= az <= c2):
                    break
        elif (el is not None) & (az is None):
            c1 = getAltaz(source, time, loc).alt.deg
            c2 = getAltaz(source, time+smalldt, loc).alt.deg
            if way.lower() == 'rise':
                if (c1 <= el <= c2):
                    break
            elif way.lower() == 'set':
                if (c2 <= el <= c1):
                    break
        time += smalldt

    # more finer search
    smallestdt = TimeDelta(t_step/1800., format='sec')
    while time <= time + smalldt:
        if (az is not None) & (el is None):
            c1 = getAltaz(source, time, loc).az.deg
            c2 = getAltaz(source, time+smallestdt, loc).az.deg
            if source.dec.deg > loc.lat.deg:
                # circumpolar
                if (0. < az <= 0.+deltaaz):
                    if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                        if (c1 <= az <= c2):
                            break
                    elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                        if (c2 <= az <= c1):
                            break
                    else:
                        if (c1 + 360. >= 360. - az >= c2):
                            break
                elif (az == 0.) or (az == 360.):
                    if (c2 - c1 > 180.):
                        break
                elif (360.-deltaaz <= az < 360.):
                    if   (270. <= c1 < 360.) & (270. <= c2 < 360.):
                        if (c2 <= az <= c1):
                            break
                    elif (0. <= c1 < 90.) & (0. <= c2 < 90.):
                        if (c1 <= az <= c2):
                            break
                    else:
                        if (c2 <= az <= c1+360.):
                            break
                else:
                    pass
            else:
                if (c1 <= az <= c2):
                    break
        elif (el is not None) & (az is None):
            c1 = getAltaz(source, time, loc).alt.deg
            c2 = getAltaz(source, time+smallestdt, loc).alt.deg
            if way.lower() == 'rise':
                if (c1 <= el <= c2):
                    break
            elif way.lower() == 'set':
                if (c2 <= el <= c1):
                    break
        time += smallestdt

    return time + smallestdt/2.


# =================================================================================== #
# ------------------------------------- riseTime ------------------------------------ #
# =================================================================================== #
def riseTime(source, time, loc, unit='deg'):
    """ Compute the rise time of a source
        This is defined as 0 deg elevation crossing.

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or Time
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`

        Returns
        -------
        * **rising_time** : ``astropy.time.Time`
            Rising time (precision : +/- 2.5 sec)

        Example
        -------
        To get the rising time of Cyg A
            >>> riseTime('Cyg A', 'now', 'nenufar')
    """
    rise = getTransit(source=source,
                        time=time,
                        loc=loc,
                        el=0,
                        unit=unit,
                        way='rise')

    return rise


# =================================================================================== #
# ------------------------------------- setTime ------------------------------------- #
# =================================================================================== #
def setTime(source, time, loc, unit='deg'):
    """ Compute the set time of a source
        This is defined as 0 deg elevation crossing.

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or Time
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`

        Returns
        -------
        * **setting_time** : ``astropy.time.Time`
            Setting time (precision : +/- 2.5 sec)

        Example
        -------
        To get the setting time of Cyg A
            >>> setTime('Cyg A', 'now', 'nenufar')
    """
    sett = getTransit(source=source,
                        time=time,
                        loc=loc,
                        el=0,
                        unit=unit,
                        way='set')

    return sett


# =================================================================================== #
# ----------------------------------- meridianTime ---------------------------------- #
# =================================================================================== #
def meridianTime(source, time, loc, unit='deg'):
    """ Compute the set time of a source
        This is defined as 0 deg elevation crossing.

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or Time
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`

        Returns
        -------
        * **meridian_time** : ``astropy.time.Time`
            Meridian transit time (precision : +/- 2.5 sec)

        Example
        -------
        To get the setting time of Cyg A
            >>> meridianTime('Cyg A', 'now', 'nenufar')
    """
    meridian = getTransit(source=source,
                        time=time,
                        loc=loc,
                        az=180,
                        unit=unit)

    return meridian


# =================================================================================== #
# ------------------------------------- getSep -------------------------------------- #
# =================================================================================== #
def getSep(source1, source2, time=None, loc=None, unit='deg'):
    """ Get the angular separation between two sources

        Parameters
        ----------
        * **source1** : str, tuple
            Soure name / cooodinates to be resolved
        * **source2** : str, tuple
            Soure name / cooodinates to be resolved
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`

        Returns
        -------
        * **angular_separation** : ``astropy.coordinates.angles.Angle``
            Angular separation between `source1` and `source2`
    """
    source1 = getSrc(source=source1, time=time, loc=loc, unit=unit)
    source2 = getSrc(source=source2, time=time, loc=loc, unit=unit)

    return source1.separation(source2)


# =================================================================================== #
# ---------------------------------- plotElevation ---------------------------------- #
# =================================================================================== #
def plotElevation(source, time, loc, unit='deg', dt=1800):
    """ Plot the source elevation for a day since `time`

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or Time
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`
        * **dt** : number, optional
            Time interval for the elevation computation (seconds)
    """
    time   = getTime(time)
    t0     = time.iso.split()[0].replace('-', '/') 
    sname  = source
    lname  = loc 
    loc    = getLoc(loc)
    source = getSrc(source=source, time=time, loc=loc, unit=unit)
    
    # Compute the elevation vs time
    dt    = TimeDelta(dt, format='sec')
    nvals = int((TimeDelta(1, format='jd')/dt).value)
    times = np.zeros( nvals )
    elev  = np.zeros( nvals )
    for i in np.arange(nvals):
        src = getAltaz(source=source, time=time, loc=loc, unit=unit)
        times[i] = time.mjd
        elev[i]  = src.alt.deg
        time += dt

    # Interpolate
    evst  = interp1d(times, elev, kind='cubic')
    times = np.linspace(times[0], times[-1], 1000) 
    elev  = evst(times)

    # Plot
    fig, ax = plt.subplots()
    xtime = mdates.date2num( Time(times, format='mjd').to_datetime() )
    ax.plot( xtime, elev, label='{} @ {}'.format(sname, lname) )
    ax.axhline(0., linestyle='--', color='black', linewidth=1)
    ymin, ymax = ax.get_ylim()
    ax.fill_between( xtime, ymin, ymax,
        where=(elev <= 0.), facecolor='gray', alpha=0.5, step='post')
    ax.fill_between( xtime, ymin, ymax,
        where=(0. <= elev) & (elev <= 20.), facecolor='C3', alpha=0.5, step='mid')
    ax.fill_between( xtime, ymin, ymax,
        where=(20. <= elev) & (elev <= 40.), facecolor='C1', alpha=0.5, step='mid')
    ax.fill_between( xtime, ymin, ymax,
        where=(40. <= elev), facecolor='C2', alpha=0.5, step='mid')
    ax.xaxis_date()
    date_format = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_minor_formatter(date_format)
    fig.autofmt_xdate()
    ax.legend()
    ax.set_xlabel('Time ({} UTC)'.format(t0))
    ax.set_ylabel('Elevation (degrees)')
    plt.show()


# =================================================================================== #
# ---------------------------------- plotElevations --------------------------------- #
# =================================================================================== #
def plotElevations(sources, time, loc, unit='deg', dt=1800):
    """ Plot the source elevation for a day since `time`

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or Time
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`
        * **dt** : number, optional
            Time interval for the elevation computation (seconds)
    """
    fig, ax = plt.subplots()
    lname  = loc
    tini = time
    for source in sources:
        time   = getTime(tini)
        t0     = time.iso.split()[0].replace('-', '/') 
        sname  = source
        loc    = getLoc(loc)
        source = getSrc(source=source, time=time, loc=loc, unit=unit)
        
        # Compute the elevation vs time
        dt    = TimeDelta(dt, format='sec')
        nvals = int((TimeDelta(1, format='jd')/dt).value)
        times = np.zeros( nvals )
        elev  = np.zeros( nvals )
        for i in np.arange(nvals):
            src = getAltaz(source=source, time=time, loc=loc, unit=unit)
            times[i] = time.mjd
            elev[i]  = src.alt.deg
            time += dt

        # Interpolate
        evst  = interp1d(times, elev, kind='cubic')
        times = np.linspace(times[0], times[-1], 1000) 
        elev  = evst(times)

        # Plot
        xtime = mdates.date2num( Time(times, format='mjd').to_datetime() )
        ax.plot( xtime, elev, label='{} @ {}'.format(sname, lname) )
        ax.axhline(0., linestyle='--', color='black', linewidth=1)
        ymin, ymax = ax.get_ylim()
    
        ax.xaxis_date()
        date_format = mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(date_format)
        ax.xaxis.set_minor_formatter(date_format)
        fig.autofmt_xdate()
        ax.legend()
    ax.set_xlabel('Time ({} UTC)'.format(t0))
    ax.set_ylabel('Elevation (degrees)')
    plt.show()


# =================================================================================== #
# ---------------------------------- plotSeparation --------------------------------- #
# =================================================================================== #
def plotSeparation(sources, time, loc, unit='deg', dt=1800):
    """ Plot the source elevation for a day since `time`

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or Time
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **unit** : str, optional
            If `source` is a tuple of ra/dec, unit can be either `'deg'` or `'rad'`
        * **dt** : number, optional
            Time interval for the elevation computation (seconds)
    """
    time   = getTime(time)
    t0     = time.iso.split()[0].replace('-', '/') 
    sname  = '{} -- {}'.format(sources[0], sources[1])
    lname  = loc 
    loc    = getLoc(loc)
    
    # Compute the elevation vs time
    dt    = TimeDelta(dt, format='sec')
    nvals = int((TimeDelta(1, format='jd')/dt).value)
    times = np.zeros( nvals )
    sep  = np.zeros( nvals )
    for i in np.arange(nvals):
        times[i] = time.mjd
        sep[i]  = getSep(sources[0], sources[1], time=time, loc=loc, unit='deg').deg
        time += dt

    # Interpolate
    evst  = interp1d(times, sep, kind='cubic')
    times = np.linspace(times[0], times[-1], 1000) 
    sep  = evst(times)

    # Plot
    fig, ax = plt.subplots()
    xtime = mdates.date2num( Time(times, format='mjd').to_datetime() )
    ax.plot( xtime, sep, label='{} @ {}'.format(sname, lname) )
    ax.axhline(0., linestyle='--', color='black', linewidth=1)
    ymin, ymax = ax.get_ylim()
    ax.xaxis_date()
    date_format = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_minor_formatter(date_format)
    fig.autofmt_xdate()
    ax.legend()
    ax.set_xlabel('Time ({} UTC)'.format(t0))
    ax.set_ylabel('Separation (deg)')
    plt.show()


# =================================================================================== #
# ------------------------------------ visibleSky ----------------------------------- #
# =================================================================================== #
def visibleSky(time, loc, mode='radec'):
    """ Plot the visible sky

        Parameters
        ----------
        * **source** : str, tuple or ``astropy.coord.SkyCoord``
            The astrophysical position/source to convert into Alt Az
        * **time** : str, number or Time
            The UTC time at which the conversion should be computed
        * **loc** : str or tuple
            The location at which the conversion should be computed
        * **mode** : str
            'radec' or 'altaz'
    """
    import healpy as hp
    import matplotlib as mpl

    time = getTime(time)
    loc  = getLoc(loc)

    # Read GAIA HealPIX map
    modulepath = os.path.dirname( os.path.realpath(__file__) )
    gaia = hp.read_map(os.path.join(modulepath, 'other/gaia_medium.fits'))
    gaiacart = hp.cartview(gaia, coord=['G', 'C'], xsize=1024,
            ysize=512, return_projected_map=True)
    plt.close('all')
    gaiara  = np.linspace(180., -180., gaiacart.shape[1]) 
    gaiadec = np.linspace(-90., 90., gaiacart.shape[0]) 
    
    if mode == 'radec':
        ragrid, decgrid = np.meshgrid(gaiara, gaiadec)
        altaz = getAltaz((ragrid, decgrid), time=time, loc=loc)
        azgrid = altaz.az.deg
        altgrid = altaz.alt.deg
        
        invisibleMask = altgrid <= 0.0
        visibleMask   = altgrid > 0.0 
        gaiacart[invisibleMask] = 0.

        limits = (gaiara.max(), gaiara.min(), gaiadec.min(), gaiadec.max())
        normcb = mpl.colors.LogNorm()
        plt.imshow(gaiacart, origin='lower', interpolation='nearest', cmap='bone', norm=normcb, extent=limits)

        # for source in sources:
        #     source = getSrc(source=source, time=time, loc=loc)
        #     plt.plot(source.ra.deg, source.ra.deg, 'ro')

        plt.xlabel('RA')
        plt.ylabel('Dec')
        plt.show()

    elif mode == 'altaz':
        ra0, dec0 = (gaiara[0], gaiadec[0])
        dra, ddec = (gaiara[0] - gaiara[1], gaiadec[1] - gaiadec[0])
        elegrid, azigrid = np.meshgrid(np.arange(-90, 90, ddec),
            np.arange(0, 360, dra) )
        radec = toRadec((azigrid, elegrid), time=time, loc=loc)
        ragrid = radec.ra.deg
        decgrid = radec.dec.deg
        ragrid[ragrid > 180] -= 360 # RA is within -180 and 180
        xraind  = (ra0 - ragrid) / dra     + 0.5
        xdecind = (decgrid - dec0) / ddec  + 0.5
        gaiacart = gaiacart[xdecind.astype(int), xraind.astype(int)].T

        # gaiacart[0:int(gaiacart.shape[0]/2), :] = gaiacart[0:int(gaiacart.shape[0]/2), :] / 10

        limits = (azigrid.max(), azigrid.min(), elegrid.min(), elegrid.max())
        normcb = mpl.colors.LogNorm()
        plt.imshow(gaiacart, origin='lower', interpolation='nearest', cmap='bone', norm=normcb, extent=limits)
        plt.xlabel('Az')
        plt.ylabel('Alt')
        plt.show()
    
    return



