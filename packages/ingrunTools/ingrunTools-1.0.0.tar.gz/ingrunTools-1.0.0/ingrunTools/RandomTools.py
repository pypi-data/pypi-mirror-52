import random


def get_random_list(max_1, length, min_1=0):
    """
        :function:   返回一个包含随机不重复整数的列表
                     - 栗子： print(get_random_list(10, 5, -10))
                             [1, 9, 4, -5 ,7]
        :param max_1:   最大值
        :param length:   返回的随机列表的长度
        :param min_1:   最小值 可不填 默认为0
        :return: []
        ***  1. 最大最小值之间的长度 应该比返回列表的长度要长  否则 会按照最大值与最小值之间的长度来返回列表
             2. 若最大值小于最小值， 则仅返回最小值 ： [min_1]
    """
    if max_1 < min_1:
        max_1 = min_1
    if max_1 - min_1 <= length:
        length = max_1 - min_1 + 1

    v = []
    while len(v) is not length:
        random.seed()
        k = random.randint(min_1, max_1)
        if not v.count(k):
            v.append(k)
    return v


def get_random_data_list(li, count):
    """
    function: 随机返回一个列表的一部分
    :param li:   源列表
    :param count:   需要返回的长度
    :return:   []
    *** : 1. 需要返回的长度不大于源列表长度，则返回源列表的长度

    """
    c = get_random_list(len(li) - 1, count)
    for index, i in enumerate(c):
        c[index] = li[i]
    return c


print(get_random_data_list([1, 2, 3, 4, 5], 15))
