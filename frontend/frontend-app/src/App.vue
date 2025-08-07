<template>
  <div>
    <h1>Menadżer Haseł</h1>

    <form @submit.prevent="addPassword">
      <input
        type="text"
        v-model="newPassword.service"
        placeholder="Serwis"
        required
      />
      <input
        type="text"
        v-model="newPassword.login"
        placeholder="Login"
        required
      />
      <input
        type="password"
        v-model="newPassword.password"
        placeholder="Hasło"
        required
      />
      <button type="submit">Dodaj</button>
    </form>

    <ul>
      <li v-for="password in passwords" :key="password.id">
        <strong>{{ password.service }}</strong> — {{ password.login }}
        <button @click="deletePassword(password.id)">Usuń</button>
      </li>
    </ul>
  </div>
</template>




<script>
import axios from 'axios'

export default {
  data() {
    return {
      passwords: [],
      newPassword: {
        service: '',
        login: '',
        password: ''
      }
    }
  },
  methods: {
   async fetchPasswords() {
  const response = await axios.get('http://127.0.0.1:8000/passwords')
  console.log('Dane z backendu:', response.data) // DEBUG
  this.passwords = response.data
}
,
    async addPassword() {
      await axios.post('http://127.0.0.1:8000/passwords', this.newPassword)
      this.newPassword = { service: '', login: '', password: '' }
      this.fetchPasswords()
    },
    async deletePassword(id) {
      await axios.delete(`http://127.0.0.1:8000/passwords/${id}`)
      this.fetchPasswords()
    }
  },
  mounted() {
    this.fetchPasswords()
  }
}
</script>


<style>
body {
  background-color: #f2f2f2; /* lekko szare tło */
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 20px;
}

h1 {
  color: #333333; /* ciemny szary */
  text-align: center;
  margin-bottom: 30px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 400px;
  margin: 0 auto 30px auto;
}

input {
  padding: 10px;
  font-size: 16px;
}

button {
  padding: 10px;
  font-size: 16px;
  background-color: #007BFF; /* niebieski */
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3; /* ciemniejszy niebieski przy najechaniu */
}

ul {
  list-style: none;
  padding: 0;
  max-width: 600px;
  margin: 0 auto;
}

li {
  background-color: white;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

li strong {
  color: #333333;
}

li button {
  background-color: #dc3545; /* czerwony dla "Usuń" */
}

li button:hover {
  background-color: #a71d2a;
}
</style>
