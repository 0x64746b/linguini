from string import Template

from utils import classproperty


class Templates(object):

    _recipe_format = \
"""
\\begin{recipe}$header
$ingredients
\end{recipe}
"""

    _recipe_header_format = '{$title \creator{$creator}}{$num_dishes}{$prep_time}'

    _ingredient_format = """    \ingredient[$amount]{$unit}{$description}
        $processing
"""

    @classproperty
    @classmethod
    def recipe(cls):
        return Template(cls._recipe_format)

    @classproperty
    @classmethod
    def recipe_header(cls):
        return Template(cls._recipe_header_format)

    @classproperty
    @classmethod
    def ingredient(cls):
        return Template(cls._ingredient_format)
