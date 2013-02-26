from string import Template
import logging


# module wide logger instance
logger = logging.getLogger(__name__)


class Recipe(object):

    _recipe_format = \
"""
\\begin{recipe}$header
$ingredients
\end{recipe}
"""

    _header_format = '{$title \creator{$creator}}{$num_dishes}{$prep_time}'

    def __init__(self):
        self._ingredients = []

    @property
    def title(self): pass

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def creator(self): pass

    @creator.setter
    def creator(self, creator):
        self._creator = creator

    @property
    def num_dishes(self): pass

    @num_dishes.setter
    def num_dishes(self, num_dishes):
        self._num_dishes = num_dishes

    @property
    def prep_time(self): pass

    @prep_time.setter
    def prep_time(self, prep_time):
        self._prep_time = prep_time

    def add(self, ingredient):
        self._ingredients.append(ingredient)

    def render(self):
        logger.debug("Rendering recipe")
        header = self._render_header()
        ingredients = self._render_ingredients()

        template = Template(Recipe._recipe_format)
        return template.substitute(header=header, ingredients=ingredients)

    def _render_header(self):
        logger.debug("Rendering header")
        template = Template(Recipe._header_format)
        return template.substitute(title=self._title,
                                   creator=self._creator,
                                   num_dishes=self._num_dishes,
                                   prep_time=self._prep_time)

    def _render_ingredients(self):
        logger.debug("Rendering ingredients")
        ingredients = ""
        for ingredient in self._ingredients:
            ingredients += ingredient.render()
        return ingredients


class Ingredient(object):

    _format = """    \ingredient[$amount]{$unit}{$description}
        $processing
"""

    @property
    def amount(self): pass

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def unit(self): pass

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    @property
    def description(self): pass

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def processing(self): pass

    @processing.setter
    def processing(self, processing):
        self._processing = processing

    def render(self):
        template = Template(Ingredient._format)
        return template.substitute(amount=self._amount,
                                   unit=self._unit,
                                   description=self._description,
                                   processing=self._processing)
