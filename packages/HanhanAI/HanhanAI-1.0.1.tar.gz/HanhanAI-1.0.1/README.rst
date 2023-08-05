HanhanAI
===========================
System Overview

  Universal game AI system.
  Game developers need to provide functions like those provided by Open-AI game, so they can train their game AI.

Use Instructions

  1. use " init_UDQN(game, inputImageSize, choose_optimizers, learning_rate) " to create your network object.
  2. the object has the function "run(game, inputImageSize, total_steps, total_reward_list, num, step_num)" to train.
  3. " plot_cost() " shows the gradient change graph

Environment Instructions

  Python3.7+Graphaiz2.38

Directory Structure Instructions

  HanhanAI

      __init__.py

      universal_dqn.py

  LICENSE

  README.rsd

  setup.py


V1.0.1 version

  1. fix bugs
