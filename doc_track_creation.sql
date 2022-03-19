DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `DOC_TRACK_CREATION`()
BEGIN
DROP DATABASE document_tracking_system;
CREATE DATABASE document_tracking_system;
CREATE TABLE organisations (
    org_id int PRIMARY KEY,
    name varchar(255)
);
CREATE TABLE documents (
    doc_id int PRIMARY KEY, 
    type ENUM ('physical_paper','CD','harddrive'),
    name varchar(255),
    content varchar(255),
    creation_date date
);

CREATE TABLE drafts(
    draft_id int PRIMARY KEY,
    content varchar(255),
    doc_id int
);

CREATE TABLE copies(
    copy_id int PRIMARY KEY,
    content varchar(255),
    draft_id int
);

CREATE TABLE tracking(
    track_id int PRIMARY KEY,
    track_date date,
    copy_id int,
    user_id int
);

CREATE TABLE users(
    user_id int PRIMARY KEY,
    type enum ('employee','external_office'),
    name varchar(255),
    mailing_address varchar(255)
);

CREATE TABLE document_receive( 
receipt_id int PRIMARY KEY,
receipt_date date,
org_id int,
doc_id int,    
FOREIGN KEY (org_id) REFERENCES organisations(org_id) ,
FOREIGN KEY (doc_id) REFERENCES documents(doc_id) 
);

ALTER TABLE drafts
ADD FOREIGN KEY (doc_id) REFERENCES documents(doc_id) ;

ALTER TABLE copies
ADD FOREIGN KEY (draft_id) REFERENCES drafts(draft_id) ;

ALTER TABLE tracking
ADD FOREIGN KEY (copy_id) REFERENCES copies(copy_id) ,
ADD FOREIGN KEY (user_id) REFERENCES users(user_id) ;







END$$
DELIMITER ;