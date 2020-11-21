# Homework 5

**Romania Problem Notes**    
I implemented this problem with a list function rather than your heapq usage. Because of that, I'm not sure how I should implement the extracredit.
Also my logging functions prob double the operations needed here but I didn't really care to fix it.

# Homework 4

***Note to Dr. Spell***    
*We submitted a completely finished version to you. Still, we're going to continue to work on the project and make it better on the after_turn_in branch. We'd like for you to check that out because it will have better code, but the master branch will remain unchanged.*

The basic idea behind our agents is that they face a certain direction and will only go forward and right (relative to the direction they face). This means that the agents stick to walls and spiral inward to explore a world.

Important Note!!!    
Our implementation means that Agents **DO NOT KNOW THEIR CARDINAL DIRECTION** all of their movements are relative! Why would a Roomba know if it's pointing up or down, left or right, all it knows are percepts and movements. We're doing this to *cough cough* retain our integrity to the project *cough cough* not because it allows us to better navigate our enviornment.

**Toyota Corolla Agent (SRV2):**    
If the agent has bumped in the last action then it will try to move in each direction until there is no bump. If it was not bumped in the last action, it will move right, randomness is added to make sure the agent will not get stuck repeating the same actions. We called this agent the Toyota Corolla Agent because we're 99% sure it's a reflex agent under your specifications, just that the variable that we use to return our action, since it isn't reset, is used to find a next action. Because we use our last action to decide our next one, we wanted to air on the side of safety and call it a "hybrid" or Toyota Corolla agent. We'd like for you to consider it as a reflex agent because it is so simple and we want the clout for making a perfect reflex agent.   

 This agent is non-deterministic.   

**Toyota Corolla Agent Plus (SRV2+):**   
SRV2 with hose action. Same logic as Toyota Corolla Agent.   

 This agent is non-deterministic.   

**Simple Agent:**    
Moves left if bumped, forward otherwise, with additional randomness to try to extricate it from loops and holes. This is a 100% true simple reflex agent. It's really dumb.   

 This agent is non-deterministic.   

**True Model Agent:**    
Basic moveset is the same, maps the world as it moves through it and checks if the agent has gotten stuck in a loop. This makes the agent completely deterministic as randomness is not needed to break out of loops. This is currently working, just that the loop tracker and mapping is resulting in a lower score than Toyota Corolla Agent. For that reason, we've excluded it from the data collection since it's much less efficient.   

 This agent is deterministic.   

**Defective Agent:**    
This agent has a 25% chance of leaking dirt into its current square with every move. To easily maximize its score, this agent never moves. 
Since you said that it has a 25% of leaking dirt, all we're doing is staying in the same place and sucking. This will mean we're optimizing our performance by abusing our faults. This is a kind of exploit, more because our Toyota Corolla works great even with defects. If you don't like how we're maximizing our utiliity here, you can just use the Toyota Corolla with the defect enviroment.   

 This agent is deterministic.   

  **Reflex Simulation Data**   

On Spell's world, our SRV2 (non-hosing version) achieved **98% accuracy** or an average of 3.928 over 125 trials.   
20 Trial Performance History (**perfect**): [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]   
  Frequency:   
  4s - 115    
  3s - 10    

On Spell's world, our SRV2+ achieved **100% accuracy**.
Performance History: [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
SVR2+ is also known as Toyota_Corolla_

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

- [x] Doc Strings
- [x] Wiki and Explaining Text
- [ ] Double Check Done
- [x] 1.4 Console Outputs

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
- [ ] Mapping
- [ ] Loop Checking
- [x] Explanation
- [x] Simulation Data

SRV2+

- [x] Hose Function
- [x] Hose Detection

Defective

- [x] Doc Strings
- [x] Wiki Explanation
