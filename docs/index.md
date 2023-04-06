---
layout: page
---
# CS4474B Final Report - Group 21

## Table of Contents
* This line is needed, but won't appear
{:toc}

## Authors
<table>
	<tr>
		<td><center markdown="span">**Reese Collins**<br/></center>
		<center markdown="span">*University of Western Ontario*<br/></center>
		<center markdown="span">*Department of Computer Science*<br/></center>
		<center markdown="span">rcolli47@uwo.ca</center>
		</td>
		<td><center markdown="span">**Daniel McGarr**<br/></center>
		<center markdown="span">*University of Western Ontario*<br/></center>
		<center markdown="span">*Department of Computer Science*<br/></center>
		<center markdown="span">dmcgarr@uwo.ca</center>
		</td>
		<td><center markdown="span">**Navjeeven Mann**<br/></center>
		<center markdown="span">*University of Western Ontario*<br/></center>
		<center markdown="span">*Department of Computer Science*<br/></center>
		<center markdown="span">nmann29@uwo.ca</center>
		</td>
		<td><center markdown="span">**Sundin Nguyen**<br/></center>
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
		<td colspan="5"><center markdown="span">[Original Repository](https://github.com/tukiains/blackjack-gui/) by Simo Tukiainen (simo.tukiainen@fmi.fi)</center></td>
	</tr>
	<tr>
		<td colspan="5"><center markdown="span">[Our Repository](https://github.com/uwohci23/group-21/)</center></td>
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
![](/docs/assets/images/Map.png)

## Design Principles
### 80/20 Rule
During a blackjack hand, there are certain actions you can and cannot do. Depending on your cards, you may be able to hit, stand, double, etc. However, there are also cases where you’re only able to hit and stand. By employing the 80/20 rule we only show the options that are available to the user and hide the options that are not. In our system, 80% of the actions for your hand are caused by 20% of the shown actions which ultimately depend on the user's hand.

### Confirmation of Actions
Exiting during a live hand will prompt the user to confirm if they would like to exit the table.  Confirmation will also be made for dealing the next hand, it will confirm to the user whether they would like to bet the same amount of money or make a different wager. The decision was changed from having a confirmation to whether the user wants to hit or stay as this would degrade the speed and quality of gameplay.

### Externalization of Information
The usable buttons are displayed prominently in contrast to the unusable buttons which are invisible. This externalization allows the user to easily find the actions they will access often during gameplay. Also, the “Get Help” button internalizes the Blackjack term information that the user may not necessarily want always visible. This internalization reduces the cognitive load, which can benefit an intermediate user who already understands the Blackjack terms.

### Visibility
By only displaying the game features of the system that were currently a viable action allowed for the user to only be shown the options that can be currently selected. It mitigates the information overload of the past design and does not overwhelm the user with a taskbar full of options to look at.

### Affordance
The redesign of the betting system has a twofold design; by changing the amount to bet from a slider to chips on the table it affords the user to select the monetary combination of chips they would like to bet which is also used as a metaphor for real betting. Another aspect of correctly perceived affordance incorporated into our design is the chip stack being shown above the user's chip stack. This affords the user to understand the relationship between the chips they have bet to the total amount they have left. It also removes the sliders correctly rejected affordance of sliding the bet amount to a max amount of user's stack. An additional use of affordance is the directional back arrows incorporated into the menu system. These use correctly perceived affordances so the user knows that if the button is pressed it will take them to the previous state of the games control state.

### Familiarity
Using playing chips to represent the players stack suggests its function to bet these chips similar to a casino. Similar color scheme to traditional Blackjack tables seen at casinos. Rules of the game and payout rates are shown on the table as seen with live blackjack.

### Constraints
Once the results of a match are shown (blackjack, push, bust, etc.), the only main action a user can do is place another bet. In the betting phase, the user can either increase their bet or click “deal” to start a new match. In both of these cases, the user cannot perform any of the actions that were only available during an active match (as shown with the buttons’ differing font colours). These are examples of a logical constraint as they limit the range of actions the user can perform. These help the user make decisions that flow with the established rules of Blackjack.

### Chunks
In our game, we employed Hick’s Law by adjusting the number of options available to the user dynamically based upon the user’s hand and the dealer’s up card. We removed actions from the UI that would be invalid for the user to take, therefore reducing the number of choices presented to the user and enabling their choice making process more streamlined to what they are able to do.

### Fitts' Law
Our design places our chips next to our deal function, once chips have been selected for a wager size, the deal button will be a small distance away from the actions. The actions are then stacked above the deal button so that the new gameplay options are easily accessible from the current mouse position from the deal button. The buttons for gameplay are along the game's boarders, which follows the other principle of Fitts' law of infinite edges. 

### Consistency
#### Aesthetic
The fonts and menu bars are consistent throughout the game.

#### Functional
The game does not use any dragging features throughout the project. Only allows for mouse clicks. Makes operations of the user consistent throughout the application.

#### External
The game colors that are used are similar to the felt tables of casinos, the vibrant green is used throughout the gameplay. The black trim represents the leather edges of casino table arm rests.

### Feedback
In our blackjack game, we modified the coach mode to provide users with feedback on how to optimally play. By leveraging the feedback design principle, we emphasize the importance of providing clear feedback to the user when they enable coach mode.  If a user selects an incorrect mode, coach mode will present a message telling them what the correct mode would in face be.

### Gulf of Evaluation
To reduce the gulf of evaluation and allow the user to understand the game of blackjack easily we use familiar language in our game, such as “hit” and “stand” versus more confusing terms such as “draw” and “hold”. We also provide feedback to the user once their hand is finished telling them whether they won or lost along with providing feedback to the user when they are in coach mode.

### Gulf of Execution
To decrease the gulf of execution we employ methods such as making UI elements as visible as possible and providing visual cues as to when a user can do certain actions in the game. Depending on a user's hand the game will hide certain buttons which would be invalid actions therefore we only present the valid actions that a user can take. We also match the look of the game to what you would find at an actual casino, and by doing so we employ familiarity to help reduce the gulf of execution. Rules, actions, chips are all UI elements that we’ve matched to the look of an actual casino.

### Representation
Prior to our redesign the way a user would place a bet is using a slider that went from 1 to 10, this is a bad representation as it does not coincide with the task of betting. Instead, we redesigned the betting system to use casino chips. We added chips ranging from $5, $10, $25, and $50 and you could click on a chip multiple times to up your bet to any value if you had enough money to cover your bet.

### Metaphors
We modelled casino chips ($5, $10, $25, $50) in our blackjack game as a key UI element for placing bets. This design choice leverages the metaphor of using chips to place bets in a casino setting, making the game more intuitive and engaging for users. Each chip denomination is represented using realistic graphics that closely resemble actual casino chips, creating a direct and immersive connection between the game and the user's mental model of how betting works in a casino.

### Semiotics
The sound of the card deck being shuffled when the “deal” button is pressed is an indexical, auditory sign that is directly related to the deck of cards. Although the cards are not visually shown to be shuffled, this indexical sign gives the impression of the deck shuffling being performed.

### Progressive Disclosure
This design principle is used when the user wants to look up what each button does while they are using Coach Mode. When the user enters Coach Mode, they are not automatically presented with the list of terms. Rather, they need to make a request for its appearance by clicking the “Get Help” button.

### Causality
Prior to the start of a match, the user can place a bet. Each time one of the tiles (5, 10, 25, 50) is clicked on, the value of the total bet increases by the selected tile’s face value. Through this, the user’s selection immediately causes the total bet amount to change. We also employed causality as a design principle in our blackjack game by providing clear and immediate feedback to the user on the outcomes of their decisions. We display whether the user won the hand, and we show the total value of the user's and the dealer's cards when the user decides to hit or stand. This helps the user understand the impact of their decisions on the game's outcome and guides their decision-making process in future hands.

### Positive Transfer
In our blackjack game, we used positive transfer by designing the game to closely resemble an actual casino blackjack table. By modeling the look of the table, chips, and rules in our game to match the appearance of a real blackjack table as closely as possible, we aimed to help users transfer their existing knowledge and skills of playing blackjack in a casino setting to our game. Users who have played blackjack in a casino before will be familiar with the visual elements and rules of the game, making it easier for them to understand and engage with our game.

### Mapping
In the original game, the betting was controlled by a horizontal slider placed on the top right corner of the UI, but the confirmed bet amount appeared on the bottom-center of the UI. In our redesign, the betting was controlled by clicking four types of chips ($5, $10, $25, $50) that were placed slightly below the confirmed bet amount. This improved mapping layout creates a more natural feel as it creates a better impression of the user being in possession of the tiles they can choose to add to their bet amount.

## Heuristic Evaluation
### Visibility of System Status
In regard to the visibility of the system status, the player is now able to see the cards they have along with the dealer’s cards and the total sum of their respective hands. The game also displays messages to the user indicating their system status such as winning or losing and the reason for the loss. However, the system could benefit from providing more feedback to the player such as when the dealer hits or stands.

Another aspect of the visibility of the system status is that the game has been updated to remove the buttons that are not able to be pressed with the current state of the dealers and user's cards. This provides the user with a good visibility of the actions that can be taken with respect to the state of the game.

### Match Between the System and the Real World
The system follows the rules and conventions of a traditional blackjack game in the real world. The game also uses appropriate terminology and symbols to represent cards and other actions. Furthermore, the table colours have been matched to a similar colour to the felt used in casinos. The chips used for betting result in a close simulation of live action betting to choose the chips you wish to wager. Lastly, the common rules of the game are displayed on the table as seen in most casinos. As a result, from these design choices this heuristic is well met.

### User Control and Freedom
The system allows the user to act freely with control over their actions in the game. The player can, for example, hit or stand and choose to place a bet or not. However, the system could use a little more work by providing the player with more options, such as customization to fit their user experience. This could range from changing the theme of the cards to adjusting the game speed to their preferences.

This game does lack on user freedom as it is meant to match the stakes of gambling in a casino. The game should not be designed to incorporate an undo function or redo of any kind as that is not permitted in live casinos. This heuristic may be lacking but it does this intentionally as the limitations of the game environment affords this.

### Consistency and Standards
The system is consistent throughout the game. The player interacts with the game by using a user interface which is populated with various buttons and sliders. The game provides feedback and visual cues. However, the system could benefit by following the design standard of more modern blackjack games as a lot of the terminology is not well known by most people such as “insurance”.

The terminology used throughout the game matches what is commonly used in casinos. It allows the user to have positive transfer of knowledge from real casinos and vice versa coming from the game to a real casino. This heuristic has been met as it follows a good internal consistency to game functionality and external consistency to a live blackjack table in a casino.

### Error Prevention
The system is consistent throughout the game. The player interacts with the game by using a user interface which is populated with various buttons and sliders. The game provides feedback and visual cues. However, the system could benefit by following the design standard of more modern blackjack games as a lot of the terminology is not well known by most people such as “insurance”.

The terminology used throughout the game matches what is commonly used in casinos. It allows the user to have positive transfer of knowledge from real casinos and vice versa coming from the game to a real casino. This heuristic has been met as it follows a good internal consistency to game functionality and external consistency to a live blackjack table in a casino.

### Recognition vs. Recall in User Interfaces
A key priority in our system was to ensure that the user would not have to recall what terminology and symbols mean in our game. By employing recognizable and highly visible UI elements we can reduce the cognitive effort required to play the game. All of the actions that a user can take are visible to them when they are in a hand, and any actions that are unable to be selected are then disabled. Rather than trying to remember what they can or cannot do with a certain hand, we take care of that and instead present them with the options they can carry out.

### Flexibility and Efficiency of Use
To provide our users with a flexible experience we offered inexperienced blackjack players a tutorial option beside the normal play option. In this case, users would be put into the game with coach mode enabled and would be provided feedback based on their actions in the game. For more experienced players we offer them the normal play option, and in the game UI they have the option to enable coach mode.

### Aesthetic and Minimalist Design
The system provides a clean and minimalist design, with a focus on simplicity and ease of use. With only critical information being presented to the user we can reduce the noise in the UI and allow the user to focus on the game.

### Help Users Recognize, Diagnose, and Recover from Errors
Feedback is provided back to the player or user when they make a mistake in the coach mode. For example, if a user tries to hit when they have two face cards against a dealer 5, the system will give the user a message that the correct move is to stay versus trying to hit. By providing actionable feedback we allow the user the ability to take the correct action.

### Help and Documentation
The basic rules of the game are displayed on the table once the game is started. This allows for new users to read the rules of the gameplay. The text is as follows:

> BLACKJACK PAYS 3 TO 2  
  Dealer must stand on a 17 and draw to 16  
  Insurance pays 2 to 1  

The text indicates to the user how the payouts are made and the rules the dealer must follow. For our improvements to coach mode, it gives the user a training environment to practice playing blackjack with more feedback features rather than in the original design informing the user to “try again” when selecting an option. The redesign of coach mode tells the user the correct action to take with respect to their current hand.

With blackjack having a unique combination of skill and luck to beat the dealer, our redesign on the game provides the user enough help and documentation to succeed. Our help documentation can be found only when coach mode has been selected, this could be taken further; the user is only informed with the meaning behind each action of the game from the help documentation. This documentation could be further refined by implementing the strategy chart below.

By incorporating this chart into the help documentation it will allow users to gain familiarity with which state of hands results in what action. Our evaluation of our help documentation is good, along with the use of coach mode it helps the users to learn when to make what decision in the game. The improvement would allow the users to learn and remember how to play the game.

## Final Thoughts
Overall, our project has successfully incorporated the 10 heuristics of evaluation. There were many design principles that were used that allowed for a HCI focused redesign. The project, like many artifacts that have been developed, can always be further improved. For the redesign of a python-based blackjack system we have made improvements to allow for a more user-friendly environment. Some of these improvements, however, could be taken further; these may include our help and documentation, visibility of system status, and error recovery. Starting with the visibility of our system, an improvement that could be made is to incorporate more feedback to the user about the dealer’s actions once they have selected their action. This will allow the user to better understand the current state of the dealer with regards to their action. For example, if the user decides to stay, the system should indicate that the dealer will either stay if their card is higher than 16 or keep ‘hitting’ until greater than 16. This will show the user what is being done in response to their action. As for help and documentation, as mentioned in the section above there should be greater access to helpful information whether in coach mode or not. The increase of documentation should be accessible from the menu page as well before the game begins to allow for the user to have access before they begin if they have not played the game prior. The addition of the strategy chart will also help close the gulf of evaluation. Lastly, for future improvements to the error recovery, these should only be done within coach mode. Blackjack is a game of chance and skill, understanding that there are stakes to one's actions is an important part of the game since it a game of wagering one's money. The use of error recovery is not something that should be fully incorporated into the main game but should be considered for training purposes while the user is in coach mode.  

To conclude, our artifact is one that has shown great improvement but like any system or product it will need further refinement. The work that has been done has been thought of through the lense of design principles and HCI concepts which has been done by consciously designing our project in a human-centered manner. Our evaluation was done to assess the effectiveness of the project through common heuristic principles which gave light to design choices that were done well and others that could be improved further. Considering all the HCI concepts and terminology used throughout the various development stages, our project was created in a way to think deeply about users' needs and create a product that bridges the gap between system centered design and human centered design. 