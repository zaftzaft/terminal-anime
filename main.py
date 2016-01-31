#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import argparse
import curses

from PIL import Image
from drawille import Canvas


def pad(s, w):
    if len(s) < w:
        s += (" " * (w - len(s) - 1))
    return s


def main(args, opts):
    curses.use_default_colors()
    curses.curs_set(0)

    win = curses.initscr()

    source = Image.open(opts.filename)

    c = Canvas()

    try:
        while True:
            (wh, ww) = win.getmaxyx()

            try:
                source.seek(source.tell() + 1)
            except:
                if opts.onetime:
                    break
                source.seek(0)

            img = (source
                    .resize(((ww - 1) * 2, wh * 4))
                    .convert("1")
                    )
            w = img.width

            (x, y) = (0, 0)
            for v in img.getdata():

                if opts.reverse:
                    if not v:
                        c.set(x, y)

                else:
                    if v:
                        c.set(x, y)

                x += 1

                if w <= x:
                    x = 0
                    y += 1

            for r in range(wh):
                line = c.rows(min_y=(r*4), max_y=((r+1)*4))[0]
                win.addnstr(r, 0, pad(line, ww), ww)

            win.refresh()
            c.clear()
            time.sleep(opts.interval)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Terminal Animation")

    parser.add_argument("filename", help="Source filename (anime-gif)")

    parser.add_argument("-n", "--interval", type=float, default=0.1)
    parser.add_argument("-r", "--reverse", action="store_true")
    parser.add_argument("-1", "--onetime", action="store_true")

    args = parser.parse_args()

    curses.wrapper(main, args)
