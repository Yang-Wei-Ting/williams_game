# TkTactics

**TkTactics** is a single-player, turn-based strategy board game. You command the blue army, battling against ever-growing waves of red enemy forces controlled by the computer. With each wave, the enemy grows stronger and more aggressive - can you hold the line and lead your troops to victory?

## Requirements

    OS: Linux or Windows
    Python: Version 3.10 or higher

## How to Play

    git clone https://github.com/Yang-Wei-Ting/TkTactics.git
    cd TkTactics/
    python sources/play.py

## Game Overview

### Units

Each unit has a health bar. When a unit’s health reaches zero, it is destroyed.

#### Soldier Units

There are four types of soldier units, each with its own strengths and weaknesses:

##### Infantries

![](images/blue_infantry_1.gif)
![](images/red_infantry_1.gif)

High defense  
Moderate attack range  
Strong against: Cavalries  
Weak against: Archers, Heroes

##### Archers

![](images/blue_archer_1.gif)
![](images/red_archer_1.gif)

High attack range  
Strong against: Infantries  
Weak against: Cavalries, Heroes

##### Cavalries

![](images/blue_cavalry_1.gif)
![](images/red_cavalry_1.gif)

High mobility  
Strong against: Archers  
Weak against: Infantries, Heroes

##### Heroes

![](images/blue_hero_1.gif)
![](images/red_hero_1.gif)

High attack, health, and mobility  
Strong against: All other soldier unit types

#### Controlling Your Soldier Units

##### Selecting

Press a unit to select it.  
Light blue squares: Available movements  
Red diamond-shaped marker: Attack range

##### Moving and Attacking

Move: Drag the unit onto a light blue square and release.  
Attack: Drag the unit onto an enemy within attack range and release.

After moving and attacking, a unit turns gray - indicating it can no longer perform any actions until the next turn.

##### Healing

Units automatically heal between enemy waves.

#### Inspecting Enemy Soldier Units

Press an enemy unit to view its attack range and mobility.

#### Leveling Up Soldier Units

Units gain experience by attacking enemies.  
When enough experience is earned, a unit automatically levels up and becomes stronger.

The unit’s level is shown in the upper-left corner of its icon.  
For example: cavalries from level 1 to 5:

![](images/blue_cavalry_1.gif)
![](images/blue_cavalry_2.gif)
![](images/blue_cavalry_3.gif)
![](images/blue_cavalry_4.gif)
![](images/blue_cavalry_5.gif)

#### Building Units

Currently, there is one type of building units:

##### Barracks

![](images/barrack.gif)

Used to recruit new soldier units.

#### Recruiting Soldier Units

Earn coins by surviving each enemy wave.  
Spend coins at building units to recruit new soldier units.

How to recruit:  
Click a building unit to open the production panel on the right.  
Click a soldier unit to recruit - blue means you can afford it; gray means you can’t.  
Click one of the highlighted light blue squares to deploy the unit.  
The new unit will become active on your next turn.
