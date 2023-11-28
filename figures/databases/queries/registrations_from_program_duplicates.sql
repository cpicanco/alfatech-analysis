/* return  */
SELECT
	ALUNO_ID,
    INICIO,
    FIM,
    SUSPENSA
FROM MATRICULA
WHERE ALUNO_ID IN (
    SELECT ALUNO_ID
    FROM MATRICULA
    WHERE PROJETO_ID = 132 AND PROGRAMA_ID = :PROGRAM_ID
    GROUP BY ALUNO_ID
    HAVING COUNT(ALUNO_ID) > 1
)
AND PROJETO_ID = 132 AND PROGRAMA_ID = :PROGRAM_ID
ORDER BY ALUNO_ID, INICIO