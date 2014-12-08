select distinct
	"INSTANCE"."INSTANCE_ID",
	"DOSSIERNR"."ANSWER" as "DOSSIER_NR",
	"FORM"."NAME"        as "FORM",
	"USER"."USERNAME"        AS "USER",
	"ANSWER_PETITION"."ANSWER" AS "PETITION",
	(
		SELECT
			LISTAGG("ANSWER_LIST"."NAME", ', ') WITHIN GROUP (ORDER BY "ANSWER_LIST"."NAME")
		FROM
			table(json_unserialize((
				SELECT
					"ANSWER" as "ANSW"
				FROM
					"ANSWER"
				WHERE
					"ANSWER"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"
					AND
					"QUESTION_ID" = 97
					AND
					"CHAPTER_ID" = 21
					AND
					"ITEM" = 1
				))
			)
		JOIN "ANSWER_LIST" ON (
			"VAL" = "ANSWER_LIST_ID"
		)
	) AS "INTENT",
	"ANSWER_CITY"."ANSWER"     AS "CITY",
	GET_STATE_NAME_BY_ID("INSTANCE"."INSTANCE_STATE_ID") AS "STATUS"
	
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

	"ANSWER" "ANSWER_PETITION" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_PETITION"."INSTANCE_ID"

		AND

		"ANSWER_PETITION"."QUESTION_ID" = 23

		AND

		"ANSWER_PETITION"."CHAPTER_ID" = 1

		AND

		"ANSWER_PETITION"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_INTENT" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_INTENT"."INSTANCE_ID"

		AND

		"ANSWER_INTENT"."QUESTION_ID" = 97

		AND

		"ANSWER_INTENT"."CHAPTER_ID" = 21

		AND

		"ANSWER_INTENT"."ITEM" = 1

	)

LEFT JOIN

	"ANSWER" "ANSWER_CITY" ON (

		"INSTANCE"."INSTANCE_ID" = "ANSWER_CITY"."INSTANCE_ID"

		AND

		"ANSWER_CITY"."QUESTION_ID" = 63

		AND

		"ANSWER_CITY"."CHAPTER_ID" = 1

		AND

		"ANSWER_CITY"."ITEM" = 1

	)



join "FORM" ON (
	"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"
)

JOIN "USER" ON (
		"INSTANCE"."USER_ID" = "USER"."USER_ID"
)

LEFT JOIN ANSWER  PARCEL_NR ON ( 
  "INSTANCE"."INSTANCE_ID" = "PARCEL_NR"."INSTANCE_ID" AND "PARCEL_NR".QUESTION_ID = 91 AND "PARCEL_NR".CHAPTER_ID =21 AND "PARCEL_NR".ITEM = 1
  )
JOIN
	"GROUP_LOCATION" ON (
	 	"GROUP_LOCATION"."GROUP_ID" = [GROUP_ID]
	)
WHERE
	"GROUP_LOCATION"."LOCATION_ID" = "INSTANCE_LOCATION"."LOCATION_ID"
