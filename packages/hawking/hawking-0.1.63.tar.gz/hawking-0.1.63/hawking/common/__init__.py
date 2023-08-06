from hawking.common.color import *


def bold(skk):
    print_color(skk, bold=True, color=LIGHT_YELLOW)


def info(skk):
    print_color(skk, color=LIGHT_CYAN)


def hilite(skk):
    print_color(skk, underline=True, color=LIGHT_GREEN)
