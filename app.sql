create database if not exists app;

use app;

create table if not exists basic_info (
    id int auto_increment primary key,
    name char(50) not null,
    package char(100) not null,
    version char(30) not null,
    path char(100) not null
);
