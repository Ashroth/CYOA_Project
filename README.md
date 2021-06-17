# CYOA_Project
Final project for CS50W

## Description
This project is an online choose your own adventure creator and player. Users can, after registering, create their own adventures, composed of self-created events, items and choices.

## Distinctivness and Complexity
My project can be divided into two parts: create and view.
Create is the portion responsible for the creation, editing and deleteing of adventures and parts of adventures.
The structure of the models in this project is thus:
- Each adventure has events and items.
- Each event has choices and may have items that may be hidden.
- Each choice links up to two events from the adventure together and may have conditions (this many of this item) that may be hidden
- Each item is either a status, an item or a hidden trigger and has to be named in the adventure context before they may be added to events.
Thus my models create a structure distinct from the prior projects on this course. Further, my models allow the user to seperate them into visible changes that the user may see and hidden changes that do not show to the user.
Therefore my project is also more complex than the prior projects.
View is responsible for the playing of created adventures. This portion uses javascript to load and display the events and choices of the adventure.
Further, it is also responsible for enforcing the game-logic defined during creation; the addition and removal of items during events, whether or not the player can select a choice and also what happens if the player runs into a dead end or loses all their health. The game logic required by my project is definitely an added degree of complexity in comparison to the prior projects of this course.

## Content of files (Relevant files are all within the CYO app):
*urls.py* just contains the paths for the project.
*views.py*: Contain the view functions and modelforms:
- index_view shows the index and all created adventures
- adventure_create_view shows the create view for adventures and creates the start and end events and the "Health" status for an adventure when created
- adventure_edit_view shows the screen that contains all the details of the adventure, provided the user is the one who created the adventure.
- item_add_view allows the user to add items to the specific adventure.
- event_create_view is used when creating events for the adventure.
- event_edit_view show all the components of the specified event.
- event_item_view allows the user to add items (that have previously been added to the adventure) to the event. The amount dictates whether these are additions or removals, with 0 removing all of the item from the player
- choice_create_view creates a choice from the event where this view is called from to any other event in the adventure
- choice_item_view creates conditions for the choice this view is called for, requiring the player to have the defined amount of the specific item, with negative values removing that many of the item from the player.
- adventure_view renders the first screen of the chosen adventure
- adventure_event_view is used during the play to load the chosen event, any items attached to it, any choices that start from the event and any conditions attached to each of the choices.
- login, logout and register_view handle the creation and login of user accounts
- delete_view handles the initial deletion call of object of <type>/<index> by displaying a warning and asking to proceed
- generic_edit handles the editing of object of <type>/<index> and also takes care of the deletion process when called from the delete_view. This function is a bit more complicated since I noticed that I could save a lot of lines by collating my model editing functions into one. Basically the function checks if the object is to be deleted, then checks that the object exists and that the user is its creator. If the request is GET, the function then creates a new form for that instance of that model which the user may edit. If the request is POST the function either saves the edits into the model or deletes the model. Finally the function redirects the user to the view that makes most sense.
	
*models.py*: The models used.
- User is just the regular user model.
- Choice connects the initial and final events together and has the text to be displayed.
- Event is just the title and text of the event and a reference to the adventure it is in.
- Adventure contains the reference to the user, the title and description.
- ItemStyle has the name and type of an item that is used within the adventure.
- Item defines the addition and removal of items defined by the ItemStyle models within the adventure. Each instance of this model is associated with either an event or a choice. Could have done both for some handy linking functionality, but the deletion would have become complicated.
Referring to the user only in adventure, and the adventure only in events and itemstyles is perhaps slightly inefficient. A more advanced version of this project would benefit from adding a reference to the adventure in the rest of the models also.

*adventure.js*: The javascript used when playing the adventures. Contains 6 functions and two definitions. The definitions are for the players state, which is initialized at health = 1 to not trigger the ending condition if the creator has removed the health model from their adventure. The other definition is just there to help store the conditions for each choice.
- inventory(type) prints the content of the players "Status" or "Item" into the corresponding html container.
- show(type) hides the main container and shows the container corresponding to the type and then calls the above. If the main block is set to not display, it is instead revealed and the other container hidden. Also disables the other button while the main screen is off.
- item_handler(inventory_name, item) handles the times when an event adds or removes an item. The item variable contains both the name and amount. The function returns an appropriate message.
- conditional_adventure(index, event_id) is called when a player clicks on a choice that has conditions attached, such as having more than 3 health. The player can not click on a choice that has conditions they do not fulfill, so this function only needs to handle the removal of items.
- condition_checker(condition) compares the players inventory against the conditions of a choice before they choice button is made. If the player fulfills the condition, the button creation proceeds. If not, the button gets an appropriate message instead.
- adventure(event_id) handles the fetching and drawing of the next event, and all the items and choices therein. First the fetched title and text are drawn, then the events items are iterated over and written out, provided the item is not set to hidden. Then the function confirms that the player is alive and that the event is not a dead end. If either of these proves false the choices in the event are replaced by an appropriate piece of text and a link to start the adventure over. Otherwise, the function then iterates over the choices, checking each for conditions and adding them to the event block.
	
The *templates* are not complicated:
- index.html just lists all existing adventures
- create.html is a generalized form template that handles all creating and editing
- adventureedit.html links to the adventure_edit_view and shows the basic details of the adventure and the various options for editing and adding to it.
- edit.html is similar to the above, but for events. It shows the choices that start from the event and any items linked to the event and conditions linked to choices.
- delete.html just renders a warning and a button that deletes whatever model indicated to the view.
- layout.html and layout_adventure.html are the layout templates. The former handles most of the site and the latter handles the "play" portion.
- login.html and register.html are the login and register views.
- adventure_view.html handles the "play" portion of the project
	
*style.css* contains the CSS for the whole project.

## How to Use:
1. Create an account
2. Press create in the navigation bar
3. Write your title and summary
4. Now you can add events and items to the adventure
5. Clicking on the name of an event or an item opens allows you to edit them
6. First event is the start event and the second is the end event. The end event should be treated as the victory condition; reducing the players health to 0 or leaving them no choices are the failure conditions.
7. Clicking on an events title opens up the events edit screen, where you can edit the particulars of that event, connecting it to other events or adding items.
8. In the event edit screen, clicking on the text of a choice allows you to edit it.
9. After you are done, just return to the index and your adventure will be visible.
10. Clicking on its title opens the adventure view with the description and title of the adventure visible, along with the start button.
11. Clicking on the start button brings you to the first screen of the adventure.
12. The inventory and status buttons will show you the players status and items. To return to the adventure from these views, just click the "back" button that has replaced the button you clicked.
	
## Additional information:
	As a final project, I found the scope of my work to be excellent; I could apply what I had learned and also practice the nitty-gritty details that had been previously been provided. My desired features also provided me with a chance to work on applying what I had learned further and also gave me several directions to further my study on the various features of django. This project is also stored in another repository on the same github account that I send this from.