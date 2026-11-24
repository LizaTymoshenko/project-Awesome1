# decorator function
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return str(e)

    #  except Exception:
    #      return "Something went wrong"
    return wrapper