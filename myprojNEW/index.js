var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var bodyParser = require('body-parser');
var flash = require('express-flash');
var session = require('express-session');
var mysql = require('mysql2');


var connection = mysql.createConnection({
    host: '34.134.166.47',
    user: 'root',
    password: 'test123',
    database: 'GroceryTracker'
});

connection.connect;

var app = express();

// set up ejs view engine 
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
//app.use(express.static(__dirname + '../public'));
app.use("/public", express.static(__dirname + "/views/public"));

app.use(session({
    secret: '123456catr',
    resave: false,
    saveUninitialized: true,
    cookie: { maxAge: 60000 }
}))

app.use(flash());

/* GET create item page, respond by rendering index.ejs */
app.get('/add', function (req, res, next) {
    res.render('index', { title: 'Add' });
});

// this code is executed when a user clicks the create item submit button
app.post('/create-item', function (req, res, next) {
    var productid = req.body.productid;
    var plucode = req.body.plucode;
    var name = req.body.name;
    var lifespan = req.body.lifespan;
    var calories = req.body.calories;
    console.log(productid);
    /*
    function getRandomInt(max) {
        return Math.floor(Math.random() * max);
    }
    let x = getRandomInt(100)
    */    
    var sql = `INSERT INTO Product (ProductID, PLUcode, ProductName, Lifespan, Calories) VALUES ('${productid}','${plucode}','${name}','${lifespan}', '${calories}')`;

    console.log(sql);
    connection.query(sql, function (err, result) {
        if (err) throw err;
        console.log('record inserted');
        req.flash('success', 'Data added successfully!');
        res.redirect('/db');
    });
});


//search
app.post('/search', function (req, res, next) {
    var name = req.body.keyword;
    console.log(name);
    
    var sql = `select * from Product where ProductName like "%${name}%"`;

    console.log(sql);
    connection.query(sql, function (error, result) {
        if (error) {
            res.send('Error in database operation');
        } else {
            console.log('The solution is: ', result);
            //res.send(result);
            res.render('productList', { data: result });
        }
    });
});

// advanced query #1
app.get('/aqONE', function (req, res) {
    var sql = `SELECT avg(Price) as temp, pr.ProductName as temp2 FROM Purchase pu NATURAL JOIN Store s JOIN Has h ON (pu.PurchaseID = h.H_purchaseID) JOIN Product pr ON (h.H_productID=pr.ProductID) GROUP BY h.H_productID ORDER BY count(H_productID);`;
    connection.query(sql, function (err, result) {
        if (err) {
            res.end('Failed:' + err);
        } else {
            console.log(result);
            res.render("advancedqueryONE", { data: result });
        }
    });
});
app.post('/aqOneSearch', function (req, res) {
    var city = req.body.keyword;
    console.log(city);
    var sql = `SELECT avg(Price) as temp, pr.ProductName as temp2
                FROM Purchase pu NATURAL JOIN Store s
                JOIN Has h ON (pu.PurchaseID = h.H_purchaseID)
                JOIN Product pr ON (h.H_productID=pr.ProductID)
                WHERE s.StoreID IN (SELECT StoreID FROM Store WHERE City = "${city}")
                GROUP BY h.H_productID
                ORDER BY count(H_productID) DESC LIMIT 15`;
    console.log(sql);
    connection.query(sql, function (err, rows) {
        if (err) {
            res.send('Failed: something messed up idk though lol')
        } else {
	    console.log(rows);
            res.render('advancedqueryONE', { data: rows });
        }
    });
});

// advanced query2
app.get('/freezer', (req, res) => {
    var space = req.body.Freezer;
    var sqlQry2 = `select round(temp.avgPrice,2) as avgPrice, Inv.StorageSpace, P.ProductName
                    from InventoryList Inv
                    join (select avg(Price) as avgPrice, H_productID
                            From Has group by H_productID) as temp on temp.H_productID = Inv.ProductID
                    join Product P on P.ProductID= Inv.ProductID
                    where Inv.StorageSpace = "Freezer"
                    order by temp.avgPrice desc limit 15`;
    connection.query(sqlQry2, function (error, result) {
        if (error) {
            res.send('Error in database operation');
        } else {
            console.log('The solution is: ', result);
            //res.send(result);
            res.render('freezer', { data: result });
        }
    });
});

//read
app.get('/db', (req, res) => {
    var sqlQry = 'select * from Product';
    connection.query(sqlQry, function (error, result) {
        if (error) {
            res.send('Error in database operation');
        } else {
            console.log('The solution is: ', result);
            //res.send(result);
            res.render('productList', { data: result });
        }
    });
});

//delete
app.get('/delete/:ProductID', function (req, res) {
    console.log('test');
    var id = req.params.ProductID;
    console.log('id= ', id);
    var sql = `delete from Product where ProductID= "${id}"`;
    console.log(sql);
    connection.query(sql, function (err, rows) {
        if (err) {
            res.end('Failed:' + err)
        } else {
            res.redirect('/db')
        }
    });
});

//update
app.get('/toUpdate/:ProductID', function (req, res) {
    var id = req.params.ProductID;
    console.log('id= ', id);
    var sql = `Select * from Product where ProductID= "${id}"`;
    console.log(sql);
    connection.query(sql, function (err, result) {
        if (err) {
            res.end('Failed:' + err);
        } else {
            console.log(result);
            res.render("update", { data: result });
        }
    });
});
app.post('/toUpdate/update', function (req, res, next) {
    var id = req.body.productid
    var plucode = req.body.plucode;
    var name = req.body.name;
    var lifespan = req.body.lifespan;
    var calories = req.body.calories;
    console.log(id);
    var sql = `Update Product Set PLUcode= "${plucode}", ProductName= "${name}", Lifespan = "${lifespan}",Calories="${calories}" Where ProductID = "${id}"`;

    console.log(sql);
    connection.query(sql, function (err, result) {
        if (err) throw err;
        console.log('record update');
        req.flash('success', 'Data added successfully!');
        res.redirect('/db');
    });
});



// catch 404 and forward to error handler
app.use(function (req, res, next) {
    next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error');
});

var http = require('http').Server(app);
var port = 80;
http.listen(port, function () {
    console.log('Listening to port 80');
})
/*
// port must be set to 3000 because incoming http requests are routed from port 80 to port 8$
app.listen(3000, function () {
   console.log('Node app is running on port 3000');
});
*/
module.exports = app;
