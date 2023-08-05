HanhanAI
===========================
System Overview

  Universal game AI system.
  Game developers need to provide functions like those provided by Open-AI game, so they can train their game AI.

Use Instructions
  1.For games that use images as state
    1. use " init_UDQN(game, inputImageSize, choose_optimizers, learning_rate) " to create your network object.
    2. the object has the function "run(game, inputImageSize, total_steps, total_reward_list, num, step_num)" to train.
    3. " plot_cost() " shows the gradient change graph

  2.For games that take parameters as state
    1. use "  Population(population_num) " to create your  Population object.
    2. the object has the function " initPopulation(self, net_in, net_h1, net_h2, net_out)" to create your network.
    3. the object has the function " runGame(game)" to train.

Environment Instructions

  Python3.7+Graphaiz2.38

Directory Structure Instructions

  HanhanAI

      __init__.py

      ga_brain.py

      population

      universal_dqn.py

  LICENSE

  README.rsd

  setup.py


V2.0.2 version

  1. Can save network
