Lib for checking types of functions arguments and returning data to accordance with annotating
===================

Installation:

    pip install pystatity

Usage:

    from pystatity import strict_types

    @strict_types
    def your_func(one: str, two: int ) -> tuple:
        return one, two

    your_func('one', 2)         # ok

    your_func('one', 'two')     # will raise WrongParametersType exception

