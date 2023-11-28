SELECT
    TENTATIVAINTERACAO.RESULTADO,
    TENTATIVAINTERACAO.LATENCIA,
    TENTATIVAINTERACAO.DTYPE,
    TENTATIVAINTERACAO.TENTATIVAEXEC_ID,
    TENTATIVAINTERACAO.NROINTERACAO,
    TENTATIVAEXEC.MOMENTOINICIO AS TENTATIVA_EXECUCAO_INICIO,
    TENTATIVAEXEC.MOMENTOFIM AS TENTATIVA_EXECUCAO_FIM,
    MATRICULA.ID AS MATRICULA_ID,
    MATRICULA.ALUNO_ID,
    PASSO_OCOR.PROGRAMA_ID,
    PASSO_OCOR.PASSO_ID AS PASSO_ID,
    PASSO.NOME AS PASSO_NOME,
    BLOCO.ID AS BLOCO_ID,
    BLOCO.NOME AS BLOCO_NOME,
    SESSAOEXEC.ID AS SESSAOEXEC_ID,
    SESSAOEXEC.CANCELADA,
    SESSAOEXEC.MOMENTOINICIO AS DATA_EXECUCAO_INICIO,
    SESSAOEXEC.MOMENTOFIM AS DATA_EXECUCAO_FIM,
    TENTATIVA.NOME AS TENTATIVA_NOME

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

    INNER JOIN BLOCOEXEC
        ON PASSOEXEC.ID = BLOCOEXEC.PASSOEXEC_ID

    INNER JOIN BLOCOOCORRENCIA
        ON BLOCOEXEC.OCORRENCIA_ID = BLOCOOCORRENCIA.ID

    LEFT JOIN BLOCO
        ON BLOCO.ID = BLOCOOCORRENCIA.BLOCO_ID

    INNER JOIN TENTATIVAEXEC
        ON BLOCOEXEC.ID = TENTATIVAEXEC.BLOCOEXEC_ID

    INNER JOIN TENTATIVAOCORRENCIA
        ON TENTATIVAEXEC.OCORRENCIA_ID = TENTATIVAOCORRENCIA.ID

    INNER JOIN TENTATIVA
        ON TENTATIVAOCORRENCIA.TENTATIVA_ID = TENTATIVA.ID

    INNER JOIN TENTATIVAINTERACAO
        ON TENTATIVAEXEC.ID = TENTATIVAINTERACAO.TENTATIVAEXEC_ID

WHERE
    SESSAOEXEC.CANCELADA = 0
    AND MATRICULA.PROJETO_ID = 132
    AND PASSO_OCOR.PROGRAMA_ID = :PROGRAM_ID
    AND MATRICULA.ID = :REGISTRATION_ID
    AND MATRICULA.ALUNO_ID = :STUDENT_ID
    AND PASSO_OCOR.PASSO_ID = :STEP_ID