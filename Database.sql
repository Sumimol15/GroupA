create table users(userId int primary key,userName varchar(100) unique,firstName varchar(100),lastName varchar(100),emailId varchar(100) unique,password varchar(100),creationDateTime DATETIME); 
--The table messages used to store messages
create table messages(messageId int primary key, sentBy int foreign key references users(userId),recipientId int foreign key references users(userId),messageContent varchar(3000),messageCreationTime DATETIME,readStatus varchar(15) );
create SEQUENCE userSequence; 
alter SEQUENCE userSequence RESTART WITH 1;


create SEQUENCE messageSequence; 
alter SEQUENCE messageSequence RESTART WITH 1;