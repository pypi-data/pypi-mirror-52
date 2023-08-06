#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################
#
#  OCR TOOLS - Making climate data malleable
#  Copyright (C) 2018 Andres Chang
#
########################################

import numpy as np
import xarray as xr
import time
import pandas as pd


def xr_load(path, average=False, standardize=True, **kwargs):
    """
    Loads a netCDF and fixes date convention for CESM-LE or other Gregorian
    calendar data

    Args:
    * path (str): path to data
    * dt (str): daily or monthly (for standardization)
    * average (bool): whether to align based on average of adjacent timestamps
    (for standardization)
    """
    d = xr.open_dataset(path)

    try:
        average = kwargs["average"]
        if average:
            dt = kwargs['dt']
            fby = 'MS' if dt == 'monthly' else 'D'
            t = d['time'].to_index()

            if average:
                deltas = np.roll(np.diff(t), 1)
                td = np.append((t[:-1] - deltas / 2), t[-1] - deltas[0] / 2)

            d.coords['time'] = td
    except KeyError:
        pass

    if standardize:
        d = noleap_2_datetime(d, **kwargs)

    return(d)


def noleap_2_datetime(data, **kwargs):

    dt0 = int(data.time[1] - data.time[0])
    dt = 'daily' if dt0 < 2.3e15 else 'monthly'
    by, fby = get_groupings(dt)
    t = data['time']

    try:
        yr0, yrf = np.amin(t.to_index().year), np.amax(t.to_index().year)
    except TypeError:
        yr0, yrf = np.amin(t.to_index()).year, np.amax(t.to_index()).year
    yrs = np.arange(yr0, yrf + 1)

    for yr in yrs:
        ti = t.sel(time=slice(f4(yr) + '-01-01', f4(yr) + '-12-31'))
        try:
            td = td.append(
                pd.date_range(f4(yr) + '-01-01', freq=fby, periods=len(ti)))
        except NameError:
            td = pd.date_range(f4(yr) + '-01-01', freq=fby, periods=len(ti))

        fixed = True

    if dt == 'daily':
        for di in range(len(td)):
            if td[di - 1].is_leap_year and di == len(td):
                td = td.insert(
                    di, pd.to_datetime(f4(yrf) + '-12-31'))
            else:
                day = td[di]
                if day.is_leap_year and day.dayofyear == 60:
                    td = td[0: di].append(td[di + 1:])
                    fixed = False
                elif not day.is_leap_year and fixed is False:
                    td = td.insert(
                        di, pd.to_datetime(f4(day.year - 1) + '-12-31'))
                    fixed = True

    data.coords['time'] = td
    return(data)


def convert_lon(degrees_lon, east=True):
    if east:
        if degrees_lon < 0.:
            deg_out = 360 + degrees_lon
        else:
            deg_out = degrees_lon
    else:
        if degrees_lon > 180.:
            deg_out = degrees_lon - 360
        else:
            deg_out = degrees_lon
    return(deg_out)


def standardize_coords(dataset, center=True):
    """
    Standardize coordinates of an xarray dataset (i.e. make sure that there
    are coordinates named lat, lon, and time, which can be specified from
    other namings)

    Args:
    * dataset (xarray.Dataset)
    * center (bool): True by default - uses TLAT/TLON if multiple coordinate
    systems. If False, uses ULAT/ULON (case insensitive)
    """

    for ci in ['lat', 'lon']:
        if ci not in dataset.coords:
            c_options = [x for x in dataset.coords if ci in x.lower()]

            if len(c_options) == 1:
                c_key = c_options[0]
            elif len(c_options) > 1:
                try_tc = [x for x in c_options if 't' in
                          x.lower().replace('lat', 'la')]
                try_uc = [x for x in c_options if 'u' in str.lower(x)]
                if center and len(try_tc) == 1:
                    c_key = try_tc[0]
                elif center is False and len(try_uc) == 1:
                    c_key = try_uc[0]

            try:
                c_key
            except NameError:
                print(dataset.coords)
                c_key = input('Please enter ' + ci +
                              ', as shown in the original coordinate list: ')

            dataset.coords[ci] = dataset.coords[c_key]

    return(dataset)


