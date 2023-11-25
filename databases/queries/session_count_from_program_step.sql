SELECT
    COUNT(SESSAOEXEC.ID) AS SESSAO_COUNT

FROM PESSOA
    INNER JOIN MATRICULA
        ON PESSOA.ID = MATRICULA.ALUNO_ID

    LEFT JOIN ALUNO
        ON PESSOA.ID = ALUNO.ID

    INNER JOIN SESSAOEXEC
        ON MATRICULA.ID = SESSAOEXEC.MATRICULA_ID

    INNER JOIN PASSOEXEC
        ON SESSAOEXEC.ID = PASSOEXEC.SESSAOEXEC_ID

    INNER JOIN PASSOOCORRENCIA AS PASSO_OCOR
        ON PASSOEXEC.OCORRENCIA_ID = PASSO_OCOR.ID

    LEFT JOIN PASSO
        ON PASSO.ID = PASSO_OCOR.PASSO_ID

WHERE
    SESSAOEXEC.CANCELADA = 0
    AND MATRICULA.ID = :REGISTRATION_ID
    AND MATRICULA.PROJETO_ID = 132
    AND MATRICULA.PROGRAMA_ID = :PROGRAM_ID
    AND PASSO.ID = :STEP_ID
    AND MATRICULA.ALUNO_ID = :STUDENT_ID
GROUP BY PASSO.ID, MATRICULA.ALUNO_ID
ORDER BY MATRICULA.ALUNO_ID ASC;