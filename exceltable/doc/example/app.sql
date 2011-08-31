SELECT * FROM BAR;

-- TABLE: products start
CREATE TABLE products (
  id int(11) NOT NULL AUTO_INCREMENT,
  ProductName varchar(40) NOT NULL,
  SupplierID int(11) DEFAULT NULL,
  CategoryID int(11) DEFAULT NULL,
  QuantityPerUnit varchar(20) DEFAULT NULL,
  UnitPrice decimal(19,4) DEFAULT NULL,
  UnitsInStock smallint(6) DEFAULT NULL,
  UnitsOnOrder smallint(6) DEFAULT NULL,
  ReorderLevel smallint(6) DEFAULT NULL,
  Discontinued tinyint(4) NOT NULL,
  availableOnline bit(1) DEFAULT NULL,
  PRIMARY KEY (ProductID)
);
-- TABLE: products end

SELECT * FROM BAR;

-- Create table if it does not exist already
CREATE TABLE IF NOT EXISTS t1 (c1 CHAR(10)) SELECT 1, 2;


-- Property table
CREATE TABLE property (
  id int(11) NOT NULL AUTO_INCREMENT,
  -- Name of the property, e.g. 'color'
  name varchar(40) NOT NULL,
  -- Value of the property, e.g. 'red'
  value varchar(140) NOT NULL,
  PRIMARY KEY (id)
);


CREATE DATABASE hum;

-- Property table
CREATE TABLE bar (
  id int(101) NOT NULL AUTO_INCREMENT,
  value varchar(10) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE product (category INT NOT NULL, id INT NOT NULL, price DECIMAL,
  PRIMARY KEY(category, id)) ENGINE=INNODB;

CREATE TABLE customer (id INT NOT NULL,
                       PRIMARY KEY (id)) ENGINE=INNODB;

CREATE TABLE product_order (no INT NOT NULL AUTO_INCREMENT,
                            product_category INT NOT NULL,
                            product_id INT NOT NULL,
                            customer_id INT NOT NULL,
                            PRIMARY KEY(no),
                            INDEX (product_category, product_id),
                            FOREIGN KEY (product_category, product_id)
                              REFERENCES product(category, id)
                              ON UPDATE CASCADE ON DELETE RESTRICT,
                            INDEX (customer_id),
                            FOREIGN KEY (customer_id)
                              REFERENCES customer(id)) ENGINE=INNODB;

