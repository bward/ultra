# Global variables
_alph = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')
_alph_indexes = tuple([dict([(value, key) for (key, value) in enumerate(alph)]) for alph in _alph])
_alph_length = len(_alph[0])
