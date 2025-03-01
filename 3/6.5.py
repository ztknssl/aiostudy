def is_palindrome(string_: str):
    string_ = string_.strip().replace(' ', '').casefold()
    return string_ == string_[::-1]
