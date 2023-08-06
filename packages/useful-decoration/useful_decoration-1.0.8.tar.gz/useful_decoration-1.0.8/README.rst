useful-decoration
-----------------

Description
-----------

    I wrote some decorators that are commonly used in my work. And give
    an example if the decorator is used.

Installing
-----------

Install and update using `pip`_:


.. code:: python

    pip install  useful-decoration

Simples
_______

.. code-block:: python


    from useful_decoration.decorations import element_mapping


    class Person:

        def __init__(self, name):
            self.name = name

        @element_mapping(factor_name="factor")
        def calculate(self):
            return 10


    if __name__ == '__main__':
        p = Person(name='frank')

        print(p.calculate())  # {'factor': 10}

Links
_____

pypi address https://pypi.org/project/useful-decoration/



.. _pip: https://pip.pypa.io/en/stable/quickstart/
