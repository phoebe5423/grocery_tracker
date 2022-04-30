CREATE DEFINER=`root`@`%` TRIGGER `insertInventory` AFTER INSERT ON `Has` FOR EACH ROW BEGIN 
SET @invID=(SELECT Distinct InventoryID FROM Purchase pu WHERE pu.PurchaseID=new.H_purchaseID); 
SET @cusID=(SELECT Distinct CustomerID FROM Purchase pu WHERE pu.PurchaseID=new.H_purchaseID); 
SET @invExi=(SELECT InventoryID FROM InventoryList WHERE InventoryID=@invID); 
SET @proName=(SELECT ProductName FROM Product WHERE ProductID=new.H_productID); 
If @invExi IS NULL THEN INSERT INTO InventoryList (`InventoryID`, `CustomerID`, `ProductID`, `ItemName`, `ExpirationDate`, `StorageSpace`, `Amount`, `Unit`) VALUES (@invID, @cusID, new.H_productID, @proName, new.ExpirationDate, new.StorageSpace, new.Amount, new.Unit); 
END IF; 
END