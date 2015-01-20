SELECT
	"INSTANCE"."INSTANCE_ID"   AS "INSTANCE_ID",
	"ANSWER_DOK_NR"."ANSWER"   AS "DOSSIER_NR",
	"FORM"."NAME"              AS "FORM",
	"LOCATION"."NAME"          AS "COMMUNITY",
	"USER"."USERNAME"          AS "USER",
	CASE WHEN
			"ANSWER_COMPANY"."ANSWER" IS NOT NULL 
		THEN "ANSWER_COMPANY"."ANSWER"
		ELSE "ANSWER_APPLICANT"."ANSWER"
	END AS "PETITION",
	(SELECT LISTAGG("NAME", ', ') WITHIN GROUP (ORDER BY "NAME") 
		FROM INTENTIONS WHERE "INSTANCE_ID" = "INSTANCE"."INSTANCE_ID") AS "INTENT",
	"ANSWER_STREET"."ANSWER"     AS "STREET",
	"INSTANCE_STATE"."NAME"    AS "STATE",
	"INSTANCE_STATE_DESCRIPTION"."DESCRIPTION"    AS "STATE_DESCRIPTION"
FROM
	"INSTANCE"
JOIN
	"INSTANCE_LOCATION" ON (
		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"
	)
JOIN 
	"LOCATION" ON (
	 "INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"
	)
JOIN
	FORM ON (
		"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"
)
JOIN
	"USER" ON (
		"INSTANCE"."USER_ID" = "USER"."USER_ID"
)
JOIN
	"ANSWER" "ANSWER_DOK_NR" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_DOK_NR"."INSTANCE_ID"
		AND
		"ANSWER_DOK_NR"."QUESTION_ID" = 6
		AND
		"ANSWER_DOK_NR"."CHAPTER_ID" = 2
		AND
		"ANSWER_DOK_NR"."ITEM" = 1
	)
LEFT JOIN
	"ANSWER" "ANSWER_APPLICANT" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_APPLICANT"."INSTANCE_ID"
		AND
		"ANSWER_APPLICANT"."QUESTION_ID" = 23
		AND
		"ANSWER_APPLICANT"."CHAPTER_ID" = 1
		AND
		"ANSWER_APPLICANT"."ITEM" = 1
	)
LEFT JOIN 
	"ANSWER" "ANSWER_COMPANY" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_COMPANY"."INSTANCE_ID"
		AND
		"ANSWER_COMPANY"."QUESTION_ID" = 221
		AND
		"ANSWER_COMPANY"."CHAPTER_ID" = 1
		AND
		"ANSWER_COMPANY"."ITEM" = 1
	)
LEFT JOIN
	"ANSWER" "ANSWER_STREET" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET"."INSTANCE_ID"
		AND
		"ANSWER_STREET"."QUESTION_ID" = 93
		AND
		"ANSWER_STREET"."CHAPTER_ID" = 101
		AND
		"ANSWER_STREET"."ITEM" = 1
	)
JOIN 
	"INSTANCE_STATE" ON (
	"INSTANCE_STATE"."NAME" = 'redac'
)
LEFT JOIN
	"INSTANCE_STATE_DESCRIPTION" ON (
		"INSTANCE_STATE_DESCRIPTION"."INSTANCE_STATE_ID" = "INSTANCE"."INSTANCE_STATE_ID"
	)
JOIN
	"FORM_GROUP_FORM" ON (
	"FORM_GROUP_FORM"."FORM_ID" = "INSTANCE"."FORM_ID"
)
WHERE
	"INSTANCE"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"
	AND
	"FORM_GROUP_FORM"."FORM_GROUP_ID" = 141
