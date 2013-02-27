from string import Template

from utils import classproperty


class Templates(object):

    _document_format = \
r"""
\documentclass[a4paper,10pt]{article}

\usepackage{ngerman}
\usepackage[utf8]{inputenc}

\usepackage{graphicx}

\usepackage[index,nonumber]{cuisine}

% Some styling of the recipe
%% \RecipeWidths{Total}{Number}{Number of servings}{Ingredient}{Quantity}{Units}
\RecipeWidths{\textwidth}{0.5cm}{3cm}{3.75cm}{.75cm}{1.75cm}

\renewcommand*{\recipetitlefont}{\large\bfseries\sffamily}
\renewcommand*{\recipequantityfont}{\sffamily\bfseries}
\renewcommand*{\recipeunitfont}{\sffamily}
\renewcommand*{\recipeingredientfont}{\sffamily}
\renewcommand*{\recipefreeformfont}{\itshape}

% Images are stored here
\graphicspath{{./images/}}

% Draw frame around images
\setlength\fboxsep{0pt}
\setlength\fboxrule{0.5pt}

% Give credit
\newcommand{\creator}[2][von]{\textnormal{\small{(#1 #2)}}}

\begin{document}
    $recipe
\end{document}
"""

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
    def document(cls):
        return Template(cls._document_format)

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
