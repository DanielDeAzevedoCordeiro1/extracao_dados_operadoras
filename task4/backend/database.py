import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123",
            database="ans_db",
        )
        return connection
    except Error as e:
        print(e)
        return None


def get_maior_despesa_trimestral():
    return """
        WITH ultimo_periodo AS (
        SELECT MAX(DATA) AS data_maxima
        FROM dems_contabeis
    ),
    ultimo_trimestre AS (
        SELECT
            YEAR(data_maxima) AS ano,
            QUARTER(data_maxima) AS trimestre
        FROM
            ultimo_periodo
    )
    SELECT
        o.Razao_Social AS operadora,
        o.Registro_ANS,
        d.VL_SALDO_FINAL - d.VL_SALDO_INICIAL AS total_despesas_sinistros
    FROM
        dems_contabeis d
    JOIN
        operadoras o ON d.REG_ANS = o.Registro_ANS
    JOIN
        ultimo_trimestre ut ON YEAR(d.DATA) = ut.ano AND QUARTER(d.DATA) = ut.trimestre
    WHERE
        d.DESCRICAO LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%'
    GROUP BY
        o.Razao_Social, o.Registro_ANS
    ORDER BY
        total_despesas_sinistros DESC
    LIMIT 10;
"""


def get_maior_despesa_ultimo_ano():
    return """
       SELECT 
    d.REG_ANS,
    (SELECT razao_social FROM operadoras WHERE operadoras.registro_ans = d.REG_ANS LIMIT 1) AS nome_operadora,
    SUM(
        CASE 
            -- Contas que começam com (-) são de natureza credora (reduzem despesa)
            WHEN d.DESCRICAO LIKE '(-) %' THEN -1 * (COALESCE(d.VL_SALDO_FINAL, 0) - COALESCE(d.VL_SALDO_INICIAL, 0))
            -- Contas normais de despesa aumentam o total
            ELSE (COALESCE(d.VL_SALDO_FINAL, 0) - COALESCE(d.VL_SALDO_INICIAL, 0))
        END
    ) AS total_despesas
FROM 
    dems_contabeis d
WHERE
    -- Apenas contas de despesa (classe 4)
    d.CD_CONTA_CONTABIL LIKE '4%'
    -- Filtrar pelo ano de 2024
    AND d.DATA BETWEEN '2024-01-01' AND '2024-12-31'
    -- Filtrar pela descrição específica
    AND d.DESCRICAO LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%'
GROUP BY 
    d.REG_ANS
ORDER BY 
    total_despesas DESC
LIMIT 10;
"""