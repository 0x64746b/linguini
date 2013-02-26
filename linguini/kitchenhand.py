import gtk
import gobject
import sys
import signal
import logging

from data import Recipe, Ingredient

# module wide logger instance
logger = logging.getLogger(__name__)


class State(object):
    (TITLE, CREATOR, NUM_DISHES, PREP_TIME, INGREDIENTS,
     INGREDIENT, AMOUNT, UNIT, PROCESSING,
     DONE) = range(10)

    _prompts = { TITLE: "What is the title of the recipe?",
                 CREATOR: "Who created this recipe?",
                 NUM_DISHES: "How many dishes does this recipe serve?",
                 PREP_TIME: "How long does it take to prepare and cook this recipe?",
                 INGREDIENTS: "Please enter an ingredient:",
                 INGREDIENT: "Which ingredient do you want to add? (Ctrl+C to abort)",
                 AMOUNT: "How much do you want to add of this ingredient?",
                 UNIT: "What is the unit of this ingredient?",
                 PROCESSING: "What should be done with the ingredients?", }

    def __init__(self):
        self._current = State.TITLE

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, state):
        self._current = state

    def prompt(self):
        print(State._prompts[self._current])

    def advance(self):
        self._current += 1
        self.prompt()


class KitchenHand(object):
    SIGNAL_NEW_CLIPBOARD_CONTENT = 'owner-change'

    def __init__(self, output_file):
        self._output_file = output_file

        self._recipe = Recipe()
        self._state = State()

        self._watch_inputs()
        signal.signal(signal.SIGINT, self._handle_SIGINT)

        self._state.prompt()

    def _watch_inputs(self):
        self._watch_clipboard()
        self._watch_stdin()

    def _watch_clipboard(self):
        self.clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_PRIMARY)
        self.clipboard.connect(self.SIGNAL_NEW_CLIPBOARD_CONTENT,
                               self._handle_clipboard_content)

    def _watch_stdin(self):
        gobject.io_add_watch(sys.stdin, gobject.IO_IN,
                             self._handle_stdin_content)

    def _handle_clipboard_content(self, clipboard, event):
        selection = clipboard.wait_for_text()
        print selection    # provide feedback for the user
        self._process_input(selection)

    def _handle_stdin_content(self, stdin, condition):
        value = stdin.readline()
        self._process_input(value)
        return True

    def _handle_SIGINT(self, signal, frame):
        logger.debug("caught SIGINT")
        if self._state.current in [State.INGREDIENTS,
                                   State.INGREDIENT,
                                   State.AMOUNT,
                                   State.UNIT,
                                   State.PROCESSING]:
            self._state.current = State.DONE
            self._process_input(None)
        else:
            logger.debug("Quitting while in state '{}'".format(
                self._state.current))
            gtk.main_quit()

    def _process_input(self, value):
        if value: value = value.strip()
        logger.debug("processing input '{}' in state {}".format(
            value, self._state.current))

        if self._state.current == State.TITLE:
            self._recipe.title = value
            self._state.advance()
        elif self._state.current == State.CREATOR:
            self._recipe.creator = value
            self._state.advance()
        elif self._state.current == State.NUM_DISHES:
            self._recipe.num_dishes = value
            self._state.advance()
        elif self._state.current == State.PREP_TIME:
            self._recipe.prep_time = value
            self._state.current = State.INGREDIENTS
            self._process_input(None)
        elif self._state.current == State.INGREDIENTS:
            self._ingredient = Ingredient()
            self._state.prompt()
            self._state.advance()
        elif self._state.current == State.INGREDIENT:
            self._ingredient.description = value
            self._state.advance()
        elif self._state.current == State.AMOUNT:
            self._ingredient.amount = value
            self._state.advance()
        elif self._state.current == State.UNIT:
            self._ingredient.unit = value
            self._state.advance()
        elif self._state.current == State.PROCESSING:
            self._ingredient.processing = value
            self._recipe.add(self._ingredient)
            self._state.current = State.INGREDIENTS
            self._process_input(None)
        else:
            self._write()
            self._exit()

    def _write(self):
        recipe = self._recipe.render()
        output = open(self._output_file, 'w')
        output.write(recipe)
        output.close()

    def _exit(self):
        print "We're done!"
        sys.exit()

