#! /usr/bin/env python
# -*- coding: utf-8 -*-
def color(raw_string, colour):
    """
    @returns a bold font
    usage: color("raw string here", 'red')
    """
    black = ('28', '1')
    red = ('31','1')
    green = ('32','1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(eval(colour)), raw_string)

if __name__ == "__main__":
    print color("this string","black")
