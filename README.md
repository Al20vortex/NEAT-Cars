# NEAT-Cars

This is a project I used to familizarize myself with AI, specifically the NEAT library for python. To run it, make sure you have NEAT and NUMPY installed,
and then run the main file. 25 cars should spawn on the racetrack, and now the AI has begun training. By around the 400th generation there should be a car
that consistently finishes a lap. From there though, I found that even after more hours of training, the cars will have difficulty getting far into the second lap.
This may be resolved by tuning some parameters in the NEAT config file, but I would like to move on from NEAT as it doesn't really give much control over the 
reproduction between generations, or the design of the neural network. A next step from here would be to dive into Deep Q Learning which is a far more recent method for training AI with neural networks.
