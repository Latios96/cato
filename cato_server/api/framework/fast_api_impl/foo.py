import inspect


def my_func(my_arg, my_kwarg=None):
    print("my_arg: "+my_arg)
    print("my_kwarg: " + my_kwarg)
if __name__ == '__main__':
    contructed_args = {"my_arg": "42", "my_kwarg": "45", "wurst": "ffff"}
    args = inspect.getfullargspec(my_func)
    call_args = { your_key: contructed_args[your_key] for your_key in args.args }
    my_func(**call_args)