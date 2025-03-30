from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection, get_maior_despesa_trimestral, get_maior_despesa_ultimo_ano

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

query2_anual = """
    WITH ultimo_ano AS (
        SELECT MAX(YEAR(DATA)) AS ano
        FROM dems_contabeis
    )
    SELECT
        o.Razao_Social AS operadora,
        o.Registro_ANS,
        SUM(d.VL_SALDO_FINAL) AS total_despesas
    FROM
        dems_contabeis d
    JOIN
        operadoras o ON d.REG_ANS = o.Registro_ANS
    JOIN
        ultimo_ano u ON YEAR(d.DATA) = u.ano
    WHERE
        d.CD_CONTA_CONTABIL LIKE '4%'  
    GROUP BY
        o.Razao_Social, o.Registro_ANS
    ORDER BY
        total_despesas DESC
    LIMIT 10;
"""

query1_trimestre = """
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
        SUM(d.VL_SALDO_FINAL) AS total_despesas_sinistros
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


@app.get("/api/data")
async def get_operadoras(tipo: str = 'anual'):
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = connection.cursor(dictionary=True)
        
        if tipo == 'anual':
            cursor.execute(query2_anual)
        else:
            cursor.execute(query1_trimestre)
        results = cursor.fetchall()
        return {"results": results}
    except Exception as e:
        print(e)
        return {"results": []}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            

            
               