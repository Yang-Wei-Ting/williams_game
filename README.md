# William's Game

**William's Game** is a single-player, turn-based strategy board game where you command blue units against the computer-controlled red units. Waves of enemy soldiers attack periodically, growing more aggressive over time.
Will you lead your soldiers to victory, or succumb to the relentless enemy onslaught?

## Requirements

    Python version >= 3.10

## How to Play

    git clone https://github.com/Yang-Wei-Ting/williams_game.git
    cd williams_game/
    python sources/play.py

## Overview

### Units

Each unit has a health bar indicating remaining hit points. When hit points reach zero, the unit is destroyed.

There are four soldier unit types, each with unique strengths and weaknesses:

#### Infantries

![](images/blue_infantry_1.gif)
![](images/red_infantry_1.gif)

Infantries are soldier units with high attack.
They are strong against cavalries but weak against archers and heroes.

#### Archers

![](images/blue_archer_1.gif)
![](images/red_archer_1.gif)

Archers are soldier units with an extended attack range.
They are effective against infantries but vulnerable to cavalries and heroes.

#### Cavalries

![](images/blue_cavalry_1.gif)
![](images/red_cavalry_1.gif)

Cavalries are highly mobile soldier units.
They have an attack bonus against archers but are countered by infantries and heroes.

#### Heroes

![](images/blue_hero_1.gif)
![](images/red_hero_1.gif)

Heroes are strong against all soldier unit types.

#### Controlling Soldier Units

Upon selecting one of your soldier units, you'll notice light blue squares and a red diamond-shaped indicator appear around it.

The light blue squares indicate where the selected soldier unit can move. Clicking on any of these squares will prompt the soldier unit to move to that position.

The red diamond-shaped indicator showcases the attack range of the selected soldier unit.
By clicking on an enemy soldier unit within this range, your chosen soldier unit will launch an attack.

Once a soldier unit has moved and attacked during the turn, its color will change to gray, and it can no longer perform any actions until the next turn.

To deselect a soldier unit, simply click on it again.

#### Leveling Up Soldier Units

Leveling up happens automatically. Every soldier unit can level up and thus become stronger once a certain amount of experience is obtained. The only means of acquiring experience is through attacking enemy units.

You can tell a soldier unit's current level by observing the upper left corner of its icon. For example, below from left to right are level 1 to level 5 (the maximum level) cavalry respectively:

![](images/blue_cavalry_1.gif)
![](images/blue_cavalry_2.gif)
![](images/blue_cavalry_3.gif)
![](images/blue_cavalry_4.gif)
![](images/blue_cavalry_5.gif)

There are two building unit types:

#### Barracks

![](images/barrack.gif)

You can spend coins to recruit infantries, archers, and cavalries from barracks.

#### Walls

![](images/wall.gif)

You can build walls to slow enemy advancement or create strategic advantages.

#### Recruiting Soldier Units

You receive some coins the next day after triumphing over an enemy wave. You can use these coins to recruit more soldier units to fight for you.

Upon choosing a production building, its production panel appears on the right-hand side of the screen. Within this panel, affordable soldier units are colored in blue, while those that you cannot afford are colored in gray.
Upon selecting an affordable soldier unit from the production panel, the corresponding building becomes encircled by light blue squares.
By clicking on any of these squares, you confirm the enlistment and place the new recruit to that position.
You can recruit new soldier units whenever you want, even during an enemy attack. However, you will have to wait until the start of the next turn for them to be ready for battle.

To cancel a recruitment, click on the corresponding icon in the production panel again. To close the production panel, click on the building again.
