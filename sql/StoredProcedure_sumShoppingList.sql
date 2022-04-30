CREATE DEFINER=`root`@`%` PROCEDURE `sumShoppingList`(IN shoppinglistID int(11))
begin
    declare varPrice REAL;
    declare loop_exit BOOLEAN DEFAULT FALSE;
    
    declare productInfo CURSOR FOR (select sum(temp.minPrice*inc.Amount)
									from ShoppingList
									natural join include inc
									join (select min(Price) as minPrice, inc1.ProductID
									from ShoppingList
									join include inc1 on inc1.ShoppingID = ShoppingList.ShoppingID
									join Has h1 on h1.H_productID = inc1.ProductID
									group by inc1.ProductID) as temp on temp.ProductID = inc.ProductID
									where ShoppingList.ShoppingID = shoppinglistID);

    declare continue handler for NOT FOUND Set loop_exit=TRUE;
    
    DROP TABLE IF EXISTS NewTable;
    create TABLE NewTable(
        Price REAL Primary key
        );
    
    open productInfo;
    cloop: LOOP
        fetch productInfo INTO varPrice; -- (extract the infromation each row)
        IF loop_exit THEN
            LEAVE cloop;
        END IF;
        
        INSERT INTO NewTable VALUES(varPrice);
    END LOOP cloop;
    close productInfo;
    
    select *
    from NewTable;
    
END