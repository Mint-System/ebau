# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-11 09:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180430_1156'),
    ]

    operations = [
        migrations.RunSQL(
            """
CREATE OR REPLACE VIEW "APPLICANT_VIEW" AS
SELECT
"INSTANCE"."INSTANCE_ID",
(SELECT string_agg("ANSWER", ', ' ORDER BY "QUESTION_ID" DESC)
  FROM
  "ANSWER"
  WHERE
  "INSTANCE"."INSTANCE_ID" = "ANSWER"."INSTANCE_ID"
  AND
  (
    "ANSWER"."QUESTION_ID" = 23
    OR
    "ANSWER"."QUESTION_ID" = 221
  )
  AND
  "ANSWER"."CHAPTER_ID" = 1
  AND
  "ANSWER"."ITEM" = 1
) AS "APPLICANT"
FROM "INSTANCE";

CREATE OR REPLACE  VIEW "ANSWER_STREET_BG" AS
SELECT
"ANSWER",
"INSTANCE_ID"
FROM
"ANSWER"
WHERE
"QUESTION_ID" = 93
AND
"CHAPTER_ID" = 21
AND
"ITEM" = 1;

CREATE OR REPLACE  VIEW "ANSWER_STREET_NP" AS
SELECT
"ANSWER",
"INSTANCE_ID"
FROM
"ANSWER"
WHERE
"QUESTION_ID" = 93
AND
"CHAPTER_ID" = 101
AND
"ITEM" = 1;

CREATE OR REPLACE  VIEW "ANSWER_STREET_247" AS
SELECT
"ANSWER",
"INSTANCE_ID"
FROM
"ANSWER"
WHERE
"QUESTION_ID" = 93
AND
"CHAPTER_ID" = 102
AND
"ITEM" = 1;

create or replace FUNCTION "GET_INST_STATE_DESCRIPTION" (STATE_NAME VARCHAR)
RETURNS varchar AS $$
DECLARE
DESCRIPTION varchar;
BEGIN
  SELECT
  "DESCRIPTION" into DESCRIPTION
  FROM
  "INSTANCE_STATE_DESCRIPTION"
  WHERE
  "INSTANCE_STATE_ID" = "GET_INST_STATE_ID_BY_NAME"(STATE_NAME);
  RETURN DESCRIPTION;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION
"GET_INST_STATE_ID_BY_NAME" (STATE_NAME VARCHAR)
RETURNS integer AS $$
DECLARE
ID integer;
BEGIN
  SELECT
  "INSTANCE_STATE_ID" into ID
  FROM
  "INSTANCE_STATE"
  WHERE
  LOWER("NAME") = LOWER(STATE_NAME);
  RETURN ID;
END;
$$ LANGUAGE plpgsql;

create or replace FUNCTION
"GET_INST_STATE_NAME_BY_ID" (STATE_ID integer)
RETURNS varchar AS $$
DECLARE
STATE_NAME varchar;
BEGIN
  SELECT
  "NAME" into STATE_NAME
  FROM
  "INSTANCE_STATE"
  WHERE
  "INSTANCE_STATE_ID" = STATE_ID;
  RETURN STATE_NAME;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE VIEW "PRESET_INTENTIONS" ("NAME", "VALUE", "INSTANCE_ID") AS
SELECT
"ANSWER_LIST"."NAME",
"ANSWER_LIST"."VALUE",
"ANSWER"."INSTANCE_ID"
FROM
"ANSWER_LIST"
JOIN
"ANSWER" ON (
    "ANSWER"."QUESTION_ID" = 97
    AND
    "CHAPTER_ID" = 21
    AND
    "ITEM" = 1
)
WHERE
"ANSWER_LIST"."QUESTION_ID" = 97
AND
"ANSWER"."ANSWER"::jsonb ? "ANSWER_LIST"."VALUE";

CREATE OR REPLACE VIEW "OTHER_INTENTIONS" ("ANSWER", "INSTANCE_ID") AS
SELECT
"ANSWER",
"INSTANCE_ID"
FROM
"ANSWER"
WHERE
(
    "QUESTION_ID" = 98
    AND
    (
        "CHAPTER_ID" = 21
        OR
        "CHAPTER_ID" = 101
    )
    AND
    "ITEM" = 1
)
OR
(
    "QUESTION_ID" = 93
    AND
    "CHAPTER_ID" = 102
);

CREATE OR REPLACE VIEW "INTENTIONS" AS
SELECT
"PRESET_INTENTIONS"."NAME"         "NAME",
"PRESET_INTENTIONS"."INSTANCE_ID"  "INSTANCE_ID"
FROM
"PRESET_INTENTIONS"
UNION
SELECT
"OTHER_INTENTIONS"."ANSWER"       "NAME",
"OTHER_INTENTIONS"."INSTANCE_ID"  "INSTANCE_ID"
FROM
"OTHER_INTENTIONS";


CREATE OR REPLACE VIEW "ANSWER_DOK_NR" AS
SELECT
"ANSWER",
"INSTANCE_ID"
FROM
"ANSWER"
WHERE
"QUESTION_ID" = 6
AND
"CHAPTER_ID" = 2
AND
"ITEM" = 1;

CREATE OR REPLACE VIEW "APPLICANT_DATA_VIEW" AS
SELECT
    "NAME_TBL"."ANSWER" "NAME",
    "EMAIL_TBL"."ANSWER" "EMAIL",
    "NAME_TBL"."INSTANCE_ID" "INSTANCE_ID"
FROM
    "ANSWER" "NAME_TBL"

JOIN
    "ANSWER" "EMAIL_TBL"
ON (
        "EMAIL_TBL"."CHAPTER_ID" = 1
    AND
        "EMAIL_TBL"."QUESTION_ID" = 66
    AND
        "EMAIL_TBL"."ITEM" = 1
)

WHERE
        "NAME_TBL"."CHAPTER_ID" = 1
    AND
        "NAME_TBL"."QUESTION_ID" = 23
    AND
        "NAME_TBL"."ITEM" = 1

    AND
        "NAME_TBL"."INSTANCE_ID" = "EMAIL_TBL"."INSTANCE_ID"
;


CREATE OR REPLACE VIEW "PROJECT_AUTHOR_DATA_VIEW" AS
SELECT
    "NAME_TBL"."ANSWER" "NAME",
    "EMAIL_TBL"."ANSWER" "EMAIL",
    "NAME_TBL"."INSTANCE_ID" "INSTANCE_ID"
FROM
    "ANSWER" "NAME_TBL"

JOIN
    "ANSWER" "EMAIL_TBL"
ON (
        "EMAIL_TBL"."CHAPTER_ID" = 1
    AND
        "EMAIL_TBL"."QUESTION_ID" = 77
    AND
        "EMAIL_TBL"."ITEM" = 1
)

WHERE
        "NAME_TBL"."CHAPTER_ID" = 1
    AND
        "NAME_TBL"."QUESTION_ID" = 71
    AND
        "NAME_TBL"."ITEM" = 1

    AND
        "NAME_TBL"."INSTANCE_ID" = "EMAIL_TBL"."INSTANCE_ID"
;



CREATE OR REPLACE VIEW "PROJECT_SUBMITTER_VIEW" AS
SELECT
    "ANSWER",
    "INSTANCE_ID"
FROM
    "ANSWER" "NAME_TBL"
WHERE
        "NAME_TBL"."CHAPTER_ID" = 103
    AND
        "NAME_TBL"."QUESTION_ID" = 257
    AND
        "NAME_TBL"."ITEM" = 1
;

CREATE OR REPLACE VIEW "PROJECT_SUBMITTER_DATA" AS
SELECT
    CASE
        "PROJECT_SUBMITTER_VIEW"."ANSWER"
        WHEN '0' THEN "APPLICANT_DATA_VIEW"."NAME"
        WHEN '1' THEN "PROJECT_AUTHOR_DATA_VIEW"."NAME"
    END "NAME",
    CASE
        "PROJECT_SUBMITTER_VIEW"."ANSWER"
        WHEN '0' THEN "APPLICANT_DATA_VIEW"."EMAIL"
        WHEN '1' THEN "PROJECT_AUTHOR_DATA_VIEW"."EMAIL"
    END "EMAIL",
    "PROJECT_SUBMITTER_VIEW"."INSTANCE_ID",
    "PROJECT_SUBMITTER_VIEW"."ANSWER"
FROM
    "PROJECT_SUBMITTER_VIEW"
LEFT JOIN
    "APPLICANT_DATA_VIEW" ON
    "PROJECT_SUBMITTER_VIEW"."INSTANCE_ID" = "APPLICANT_DATA_VIEW"."INSTANCE_ID"
LEFT JOIN
    "PROJECT_AUTHOR_DATA_VIEW" ON
    "PROJECT_SUBMITTER_VIEW"."INSTANCE_ID"= "PROJECT_AUTHOR_DATA_VIEW"."INSTANCE_ID"
;
"""
        )
    ]
