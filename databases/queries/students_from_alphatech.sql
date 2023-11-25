SELECT
	PESSOA.ID,
    PESSOA.NOMECOMPLETO AS FULLNAME,
    PESSOA.DATANASCIMENTO AS BIRTHDATE,
    PESSOA.SEXO AS SEX,
    REPLACE(
	REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
	REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
	REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    REPLACE(
    	REPLACE(ALUNO.TURMA, 'ª', ' '),
        'º', ' '),
        '°', ' '),
        '(', ' '),
        ')', ' '),
        '9ANO', ' '),
        'ANO', ' '),
        'ano', ' '),
        'AN0', ' '),
        'ano', ' '),
        'MANHÃ', ''),
        '2022', ' '),
        '2023', ' '),
        'TARDE', ' '),
        'permanecente', ' '),
        'ANOD', ' '),
        'Ano', ' '),
        'ano', ' '),
        'ANAO', ' '),
        '4A', '4'),
        '-', ' '),
        'A', ' '),
        'B', ' '),
        'C', ' '),
        'c', ' '),
        'D', ' '),
        'E', ' '),
        'F', ' '),
        ' ', '') AS SCHOOL_YEAR

FROM PESSOA
LEFT JOIN ALUNO ON ALUNO.ID = PESSOA.ID
WHERE PESSOA.ID IN (
    SELECT MATRICULA.ALUNO_ID
    FROM MATRICULA
    WHERE MATRICULA.PROJETO_ID = 132
)
ORDER BY `SCHOOL_YEAR` ASC;