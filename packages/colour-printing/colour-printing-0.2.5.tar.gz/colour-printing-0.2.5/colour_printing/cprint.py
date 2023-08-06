from colour_printing.style import setting, Fore, Mode, Back


def cprint(*args, **kwargs):
    """
    :param args: 字符
    :param kwargs: 颜色参数
    :return:  彩色字符
    """
    if kwargs:
        mode = kwargs.get('mode')
        fore = kwargs.get('fore')
        back = kwargs.get('back')
    else:
        mode = Mode.BOLD
        fore = Fore.CYAN
        back = ''
    style = setting(mode=mode, fore=fore, back=back)
    str_temp = []
    for s in args:
        str_temp.append(f'{style[0]}{s}{style[1]}')
    print(*str_temp)
