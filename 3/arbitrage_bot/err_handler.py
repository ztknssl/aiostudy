import requests

# Декоратор для отлова исключений
def error_catcher(function):
    def new_func(*args, **kwargs):
        msg = f'An error occurred in: {function.__name__}'
        try:
            return function(*args, **kwargs)
        except requests.RequestException as err:
            print(msg)
            print(f'Request error: {err}')
        except Exception as err:
            print(msg)
            print(f'Other error: {err}')

    return new_func