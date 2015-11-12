#!/usr/bin/env python

# Autocorrelation calculates how much the ciphertext agrees with itself with various offsets.
# For example: TYKZKLASFYYDKYCDERKFLRJKYAIFEUHSZERLRVJRT
#                   TYKZKLASFYYDKYCDERKFLRJKYAIFEUHSZERLRVJR
#                                     ^         ^     ^
# At an offset of 5, this text has an autocorrelation of 3 as there are 3 letter agreements.
# This is useful mainly for breaking Vigenere ciphers.


import graph as graphing
import text

class AutoCorrelation:
    display = None
    in_str = None
    title = None
    
    alph_upp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alph_low = "abcdefghijklmnopqrstuvwxyz"
    alph_upp_indexes = dict([(value, key) for (key, value) in enumerate(alph_upp)])
    alph_low_indexes = dict([(value, key) for (key, value) in enumerate(alph_low)])
    alph_length = len(alph_upp)
    
    def __init__(self, display, independent = True):
        self.display = display
        self.independent = independent
        if self.independent:
            self.display.add_menu_item(menu = '&Analysis', caption = '&Autocorrelation', function = self.run)
    
    def run(self, in_str = None, title = 'Autocorrelation'):
        if in_str is None:
            in_str = self.display.get_input()
        if in_str == '':
            return
        data = self.correlations(in_str)
        graph_data = [(i, count) for (i, count) in enumerate(data)]
        graph = graphing.Graph(graph_data, size = (485, 300), grid = True)
        image = graph.draw()
        self.display.show_image(image, title = title)
        return data
    
    def correlations(self, in_str):
        limit = 100
        in_str = text.clean(in_str, self.alph_upp + self.alph_low)
        offset_str = in_str
        data = [0] * (limit + 1)
        # This is the actual offsetty county bit.
        for offset in range(1, len(in_str) - 1):
            offset_str = offset_str[1:] + offset_str[0]
            for index, in_char in enumerate(in_str):
                if in_char == offset_str[index]:
                    data[offset] += 1
            if offset == limit:
                break
        return data
            
if __name__ == "__main__":
    a = AutoCorrelation(None, independent = False)
    in_str = """TYKZK LASFY YDKYC DERKF LRJKY AIFEU HSZER LRVJR
PNXKM ZAPKF LLVRQ AWVFZ AAZEC KPYFR VSFWR OEEVU
JIGYC YMRTF PNVRL KBVCG LVVZR VREFR HFLCJ ZEKFD
DIIZL NDZRE YADJR VGVKF LRNZR OTYVQ LTKZL NSWFP
AHVEC ETDFL AHRJD HRRJG RNFNM BRGIC ZEETC DAJEM
ADVKC JTVUR OEIVU HSEFQ PGEFD SIWVY UDZXS LSJFS
YDZMC YSZFL DOIBC KTYVJ VWMZQ PBZCG AYFER OEZTC
OECGC KTYVK HCYZL LIJKS KIVUU HSIVK HRBRZ SYLEQ
VPYZQ AITRR LDREB IOIVJ PTKCC YEJVK ILREA LTFKF
LTVEU OEVCP VTFIK HCYZL LOLIA VNKRA ASYRB SEULQ
AOVON LCKZR TAPSC AHRKY ZANVY AHVIQ AAKZM UMFUC
SIKYY ZBVVL REGKQ PMGCC AHVPK HYRCQ VHRMC IEVEU
VRIZC KTYRR PTNFS SDWRJ SIEKM LNVDW OAEUQ HNUKF
LRVWM YEYRT LIJJS LDFEJ FTYZQ WRFKM AYGVL VNVKF
LLVJQ AHVPQ LEDTM UVZEA LDFWG ASJVA BRZKW AIDVU
PLCKC SLZNG SLXZT LAWLJ SEIIC WOIKM UTYVQ ARLTR
BRVFD AHVDY JHZEC PTJFN LRRKG VNREB PTJTS YRVER
ZEKKG UGJZL TYEVV AMVJQ HGVSW AHVNY FIWFS UDKYC
LNTCM ZEUGJ HIEKC ETEVV ATFKF LMRTF PNVRL KIKCM
VKVUY ZTYFS NHZKU HSRSM BTKFZ LSVER PTDRW IENFP
AHCZQ AEEZL NOLKD VRKYC UEOKU LAKYC YSKRR POEKP
HNJDG ZSZFL PNKYC TERER PMVZU PLCRR AATBR OECRR
LSKJM CIVKK LSJRE LTYVW ZEVDR VHRMC ZCRCC KUGKF
LSVTS YIKPY NAZER OOLXF PDFER AHZEI AHZJM UELJC
ZTYVP VTFIK HCYZL LSFZR ZHFLJ KNKSC AOFJR LEG"""
    print a.correlations(in_str)
