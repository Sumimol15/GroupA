create table users(userId int primary key,userName varchar(100) unique,firstName varchar(100),lastName varchar(100),emailId varchar(100) unique,password varchar(100),creationDateTime TIMESTAMP); 
--The table messages used to store messages
create table messages(messageId int primary key, sentBy int foreign key references users(userId),recipientId int foreign key references users(userId),messageContent varchar(3000),messageCreationTime TIMESTAMP,readStatus varchar(15) )
