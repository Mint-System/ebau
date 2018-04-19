-- PK for ACTIVATION_ANSWER Table
ALTER TABLE ACTIVATION_ANSWER ADD( ID number );
CREATE SEQUENCE ID_SEQ START WITH 1 INCREMENT BY 1 CACHE 20;
UPDATE ACTIVATION_ANSWER SET ID = ID_SEQ.nextval;
ALTER TABLE ACTIVATION_ANSWER DROP PRIMARY KEY;
ALTER TABLE ACTIVATION_ANSWER ADD CONSTRAINT PKACTIVATION_ANSWER PRIMARY KEY( ID );

-- PK for BAB_USAGE Table
ALTER TABLE BAB_USAGE ADD( ID number );
CREATE SEQUENCE BAB_USAGE_ID_SEQ START WITH 1 INCREMENT BY 1 CACHE 20;
UPDATE BAB_USAGE SET ID = BAB_USAGE_ID_SEQ.nextval;
ALTER TABLE BAB_USAGE DROP PRIMARY KEY;
ALTER TABLE BAB_USAGE ADD CONSTRAINT PKBAB_USAGE PRIMARY KEY( ID );

-- PK for FORM_GROUP_FORM Table
ALTER TABLE FORM_GROUP_FORM ADD( ID number );
CREATE SEQUENCE FORM_GROUP_FORM_ID_SEQ START WITH 1 INCREMENT BY 1 CACHE 20;
UPDATE FORM_GROUP_FORM SET ID = FORM_GROUP_FORM_ID_SEQ.nextval;
ALTER TABLE FORM_GROUP_FORM ADD CONSTRAINT PKFORM_GROUP_FORM PRIMARY KEY( ID );

-- PK for NOTICE Table
ALTER TABLE NOTICE ADD( ID number );
CREATE SEQUENCE NOTICE_ID_SEQ START WITH 1 INCREMENT BY 1 CACHE 20;
UPDATE NOTICE SET ID = NOTICE_ID_SEQ.nextval;
ALTER TABLE NOTICE DROP PRIMARY KEY;
ALTER TABLE NOTICE ADD CONSTRAINT PKNOTICE PRIMARY KEY( ID );

-- PK for LETTER Table
ALTER TABLE LETTER ADD( ID number );
CREATE SEQUENCE LETTER_ID_SEQ START WITH 1 INCREMENT BY 1 CACHE 20;
UPDATE LETTER SET ID = LETTER_ID_SEQ.nextval;
ALTER TABLE LETTER DROP PRIMARY KEY;
ALTER TABLE LETTER ADD CONSTRAINT PKLETTER PRIMARY KEY( ID );

-- FK for INSTANCE.LOCATION_ID -> LOCATION.LOCATION_ID Table
ALTER TABLE INSTANCE ADD( LOCATION_ID number );
ALTER TABLE INSTANCE ADD CONSTRAINT INSTANCE_LOCATION_ID_FK FOREIGN KEY (LOCATION_ID) REFERENCES LOCATION (LOCATION_ID);

-- Add IDENTIFIER column to INSTANCE Table
ALTER TABLE INSTANCE ADD( IDENTIFIER varchar2(50) DEFAULT NULL);

-- FK for ATTACHMENT.GROUP_ID -> GROUP.GROUP_ID Table
ALTER TABLE ATTACHMENT ADD( GROUP_ID number );

ALTER TABLE ATTACHMENT ADD CONSTRAINT ATTACHMENT_GROUP_ID_FK FOREIGN KEY (GROUP_ID) REFERENCES "GROUP" (GROUP_ID);

-- Camac Core changes picked from RELEASE-NOTE.md
ALTER TABLE ANSWER_LIST MODIFY NAME VARCHAR2(1000);
ALTER TABLE INSTANCE_STATE ADD DESCRIPTION VARCHAR2(1000) DEFAULT NULL;
ALTER TABLE QUESTION ADD VALIDATION VARCHAR2(50) DEFAULT NULL;
