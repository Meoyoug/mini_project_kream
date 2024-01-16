create schema kream_new_product

use kream_new_product

create table products (
    productID int PRIMARY KEY AUTO_INCREMENT,
    category varchar(10),
    brand varchar(20),
    product varchar(50),
    price int,
    gender varchar(6)
)
