import os

global_val = 5


def abs_num(num):
    """
    :frd: input(-1) return(1)
    :frd: input(1) return(1)
    """
    cur_path = os.getcwd()
    print(cur_path)
    return abs(num)


def get_global():
    """
    :frd: return(5)
    """
    return global_val;


def sum_int(a, b):
    """
    :frd: input(1,2) return(3)
    :frd: input(2,5) return(7)
    """
    return a + b


def multiply_five_numver(a, b, c, d, e):
    """
    :frd: input(1,2,3,1,1) return(6)
    frd input(1,2,3,1,0) return(0)
    """
    return a*b*c*d*e


def handle_list(list_1):
    """
    :frd: input([1,2,3,4,5]) return([3,4,5,6,7])
    frd input([0]) return([2])
    """
    return [item + 2 for item in list_1]

def use_new_format(a, b, c):
    """
    :param a:
    :param b:
    :param c:
    :return:
    """
    return True

if __name__ == '__main__':
    print(handle_list.__doc__)
    print(use_new_format.__doc__)
    print([item for item in handle_list.__doc__.splitlines() if item])