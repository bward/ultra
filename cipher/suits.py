# -*- coding: UTF-8 -*-

# I believe this is something to do with Solitaire. I don't think it's actually called from anything though.
# Ben: is this safe to delete?

import sys
def num_to_card(num):
    if num <= 0:
        return 'no card'
    pos = num % 13
    suit = (num-1)/13
    positions = 'A234567890JQK'
    suits = 'CDHS'
    if num == 53:
        return 'joker1'
    elif num == 54:
        return 'joker2'

    return positions[pos-1] + suits[suit]

if __name__ == '__main__':
    num_to_card(int(sys.argv[1]))
