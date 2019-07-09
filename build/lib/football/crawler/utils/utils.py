def float_num(x, count=2):
    """
    :param x: 传进来的参数
    :param count: 保留的小数位数
    :return: 结果
    """
    ss = "%." + str(count) + "f"
    return float(ss % x)


