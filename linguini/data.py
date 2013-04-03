import logging

from templates import Templates


# module wide logger instance
logger = logging.getLogger(__name__)


class Recipe(object):

    def __init__(self, image):
        self._image_name = image
        self._ingredients = []

    @property
    def title(self):
        pass

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def creator(self):
        pass

    @creator.setter
    def creator(self, creator):
        self._creator = creator

    @property
    def num_dishes(self):
        pass

    @num_dishes.setter
    def num_dishes(self, num_dishes):
        self._num_dishes = num_dishes

    @property
    def prep_time(self):
        pass

    @prep_time.setter
    def prep_time(self, prep_time):
        self._prep_time = prep_time

    def add(self, ingredient):
        self._ingredients.append(ingredient)

    def render(self):
        logger.debug("Rendering recipe")
        header = self._render_header()
        image = self._render_image()
        ingredients = self._render_ingredients()

        template = Templates.recipe
        return template.substitute(header=header, image=image,
                                   ingredients=ingredients)

    def _render_header(self):
        logger.debug("Rendering header")
        template = Templates.recipe_header
        return template.substitute(title=self._title,
                                   creator=self._creator,
                                   num_dishes=self._num_dishes,
                                   prep_time=self._prep_time)

    def _render_image(self):
        image = ''
        if self._image_name:
            template = Templates.image
            image = template.substitute(image=self._image_name)
        return image

    def _render_ingredients(self):
        logger.debug("Rendering ingredients")
        ingredients = ""
        for ingredient in self._ingredients:
            ingredients += ingredient.render()
        return ingredients


class Ingredient(object):

    @property
    def amount(self):
        pass

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def unit(self):
        pass

    @unit.setter
    def unit(self, unit):
        self._unit = unit

    @property
    def description(self):
        pass

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def processing(self):
        pass

    @processing.setter
    def processing(self, processing):
        self._processing = processing

    def render(self):
        template = Templates.ingredient
        return template.substitute(amount=self._amount,
                                   unit=self._unit,
                                   description=self._description,
                                   processing=self._processing)
