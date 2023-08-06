#! /usr/bin/python
# -*- coding: utf-8 -*-



class AstroSource(object):
    """ Astrophysical source class

        Kind of a wrapper over `astropy.SkyCoord`
    """
    def __init__(c1, c2, frame='icrs'):
        self.frame = frame

    @property
    def frame(self):
        return self._frame
    @frame.setter
    def frame(self, f):
        assert isinstance(f, str), 'Frame should be a string.'
        from astropy.coordinates.baseframe import frame_transform_graph
        self._frame = f.lower()
        fnames = frame_transform_graph.get_names()
        if self._frame not in fnames:
            raise ValueError('{} not a referenced frame name: {}'
                .format(self._frame, fnames))
        return

    