.. llmgt documentation master file, created by
   sphinx-quickstart on Sat Apr 19 09:58:22 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

LLMGT Documentation
===================

LLMGT is a toolkit for modeling and evaluating language model behavior in game-theoretic settings.
It provides modules for generating structured games, running LLM-based inference, and analyzing outcomes.

This documentation is divided into the following key sections:

- **Game Construction**: Tools for sampling 2x2 games, defining payoff conditions, and labeling strategy spaces.
- **Inference**: Integration with LLMs for strategy elicitation and preference prediction.
- **Evaluation**: Modules for analyzing outputs, comparing predictions to ground truth, and inferring utilities.

.. toctree::
   :maxdepth: 2
   :caption: Game Construction

   games
   build_games

.. toctree::
   :maxdepth: 2
   :caption: Inference

   inference

.. toctree::
   :maxdepth: 2
   :caption: Evaluation

   evaluation

----

**Index pages**

* :ref:`genindex` — general index of functions/terms
* :ref:`modindex` — full module index
