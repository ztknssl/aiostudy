def is_palindrome(string_: str) -> bool | None:
    try:
        string_ = string_.strip().replace(' ', '').casefold()
        return string_ == string_[::-1]
    except AttributeError as e:
        print(f'Нужно ввести строку: {e}')
