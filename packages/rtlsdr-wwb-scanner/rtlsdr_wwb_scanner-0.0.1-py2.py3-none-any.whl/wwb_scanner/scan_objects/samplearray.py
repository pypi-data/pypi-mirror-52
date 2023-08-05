import numpy as np
from scipy.interpolate import CubicSpline
import jsonfactory

from wwb_scanner.core import JSONMixin
from wwb_scanner.utils import dbmath

class SampleArray(JSONMixin):
    dtype = np.dtype([
        ('frequency', np.float64),
        ('iq', np.complex128),
        ('magnitude', np.float64),
        ('dbFS', np.float64)
    ])
    def __init__(self, data=None, keep_sorted=True):
        self.keep_sorted = keep_sorted
        if data is None:
            data = np.empty([0], dtype=self.dtype)
        self.data = data
        if keep_sorted:
            self.data = np.sort(self.data, order='frequency')
    @classmethod
    def create(cls, keep_sorted=True, **kwargs):
        data = kwargs.get('data')
        obj = cls(data, keep_sorted=keep_sorted)
        if not obj.data.size:
            obj.set_fields(**kwargs)
        return obj
    def set_fields(self, **kwargs):
        f = kwargs.get('frequency')
        if f is None:
            raise Exception('frequency array must be provided')
        if not isinstance(f, np.ndarray):
            f = np.array([f])
        data = np.zeros(f.size, dtype=self.dtype)
        data['frequency'] = f
        for key, val in kwargs.items():
            if key not in self.dtype.fields:
                continue
            if key == 'frequency':
                continue
            if not isinstance(val, np.ndarray):
                val = np.array([val])
            data[key] = val

        if data is None:
            return

        iq = kwargs.get('iq')
        mag = kwargs.get('magnitude')
        dbFS = kwargs.get('dbFS')

        if iq is not None and mag is None:
            mag = data['magnitude'] = np.abs(iq)
        if dbFS is not None and mag is None:
            mag = data['magnitude'] = dbmath.from_dB(dbFS)
        if mag is not None and dbFS is None:
            data['dbFS'] = dbmath.to_dB(mag)

        self.append(data)
    def __getattr__(self, attr):
        if attr in self.dtype.fields.keys():
            return self.data[attr]
        raise AttributeError
    def __setattr__(self, attr, val):
        if attr in self.dtype.fields.keys():
            self.data[attr] = val
        super(SampleArray, self).__setattr__(attr, val)
    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def __len__(self):
        return len(self.data)
    def __iter__(self):
        return iter(self.data)
    @property
    def size(self):
        return self.data.size
    @property
    def shape(self):
        return self.data.shape
    def _check_obj_type(self, other):
        if isinstance(other, SampleArray):
            data = other.data
        else:
            if isinstance(other, np.ndarray) and other.dtype == self.dtype:
                data = other
            else:
                raise Exception('Cannot extend this object type: {}'.format(other))
        return data
    def append(self, other):
        if self.keep_sorted:
            self.insert_sorted(other)
        else:
            data = self._check_obj_type(other)
            self.data = np.append(self.data, data)
    def insert_sorted(self, other):
        data = self._check_obj_type(other)
        in_ix_self = np.flatnonzero(np.in1d(self.frequency, data['frequency']))
        in_ix_data = np.flatnonzero(np.in1d(data['frequency'], self.frequency))
        if in_ix_self.size:
            self.iq[in_ix_self] = np.mean([
                self.iq[in_ix_self], data['iq'][in_ix_data]
            ], axis=0)
            self.magnitude[in_ix_self] = np.mean([
                self.magnitude[in_ix_self], data['magnitude'][in_ix_data]
            ], axis=0)
            self.dbFS[in_ix_self] = np.mean([
                self.dbFS[in_ix_self], data['dbFS'][in_ix_data]
            ], axis=0)

        nin_ix = np.flatnonzero(np.in1d(data['frequency'], self.frequency, invert=True))

        if nin_ix.size:
            d = np.append(self.data, data[nin_ix])
            d = np.sort(d, order='frequency')
            self.data = d
    def smooth(self, window_size):
        x = self.magnitude
        w = np.hanning(window_size)

        s = np.r_[x[window_size-1:0:-1], x, x[-2:-window_size-1:-1]]

        y = np.convolve(w/w.sum(), s, mode='valid')
        m = y[(window_size//2-1):-(window_size//2)]

        if m.size != x.size:
            raise Exception('Smooth result size {} != data size {}'.format(m.size, x.size))

        self.data['magnitude'] = m
        self.data['dbFS'] = dbmath.to_dB(m)
    def interpolate(self, spacing=0.025):
        fmin = np.ceil(self.frequency.min())
        fmax = np.floor(self.frequency.max())

        x = self.frequency
        y = self.magnitude
        cs = CubicSpline(x, y)
        xs = np.arange(fmin, fmax+spacing, spacing)
        n_dec = len(str(spacing).split('.')[1])
        xs = np.around(xs, n_dec)

        ys = cs(xs)
        data = np.zeros(xs.size, dtype=self.dtype)
        data['frequency'] = xs
        data['magnitude'] = ys
        data['dbFS'] = dbmath.to_dB(ys)
        self.data = data

    def _serialize(self):
        return {'data':self.data, 'keep_sorted':self.keep_sorted}
    def __repr__(self):
        return '<{self.__class__.__name__}: {self}>'.format(self=self)
    def __str__(self):
        return str(self.data)

@jsonfactory.register
class JSONEncoder(object):
    def encode(self, o):
        if isinstance(o, SampleArray):
            d = o._serialize()
            d['__class__'] = o.__class__.__name__
            return d
        return None
    def decode(self, d):
        if d.get('__class__') == 'SampleArray':
            return SampleArray(d['data'], d['keep_sorted'])
        return d
