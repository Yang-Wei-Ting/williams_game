# William's Game

**William's Game** is a single-player, turn-based strategy board game powered solely by Python's standard libraries.

## Requirements

    Python version >= 3.6

## How To Play

    git clone https://github.com/Yang-Wei-Ting/williams_game.git
    cd williams_game/
    python src/play.py

## Overview

In this game, you control the blue soldiers while the computer controls the red soldiers.
Your objective is to guide your soldiers to survive waves of enemy onslaught.

### Soldiers

There are three common types of soldiers, each with its own strengths and weaknesses.

#### Archers

![](images/blue_archer_1.gif)
![](images/red_archer_1.gif)

Archers are soldiers with an extended attack range but lower attack and health points.
They excel against infantries but are vulnerable to cavalries.

#### Cavalries

![](images/blue_cavalry_1.gif)
![](images/red_cavalry_1.gif)

Cavalries are highly mobile soldiers.
They have an attack bonus against archers but are countered by infantries.

#### Infantries

![](images/blue_infantry_1.gif)
![](images/red_infantry_1.gif)

Infantries are soldiers with high defense.
They are strong against cavalries but are weak against archers.

There is also a special type of soldiers.

#### Kings

![](images/blue_king_1.gif)
![](images/red_king_1.gif)

Kings hold an attack advantage over all soldier types, including their fellow kings.

### Control Your Soldiers

During each turn, you can direct each of your soldiers to move once and attack once.

Upon selecting one of your soldiers, you'll notice light blue squares and a red diamond-shaped indicator appear around it.

The light blue squares indicate where the selected soldier can move. Clicking on any of these squares will prompt the soldier to move to that position.

The red diamond-shaped indicator showcases the attack range of the selected soldier.
By clicking on an enemy soldier within this range, your chosen soldier will launch an attack.

Once a soldier has moved and attacked during the turn, its color will change to gray.

To deselect a soldier, simply click on it again.

### .

Above each soldier lies its heath bar.

Every soldier can level up once certain amount of experience is obtained.
Bellow from left to right are level 1 to level 5 cavalry respectively:

![](images/blue_cavalry_1.gif)
![](images/blue_cavalry_2.gif)
![](images/blue_cavalry_3.gif)
![](images/blue_cavalry_4.gif)
![](images/blue_cavalry_5.gif)

Level 5 is the maximum level.
