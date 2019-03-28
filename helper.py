
def import_check(module):

    try:

        __import__(module)

        return True

    except ImportError:

        return False