# Grocery Tracker

## Stage 5: Final Demo
Our application consists of three tabs:
* At Home
* To Buy
* Find Stores  

We created 10 tables of relational database using MySQL database.
</br>
## Application Introduciton

### At Home
The main page for users to manage their purchased items.
We provide three storage spaces, fridge, freezer, and pantry for users to manage their purchased items. Each row has item name, amount, and expiration date. Users can edit all of the information. 
![image](https://media.github-dev.cs.illinois.edu/user/14624/files/74b8be2b-fbea-43df-bc80-734f04203350)

### To Buy
Users can create their own shopping list, like **Frequent Items** or **birthday party** and put items into the lists.
![image](https://media.github-dev.cs.illinois.edu/user/14624/files/2cf02a7f-3e97-4948-a08a-0fb8a3a3a86c)

### Find Stores
Users can search grocery stores information at this page.
![image](https://media.github-dev.cs.illinois.edu/user/14624/files/10eebed3-ea9d-461e-ac1f-391d057baa8e)

## Advanced Database Functions
### Stored procedure
For our stored procedure, we wanted to provide the users a good estimate of how much they would be spending per shopping list in the To Buy tab. To achieve this we used two stored procedures. The first store procedure takes the product name as the input, and it returns the minimal price of the given product sold in all available stores. The reason for this store procedure is that we believe customers always would like to know what is the cheapest price of the products they are interested in. 
 
The second store procedure takes the shopping list as the input, and it calculates a sum of all the estimated prices given the shopping list. For each product in the shopping list, the procedure will find the minimum price of that product in all available area, and then the estimated price will be multiplied by the total amount to get the total price for that product. By iterating through all products in the shopping list, the procedure will return the lower bound of the total price of that shopping list.

### Trigger 
We has a trigger which executes after inserting a new row in the has table. A new row will be inserted into the has table when the user buys an item (controlled by user interface). The trigger will automatically create an inventory list if the list that was added in the has table does not exist. Our main goal is to trace where the food is stored, so every item the users bought should be in the inventory list.

  

##### Note:  
Our application and database are both hosted on GCP.  
The Grocery Tracker [website](https://cs411-pt1-team048.uc.r.appspot.com/) is available online as long as our GCP instance is on.

