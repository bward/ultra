import string

# This is a cipher class which can be used as a base for all the ciphers and overloaded.
# So you can quickly knock together a new cipher algorithm.

class Metacipher:
    title = 'Metacipher'
    caption = '&Metacipher'
    solve = False
    
    _display = None
    _in = None
    _out = None
    _key = None
    _encryption = False
    _independent = None
        
    def __init__(self, display = None, independent = True):
        self._independent = independent
        self._display = display
        if self._independent:
            self.menus()            
    
    def menus(self):
        self._display.add_menu_item(menu = '&Ciphers', caption = self.caption, function = self._cipher_callback)
        if self.solve:
            self._display.add_menu_item(menu = '&Solve', caption = self.caption, function = self._solve_callback)
        
    
    def encrypt(self = None, key = '', in_str = ''):
        return str((key, in_str))
    
    def decrypt(self = None, key = '', in_str = ''):
        return str((key, in_str))
    
    def crack_key(self = None, in_str = ''):
        return ''
    
    def _solve_callback(self):
        self.run(key_specified = False)
    
    def _cipher_callback(self):
        self.run(key_specified = True)
    
    def sanitize_key(self, key):
        return key
    
    def _perform(self, key, in_str):
        self._key = key[0]
        self._encryption = key[1]
        if self._encryption:
            out_str = self.encrypt(self._key, in_str)
        else:
            out_str = self.decrypt(self._key, in_str)
        return out_str
    
    def ask_for_key(self, key = ''):
        if self._display == None:
            return None
        rvalues, tvalues = self._display.key_dialog(radioboxes = [['Decrypt', 'Encrypt']], textboxes = [(self.title + ' key', key)], title = self.title + ' key')
        key = self.sanitize_key(tvalues[0])
        encryption = (rvalues[0] == 1)
        return key, encryption
    
    def run(self, key_specified = True):
        if self._display == None:
            return None
        self._in = self._display.get_input()
        key = ''
        if not key_specified:
            title = self.title + ': "' + string.strip(self._in[0:10]) + '"'
            key = self.crack_key(self._in)
        self._key_raw = self.ask_for_key(str(key))
        if None in self._key_raw:
            return
        self._out = self._perform(self._key_raw, self._in)
        self._display.show_output(self._out)