def load(data, var=[], interactive=True, drop=True, **kwargs):
    """
    Return a dataset with standardized coordinate names for easy querying

    Args:
    * data (str or xarray.Dataset): either an xarray dataset or a path to
    netCDF that will be read in by xr_load function
    * var (list or str): list of desired variable or main var (optional)
    * interactive (bool): instructions for the less-experienced programmer :)
    * drop (bool): if True and var specified, other data_vars are removed from
    the dataset
    """

    # Load xarray dataset
    if isinstance(data, str):
        ds = xr_load(data, **kwargs)
    elif isinstance(data, xr.core.dataset.Dataset):
        ds = data
    else:
        raise TypeError(
            "data argument must be a path to a netCDF or xarray dataset")

    # Add an attribute for main_vars
    if isinstance(var, str):
        var = [var]
    elif isinstance(var, list):
        var = var
    else:
        raise TypeError(
            "var argument must be a string or list indicating the main" +
            " variable, if any")

    # Specify in command line, if interactive set to True
    if interactive and var == []:
        if len(ds.data_vars) > 1:
            print("\n[OCR] Variables in dataset: ", ', '.join(
                  [x for x in ds.data_vars]))
            v0 = input('\n[OCR] Please enter a main variable or multiple main' +
                       ' variables separated by commas; or type HELP: ')

            if v0 == 'HELP':
                # Print variables upon request before confirming selection
                request = input(
                    '\n[OCR] Type a variable to see its associated data: ')
                while request != 'YES':
                    var = [request]
                    print(ds[request])
                    time.sleep(1.5)
                    request = input(
                        '\n[OCR] Is this the main variable? Type YES or ' +
                        'type another variable to see its associated data: ')

            else:
                if ',' in v0:
                    var = [s.strip() for s in v0.split(',')]
                elif isinstance(v0, str):
                    var = [v0]
        else:
            var = list(ds.data_vars)
            print('\n[OCR] Main variable: ' + var[0])
            print(ds[var[0]])
    elif var == []:
        var = list(ds.data_vars)

    # Standardize coordinate names
    try:
        ds = standardize_coords(ds, center=kwargs['center'])
    except KeyError:
        ds = standardize_coords(ds)

    if drop:
        ds = ds[var]

    if interactive:
        print('\n[OCR] Load complete. Dataset contents:')
        print(ds)

    return(ds)


def subset(dataset, scope):
    """
    Returns a subsetted dataset based on scope
    Args:
    * dataset (xarray.Dataset)
    * scope (ocrtools.scope)
    """

    scope_keys = [x for x in scope.__dict__.keys()]

    # First subset year range
    t0 = scope.yr0 + \
        '-01-01' if scope.yr0 is not None else np.min(dataset['time'])
    tf = scope.yrf + \
        '-12-31' if scope.yrf is not None else np.max(dataset['time'])
    d_subset = dataset.sel(time=slice(t0, tf))

    def box_subset(d_in, lat_min, lat_max, lon_min, lon_max):
        d_out = d_in.where(
            (d_in.lat >= lat_min) &
            (d_in.lat <= lat_max) &
            (d_in.lon >= lon_min) &
            (d_in.lon <= lon_max), drop=True)
        return(d_out)

    try:
        # Subset based on tk_selection
        box_subs = []
        for box_i in scope.tk_selection:
            lat_min, lat_max = sorted([box_i[0], box_i[2]])
            lon_min, lon_max = sorted([box_i[1], box_i[3]])
            d_subset_i = box_subset(d_subset, lat_min, lat_max,
                                    lon_min, lon_max)
            box_subs.append(d_subset_i)

        d_subset = xr.merge(box_subs)

    except AttributeError:
        try:
            # subset based on location
            d_subset = d_subset.sel(
                lat=scope.lat, lon=scope.lon, method='nearest')

        except AttributeError:
            # Subset based on coordinat min/max
            try:
                d_subset = box_subset(d_subset, scope.lat_min, scope.lat_max,
                                      scope.lon_min, scope.lon_max)
            except AttributeError:
                pass

    if 'z_max' in scope_keys:
        d_subset = d_subset.where(d_subset.z <= scope.z_max, drop=True)
    if 'z_min' in scope_keys:
        d_subset = d_subset.where(d_subset.z >= scope.z_min, drop=True)
    d_subset.attrs = dataset.attrs
    print('\n[OCR] Subset complete. Dataset contents:')
    print(d_subset)

    return(d_subset)


