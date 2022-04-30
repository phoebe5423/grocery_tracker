CREATE DEFINER=`root`@`%` PROCEDURE `minPriceArea`(IN prod_id varchar(255))
begin
    declare varPrice REAL;
    declare varStoreName VARCHAR(255);
    declare varstoreID int(11) ;
    declare loop_exit BOOLEAN DEFAULT FALSE;
    
    declare productInfo CURSOR FOR (select s.StoreID, avg(Price) as avgPrice, s.StoreName
									From Purchase pu natural join Store s join Has h on (pu.PurchaseID = h.H_PurchaseID)
									join Product pr on (h.H_productID = pr.ProductID)
									where pr.ProductID = prod_id
									group by s.StoreID
									order by avgPrice
									LIMIT 5);

    declare continue handler for NOT FOUND Set loop_exit=TRUE;
    
    DROP TABLE IF EXISTS minPriceArea;
    create TABLE minPriceArea(
		StoreID int(11) Primary key,
        StoreName varchar(255) ,
        Price REAL
        );
    
    open productInfo;
    cloop: LOOP
        fetch productInfo INTO varstoreID, varPrice, varStoreName;
        IF loop_exit THEN
            LEAVE cloop;
        END IF;
        
        INSERT INTO minPriceArea VALUES(varstoreID, varStoreName, varPrice);
    END LOOP cloop;
    close productInfo;
    
    select *
    from minPriceArea
    order by Price;
    
END