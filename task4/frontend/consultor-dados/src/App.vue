<template>
  <div class="container">
    <h1>Top 10 Operadoras de Saúde</h1>


    <div class="select-container">
      <label for="despesa">Selecione o Tipo de Despesa: </label>
      <select v-model="tipoDespesa" id="despesa">
        <option value="anual">Despesa Anual</option>
        <option value="trimestre">Despesa Último Trimestre</option>
        <option value="500 maiores">Dados de 500 empresas cadastradas</option>
      </select>
    </div>

    <button @click="fetchOperadoras" class="btn-fetch">Carregar Dados</button>

    <div class="operadoras-list">
      <div 
        v-for="(operadora, index) in operadoras" 
        :key="index" 
        class="operadora-card"
      >
        <h2 class="operadora-nome">{{ operadora.operadora }}</h2>
        <div class="operadora-detalhes">
          <p><strong>Registro ANS:</strong> {{ operadora.Registro_ANS }}</p>
          <p><strong>Despesas:</strong> {{ formatCurrency(operadora.total_despesas || operadora.total_despesas_sinistros) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const operadoras = ref([])
const tipoDespesa = ref('anual')

const formatCurrency = (value) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 2
  }).format(value)
}

const fetchOperadoras = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/data?tipo=${tipoDespesa.value}`)
    console.log("Dados recebidos: ",response.data.results)
    operadoras.value = response.data.results
  } catch (error) {
    console.error('Erro ao buscar operadoras:', error)
  }
}
</script>

<style scoped>

body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f7f6;
}

h1 {
  font-size: 2.5rem;
  color: #1828b9;
  margin-bottom: 30px;
  text-align: center;
}


.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}


.select-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  font-size: 1.1rem;
}

select {
  padding: 8px 16px;
  margin-left: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #ffffff;
  font-size: 1rem;
}


.btn-fetch {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 12px 24px;
  font-size: 1.1rem;
  cursor: pointer;
  display: block;
  margin: 0 auto;
  margin-bottom: 30px;
  transition: background-color 0.3s;
}

.btn-fetch:hover {
  background-color: #0056b3;
}


.operadoras-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  justify-items: center;
}


.operadora-card {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.operadora-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.operadora-nome {
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.operadora-detalhes p {
  font-size: 1rem;
  color: #555;
  margin: 5px 0;
}

strong {
  color: #007bff;
}

p{
  font-weight: 700;
  font-size: x-large;
}

select{
  color: black;
  font-size: xx-large;
  
}


@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }

  .btn-fetch {
    font-size: 1rem;
  }

  .operadora-nome {
    font-size: 1.2rem;
  }

  .operadora-card {
    padding: 15px;
  }

  .select-container {
    flex-direction: column;
    text-align: center;
    font-size: x-small;
  }

  select {
    margin: 10px 0;
  }
}
</style>