class scope(object):
    """
    Class that is used to subset data in space and time

    Args:
    * interactive (bool): instructions for the less-experienced programmer :)
    * kwargs: lat_min, lat_max, lon_min, lon_max are always defined
    to some extent. If z_min and z_max are included as keywords, they will also
    be used added as attributes to the scope object
    """

    def __init__(self, interactive=True, tk_select=True, lon_convert=False,
                 **kwargs):

        scopes = ['yr0', 'yrf', 'lat_min', 'lat_max', 'lon_min', 'lon_max',
                  'location', 'lat', 'lon']
        none_vals = {'lat_min': -90, 'lat_max': 90, 'lon_min': -180,
                     'lon_max': 180, 'yr0': None, 'yrf': None}

        if((interactive and any(x not in kwargs for x in scopes))
           or (all(x not in kwargs for x in scopes[2:]) and tk_select)):
            print("\n[OCR] Creating new scope object")

        # If no lat/lon values are provided and tk_select is True, open a
        # map window and prompt the user select area with rectangles
        if all(x not in kwargs for x in scopes[2:]) and tk_select:
            scopes = scopes[0:2] + ['tk_selection']
        elif 'location' in kwargs:
            self.location = kwargs['location']
            scopes = scopes[0:2] + ['location']
        elif 'lat' in kwargs and 'lon' in kwargs:
            scopes = scopes[0:2] + scopes[-2:]
        else:
            scopes = scopes[0:6]

        try:
            if(kwargs['z_min']):
                scopes = scopes + ['z_min']
        except KeyError:
            pass
        try:
            if(kwargs['z_max']):
                scopes = scopes + ['z_max']
        except KeyError:
            pass

        for ai in scopes:
            if ai == 'tk_selection':
                print("Select area(s) on map and then close the" +
                      " pop-up window")
                from ocrtools.tk_selector import get_dims
                setattr(self, ai, get_dims())
            elif ai == 'location':
                from geopy import Nominatim
                geolocator = Nominatim()
                geo_loc = geolocator.geocode(self.location)
                self.lat = geo_loc.latitude
                self.lon = convert_lon(geo_loc.longitude)
            else:
                try:
                    setattr(self, ai, kwargs[ai])

                except KeyError:
                    if interactive:
                        lim0 = input('Enter ' + ai + ': ')
                        if lim0 == '':
                            lim0 = none_vals[ai]
                        else:
                            lim0 = float(lim0)
                        setattr(self, ai, lim0)
                    else:
                        setattr(self, ai, none_vals[ai])

            # Convert lon values, if needed
            if 'lon' in ai:
                if lon_convert:
                    setattr(self, ai, convert_lon(getattr(self, ai)))
            if 'yr' in ai and getattr(self, ai) is not None:
                setattr(self, ai, '{:04d}'.format(int(getattr(self, ai))))

        if(interactive or tk_select):
            print("\n[OCR] Finished writing new scope object")


def f4(num): return "{:04d}".format(num)


def get_groupings(dt):
    if dt == 'monthly':
        by = 'time.month'
        fby = 'MS'
    elif dt == 'daily':
        by = 'time.date'
        fby = 'D'
    return(by, fby)
