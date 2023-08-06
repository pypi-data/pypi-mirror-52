# hpsim
A (hopefully) high performance, modular simulator for everything from molecules to galaxy clusters.

v0.0.1:
Trying to setup the package. Internally I'm at 0.3.2 - I hope to have the package reach the same point soon.

v0.0.2 - 0.0.11:
Trying to make the package actually work as it did when it was only one file locally.
I had yet to discover local developer mode.

v0.3.2:
Got the package to function. It was a good day.

v0.3.3:
Messed up all the files and updating the version # was the way forward.
This procedure will seem embarrassing in five years.

v0.4.0
Did things, but I forgot what. It probably has something to do with the restructuring of main, but I'll write more about that in v0.5.0

v0.5.0
Changed main.py to allow for a \emph{variable!} amount of variables in the function you yourself (or I) supply the various steps. Like matplotlib.funcanimation. It feels like a grand milestone.

v0.5.1
Succeeded in making a particle generator that doesn't deal with a central power, like the sun. While that wasn't too difficult, it was difficult implementing that it had certain variables only sometimes.
TODO: make 'certain variables' customizable, so the user can input his/her own.

v0.5.2
Dissatisfied with the deep-nested callings of functions throughout the programme, I changed it so it's now a more flat structure. Should make it easier to customize.
