class Utils:

    silent = False

    def log(*args, **kwargs):
        if not Utils.silent:
            print(*args, **kwargs)