<template>
  <div class="container">
    <h1>Menadżer haseł 🔐</h1>

    <form @submit.prevent="addPassword">
      <input v-model="form.service" placeholder="Serwis" required />
      <input v-model="form.login" placeholder="Login" required />
      <input v-model="form.password" placeholder="Hasło" required />
      <button type="submit">Zapisz</button>
    </form>

    <hr />

    <h2>Zapisane hasła:</h2>
    <ul>
      <li v-for="item in passwords" :key="item.id">
        <strong>{{ item.service }}</strong> – {{ item.login }} – {{ item.password }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        service: '',
        login: '',
        password: ''
      },
      passwords: []
    }
  },
  methods: {
    async addPassword() {
      await axios.post('http://127.0.0.1:8000/passwords', this.form)
      this.form = { service: '', login: '', password: '' }
      this.fetchPasswords()
    },
    async fetchPasswords() {
      const response = await axios.get('http://127.0.0.1:8000/passwords')
      this.passwords = response.data
    }
  },
  mounted() {
    this.fetchPasswords()
  }
}
</script>

<style>
.container {
  max-width: 500px;
  margin: auto;
  font-family: sans-serif;
}
input {
  display: block;
  margin: 5px 0;
  padding: 6px;
  width: 100%;
}
button {
  margin-top: 10px;
  padding: 8px 12px;
}
</style>
