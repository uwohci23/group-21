---
layout: base
---
# CS4474B Final Report - Group 21

## Table of Contents
* This line is needed, but won't appear
{:toc}

## Authors
<table>
	<tr>
		<td markdown="span"><center markdown="span">**Reese Collins**<br/></center>
		<center markdown="span">*University of Western Ontario*<br/></center>
		<center markdown="span">*Department of Computer Science*<br/></center>
		<center markdown="span">rcolli47@uwo.ca</center>
		</td>
		<td markdown="span"><center markdown="span">**Daniel McGarr**<br/></center>
		<center markdown="span">*University of Western Ontario*<br/></center>
		<center markdown="span">*Department of Computer Science*<br/></center>
		<center markdown="span">dmcgarr@uwo.ca</center>
		</td>
		<td><center markdown="span">**Navjeeven Mann**<br/></center>
		<center markdown="span">*University of Western Ontario*<br/></center>
		<center markdown="span">*Department of Computer Science*<br/></center>
		<center markdown="span">nmann29@uwo.ca</center>
		</td>
		<td markdown="span"><center markdown="span">**Sundin Nguyen**<br/></center>
		<center markdown="span">*University of Western Ontario*<br/></center>
		<center markdown="span">*Department of Computer Science*<br/></center>
		<center markdown="span">snguy22@uwo.ca</center>
		</td>
		<td><center markdown="span">**Andrew Domfe**<br/></center>
		<center markdown="span">*University of Western Ontario*<br/></center>
		<center markdown="span">*Department of Computer Science*<br/></center>
		<center markdown="span">adomfe@uwo.ca</center>
		</td>
	</tr>
	<tr>
		<td colspan="5"><center markdown="span">Original Repository by Simo Tukiainen (simo.tukiainen@fmi.fi)</center></td>
	</tr>
</table>

## Executive Summary
Our redesigned blackjack game system is designed to provide an immersive and enjoyable user experience, with a focus on simplicity and ease of use. We have approached the design of the game with a user-centered approach, prioritizing the needs and preferences of our target audience. 

To achieve this goal, we have incorporated several principles of human-computer interaction into the game design. For example, we have applied the 80/20 rule, which states that 80% of a user's needs can be met with 20% of the available options. To achieve this, we have streamlined the user interface by removing unnecessary elements and only displaying essential information, which makes it easier for players to focus on the gameplay itself. This approach reduces cognitive load and ensures that the game is accessible to both novice and experienced players. 

We have also incorporated confirmation for actions, which helps to reduce the likelihood of errors or mistakes. For instance, when a player clicks the "Back" button, a confirmation dialog box appears, allowing the player to confirm their action before proceeding. We also have a form of implicit confirmation of action where a user must click the “Rebet” button or place a new bet amount before a new hand can be dealt. Before, clicking to deal a new hand would automatically re-place your last bet without any confirmation. In a game where there are financial implications, ensuring that were reduce the likelihood of error or mistakes to around 0 is essential in creating a game that is fair to the user. This adds an extra layer of security and helps to build user confidence. 

Another way we have incorporated human-computer interaction principles is by providing a clear and concise view of the game table. We have made the blackjack table the central focus of the game, and all other information, including betting options, are laid over top of the virtual blackjack table transparently. This simplifies the user interface and ensures that the game table remains the central focus of the user's attention. 

To further enhance the user experience, we have re-designed the game with high cognitive offloading. For instance, we have automated the process of determining whether the dealer must draw another card or stay with their current hand based on the established rules of blackjack. Also, any possible actions a user can take will be presented solely based on the state of their hand. For example, we will not present the option to split unless the user has a pocket pair. This reduces the cognitive load for the user, allowing them to focus on making their own decisions while the system handles the complex calculations and decision-making processes behind the scenes and only presents the information needed. 

Overall, our redesigned blackjack game system is designed with the user in mind, focusing on simplicity, ease of use, and an engaging user experience. By incorporating human-computer interaction principles such as the 80/20 rule, confirmation for actions, and high cognitive offloading, we have created a game that is both accessible and immersive, ensuring a positive user experience for all players.

## Navigational Map

## Design Principles
### 80/20 Rule
### Confirmation of Actions
### Externalization of Information
### Visibility
### Affordance
### Familiarity
### Constraints
### Chunks
### Fitts' Law
### Consistency
### Gulf of Evaluation
### Gulf of Execution
### Metaphors
### Semiotics
### Progressive Disclosure
### Causality

## Heuristic Evaluation
### Visibility of System Status
### Match Between the System and the Real World
### User Control and Freedom
### Consistency and Standards
### Error Prevention
### Recognition vs. Recall in User Interfaces
### Flexibility and Efficiency of Use
### Aesthetic and Minimalist Design
### Help Users Recognize, Diagnose, and Recover from Errors
### Help and Documentation

## Final Thoughts
Overall, our project has successfully incorporated the 10 heuristics of evaluation. There were many design principles that were used that allowed for a HCI focused redesign. The project, like many artifacts that have been developed, can always be further improved. For the redesign of a python-based blackjack system we have made improvements to allow for a more user-friendly environment. Some of these improvements, however, could be taken further; these may include our help and documentation, visibility of system status, and error recovery. Starting with the visibility of our system, an improvement that could be made is to incorporate more feedback to the user about the dealer’s actions once they have selected their action. This will allow the user to better understand the current state of the dealer with regards to their action. For example, if the user decides to stay, the system should indicate that the dealer will either stay if their card is higher than 16 or keep ‘hitting’ until greater than 16. This will show the user what is being done in response to their action. As for help and documentation, as mentioned in the section above there should be greater access to helpful information whether in coach mode or not. The increase of documentation should be accessible from the menu page as well before the game begins to allow for the user to have access before they begin if they have not played the game prior. The addition of the strategy chart will also help close the gulf of evaluation. Lastly, for future improvements to the error recovery, these should only be done within coach mode. Blackjack is a game of chance and skill, understanding that there are stakes to one's actions is an important part of the game since it a game of wagering one's money. The use of error recovery is not something that should be fully incorporated into the main game but should be considered for training purposes while the user is in coach mode.  

To conclude, our artifact is one that has shown great improvement but like any system or product it will need further refinement. The work that has been done has been thought of through the lense of design principles and HCI concepts which has been done by consciously designing our project in a human-centered manner. Our evaluation was done to assess the effectiveness of the project through common heuristic principles which gave light to design choices that were done well and others that could be improved further. Considering all the HCI concepts and terminology used throughout the various development stages, our project was created in a way to think deeply about users' needs and create a product that bridges the gap between system centered design and human centered design. 