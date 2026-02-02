<template>
  <div class="app-container">
    <h1>Menadżer Haseł</h1>

    <!-- 🔑 Pole do wpisania klucza -->
    <div class="key-section">
      <input v-model="decryptKey" type="text" placeholder="Wpisz klucz do odszyfrowania" />
      <button @click="fetchPasswords">Załaduj hasła</button>
    </div>

    <!-- Formularz dodawania -->
    <div class="form-section">
      <input v-model="newPassword.service" type="text" placeholder="Serwis" />
      <input v-model="newPassword.login" type="text" placeholder="Login" />
      <input v-model="newPassword.password" type="password" placeholder="Hasło" />
      <button @click="addPassword">Dodaj</button>
    </div>

    <!-- Lista haseł -->
    <ul>
      <li v-for="item in passwords" :key="item.id">
        <strong>{{ item.service }}</strong> – {{ item.login }} – 
        <span>{{ decrypted[item.id] || item.password }}</span>

        <button @click="decryptPassword(item.id, item.password)">Odszyfruj</button>
        <button @click="deletePassword(item.id)">Usuń</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      passwords: [],
      decrypted: {}, // przechowuje odszyfrowane hasła
      decryptKey: "", // wpisany przez użytkownika klucz
      newPassword: { service: "", login: "", password: "" },
    };
  },
  methods: {
    async fetchPasswords() {
      const res = await axios.get("http://127.0.0.1:8000/passwords");
      this.passwords = res.data;
    },
    async addPassword() {
      await axios.post("http://127.0.0.1:8000/passwords", this.newPassword);
      this.newPassword = { service: "", login: "", password: "" };
      this.fetchPasswords();
    },
    async deletePassword(id) {
      await axios.delete(`http://127.0.0.1:8000/passwords/${id}`);
      this.fetchPasswords();
    },
    async decryptPassword(id, encrypted) {
      if (!this.decryptKey) {
        alert("Podaj klucz do odszyfrowania!");
        return;
      }
      try {
        const res = await axios.post("http://127.0.0.1:8000/decrypt", {
          key: this.decryptKey.trim(),
          password: encrypted,
        });
        this.$set(this.decrypted, id, res.data.decrypted);
      } catch (err) {
        alert("Błędny klucz lub problem z odszyfrowaniem");
      }
    },
  },
  mounted() {
    this.fetchPasswords();
  },
};
</script>

<style>
/* 🔥 Dark mode */
body {
  background-color: #121212;
  color: #f5f5f5;
  font-family: Arial, sans-serif;
}

.app-container {
  max-width: 700px;
  margin: 30px auto;
  padding: 20px;
  background: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(0,0,0,0.5);
}

input, button {
  margin: 5px;
  padding: 8px;
  border-radius: 8px;
  border: none;
}

input {
  background: #2c2c2c;
  color: #fff;
}

button {
  background: #444;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #666;
}
</style>
