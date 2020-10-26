# Homework 4

The basic idea behind our agents is that they face a certain direction and will only go forward and right (relative to the direction they face). This means that the agents stick to walls and spiral inward to explore a world.

Toyota Corolla Agent (SRV2): Keeps track of past two actions. If the agent has bumped in the last action then it will try to move in each direction until there is no bump. If it was not bumped in the last action, it will move right, randomness is added to make sure the agent will not get stuck repeating the same actions.
Toyota Corolla Agent Plus (SRV2+): SRV2 with hose action

Simple Agent: Moves left if bumped, forward otherwise, with additional randomness to try to extricate it from loops and holes.

Model Agent: Basic moveset is the same, maps the world as it moves through it and checks if the agent has gotten stuck in a loop. This makes the agent completely deterministic as randomness is not needed to break out of loops.

Defective Agent: This agent has a 25% chance of leaking dirt into its current square with every move. To easily maximize its score, this agent never moves.

Non-deterministic

  **Reflex Simulation Data**   

On Spell's world, our SRV2 (non-hosing version) achieved **98% accuracy** or an average of 3.928 over 125 trials.   
20 Trial Performance History (**perfect**): [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]   
  Frequency:   
  4s - 115    
  3s - 10    

On Spell's world, our SRV2+ achieved **100% accuracy**.
Performance History:

On Depue's world, our SRV2 achieved **100% accuracy** or an average of 8.0 over 125 trials.   
20 Trial Performance History (**perfect**): [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]   

On Yamada's world, our SRV2 achieved **99.5% accuracy** or an average of 15.92 over 125 trials.   
20 Trial Performance History (**perfect**): [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]      
  Frequency:   
  16s - 115    
  15s - 10    

On Meister's world, our SRV2 achieved **100% accuracy**. or an average of 5.0 over 125 trials.   
20 Trial Performance History (**perfect**): [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]   

On Sarkissians' world, our SRV2 achieved **100% accuracy** or an average of 8.0 over 125 trials.   
20 Trial Performance History (**perfect**): [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]   

On Liu's world, our SRV2 achieved **100% accuracy**  or an average of 5 over 125 trials.
20 Trial Performance History (**perfect**): [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]   

On Suddath's world, our SRV2 achieved **100% accuracy** or an average of 4.0 over 125 trials.   
20 Trial Performance History (**perfect**): [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]   

On Catalan's world, our SRV2 achieved **100% accuracy** or an average of 10.0 over 125 trials.   
20 Trial Performance History (**perfect**): [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]   


  **Model Simulation Data**

Code Readability 

- [ ] Doc Strings
- [ ] Wiki and Explaining Text
- [ ] Double Check Done
- [ ] 1.4 Console Outputs

Enviornment

- [x] Implemented
- [x] Doc Strings

Custom Worlds

- [x] Will D.
- [x] Will Y.
- [x] Florian

Abstract and Sub-Classes

- [x] Implemented
- [x] Doc Strings

SRV2

- [x] Rules
- [x] Percepts
- [x] Wiki Explanation

Model_Agent

- [x] Rules
- [x] Mapping
- [x] Loop Checking
- [x] Explanation
- [ ] Simulation Data

SRV2+

- [ ] Hose Function
- [ ] Hose Detection

Defective

- [x] Doc Strings
- [x] Wiki Explanation
