select 
	"INSTANCE"."INSTANCE_ID" as "INSTANCE_ID",
	"DOSSIERNR"."ANSWER" as "DOSSIER_NR",
	"FORM"."NAME"        as "FORM",
	"USER"."USERNAME"        AS "USER",
	CASE WHEN
			"ANSWER_COMPANY"."ANSWER" IS NOT NULL 
		THEN "ANSWER_COMPANY"."ANSWER"
		ELSE "ANSWER_APPLICANT"."ANSWER"
	END AS "PETITION",
	(SELECT LISTAGG("NAME", ', ') WITHIN GROUP (ORDER BY "NAME") 
		FROM INTENTIONS WHERE "INSTANCE_ID" = "INSTANCE"."INSTANCE_ID") AS "INTENT",
	CASE
		WHEN "ANSWER_STREET_BG"."ANSWER" IS NOT NULL THEN "ANSWER_STREET_BG"."ANSWER"
		WHEN "ANSWER_STREET_NP"."ANSWER" IS NOT NULL THEN "ANSWER_STREET_NP"."ANSWER"
	END AS "STREET",
	GET_STATE_NAME_BY_ID("INSTANCE"."INSTANCE_STATE_ID") AS "STATE",
	"INSTANCE_STATE_DESCRIPTION"."DESCRIPTION"    AS "STATE_DESCRIPTION"

	
FROM "INSTANCE"

JOIN "INSTANCE_LOCATION" ON (
		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"
)

JOIN "LOCATION" ON (
		"INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"
)

LEFT JOIN "ANSWER"  "DOSSIERNR" ON (
		"DOSSIERNR"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"
		AND
		"DOSSIERNR"."QUESTION_ID" = 6
		AND
		"DOSSIERNR"."CHAPTER_ID" = 2
		AND
		"DOSSIERNR"."ITEM" = 1
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
	"ANSWER" "ANSWER_STREET_BG" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET_BG"."INSTANCE_ID"
		AND
		"ANSWER_STREET_BG"."QUESTION_ID" = 93
		AND
		"ANSWER_STREET_BG"."CHAPTER_ID" = 21
		AND
		"ANSWER_STREET_BG"."ITEM" = 1
	)
LEFT JOIN
	"ANSWER" "ANSWER_STREET_NP" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET_NP"."INSTANCE_ID"
		AND
		"ANSWER_STREET_NP"."QUESTION_ID" = 93
		AND
		"ANSWER_STREET_NP"."CHAPTER_ID" = 101
		AND
		"ANSWER_STREET_NP"."ITEM" = 1
	)

LEFT JOIN
	"INSTANCE_STATE_DESCRIPTION" ON (
		"INSTANCE_STATE_DESCRIPTION"."INSTANCE_STATE_ID" = "INSTANCE"."INSTANCE_STATE_ID"
	)

join "FORM" ON (
	"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"
)

JOIN "USER" ON (
		"INSTANCE"."USER_ID" = "USER"."USER_ID"
)
JOIN
	"GROUP_LOCATION" ON (
	 	"GROUP_LOCATION"."GROUP_ID" = [GROUP_ID]
	)
WHERE
	"GROUP_LOCATION"."LOCATION_ID" = "INSTANCE_LOCATION"."LOCATION_ID"

ORDER BY "INSTANCE"."INSTANCE_ID" DESC
