
class Color(dict):
    _color_keys = ['r', 'g', 'b', 'a']
    def __init__(self, initdict=None, **kwargs):
        if initdict is None:
            initdict = {}
        initdict.setdefault('r', 0.)
        initdict.setdefault('g', 1.)
        initdict.setdefault('b', 0.)
        initdict.setdefault('a', 1.)
        super(Color, self).__init__(initdict, **kwargs)
    def copy(self):
        return Color({key:self[key] for key in self._color_keys})
    def from_list(self, l):
        for i, val in enumerate(l):
            key = self._color_keys[i]
            self[key] = val
    def to_list(self):
        return [self[key] for key in self._color_keys]
    def to_hex(self, include_alpha=False):
        keys = self._color_keys
        if not include_alpha:
            keys = keys[:3]
        vals = [int(self[key] * 255) for key in keys]
        hexstr = ['#']
        for v in vals:
            s = hex(v).split('0x')[1]
            if len(s) == 1:
                s = '0%s' % (s)
            hexstr.append(s)
        return ''.join(hexstr)
    @classmethod
    def from_hex(cls, hexstr):
        hexstr = hexstr.split('#')[1]
        d = {}
        i = 0
        while len(hexstr):
            s = '0x%s' % (hexstr[:2])
            key = cls._color_keys[i]
            d[key] = float.fromhex(s) / 255.
            if len(hexstr) > 2:
                hexstr = hexstr[2:]
            else:
                break
            i += 1
        return cls(d)
    def __eq__(self, other):
        if isinstance(other, Color):
            other = other.to_list()
        elif isinstance(other, dict):
            other = Color(other).to_list()
        elif isinstance(other, (list, tuple)):
            other = list(other)
        else:
            return NotImplemented
        self_list = self.to_list()
        if len(other) < 3:
            return False
        elif len(other) == 3:
            if self['a'] != 1:
                return False
            return self_list[:3] == other
        return self_list == other
    def __ne__(self, other):
        eq = self.__eq__(other)
        if eq is NotImplemented:
            return eq
        return not eq
    def __repr__(self):
        return '<{self.__class__}: {self}>'.format(self=self)
    def __str__(self):
        return str(self.to_list())
