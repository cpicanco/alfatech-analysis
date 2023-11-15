SELECT
    ALUNO_ID

FROM
    MATRICULA

WHERE
    PROJETO_ID = 132
    AND PROGRAMA_ID = :PROGRAM_ID
    AND (FIM IS NOT NULL)

GROUP BY
    ALUNO_ID