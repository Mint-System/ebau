alter table billing_entry add "CREATED" DATE;
alter table billing_entry add "AMOUNT_TYPE" NUMBER(1,0) DEFAULT 0 NOT NULL;
alter table billing_entry add "TYPE" NUMBER(1,0) DEFAULT 0 NOT NULL;
alter table billing_entry add "REASON" VARCHAR2(300);
alter table billing_entry add "INVOICED" NUMBER(1,0) DEFAULT 0 NOT NULL;


--- THE CONFIG TABLE

CREATE TABLE BILLING_CONFIG
(
  BILLING_CONFIG_ID NUMBER NOT NULL
, NAME VARCHAR2(100) NOT NULL
, VALUE VARCHAR2(300) NOT NULL
, CONSTRAINT BILLING_CONFIG_PK PRIMARY KEY
  (
    BILLING_CONFIG_ID
  )
  ENABLE
);


CREATE SEQUENCE BILLING_CONFIG_SEQ INCREMENT BY 1 START WITH 1 MAXVALUE 9000000 MINVALUE 1 ORDER;

INSERT INTO "CAMAC"."AIR_ACTION" (AVAILABLE_INSTANCE_RESOURCE_ID, ACTION_NAME, HIDDEN) VALUES ('billing', 'complete', '1')

