<template>
  <div class="w-full max-w-xs mx-auto">
    <form @submit.prevent="register()" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
          Username
        </label>
        <input v-model="form.username"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="username" type="text" placeholder="Username" />
      </div>

      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
          Email
        </label>
        <input v-model="form.email"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="email" type="text" placeholder="Email" />
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
          Password
        </label>
        <input v-model="form.password"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
          id="password" type="password" placeholder="•••••••••••" />
      </div>

      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="password-confirm">
          Password Confirmation
        </label>
        <input v-model="form.password2"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
          id="password-confirm" type="password" placeholder="•••••••••••" />
      </div>

      <div class="flex items-center justify-between">
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit">
          Sign Up
        </button>
      </div>
    </form>
  </div>
</template>
<script>
export default {
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        password2: "",
      },
    };
  },
  methods: {
    async register() {
      let emailRegex =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      let passwordRegex =
        /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%&*()]).{8,}/;

      if (this.form.username.length < 6) {
        this.$store.commit("SET_MESSAGE", { title: "Error", text: "Username must be 6 at least characters", display: true, style: "bg-warning" })
        return;
      }
      if (!this.form.email.toLowerCase().match(emailRegex)) {
        this.$store.commit("SET_MESSAGE", { title: "Error", text: "Please enter a valid email address", display: true, style: "bg-warning" })
        return;
      }
      if (!this.form.password.match(passwordRegex)) {
        this.$store.commit("SET_MESSAGE", { title: "Error", text: "password must be 8 characters, contain at least one capital and one lowercase letter, and have at least one special character", display: true, style: "bg-warning" })
        return;
      }
      if (this.form.password !== this.form.password2) {
        this.$store.commit("SET_MESSAGE", { title: "Error", text: "Passwords must match", display: true, style: "bg-warning" })
        return;
      }
      try {
        const res = await this.$store.dispatch("register", this.form);
        this.$store.commit("SET_MESSAGE", { title: "Success", text: "Welcome to CertNinja", display: true, style: "bg-success" })
        this.$router.push({ name: "thanks" });
      } catch (e) {
        if (e.response && e.response.data.code === "missing-parameters") {
          this.$store.commit("SET_MESSAGE", { title: "Error", text: e.response.data, display: true, style: "bg-warning" })
          return;
        }
        if (e.response && e.response.data.code === "cant-create") {
          this.$store.commit("SET_MESSAGE", { title: "Error", text: e.response.data, display: true, style: "bg-warning" })
          return;
        }
        else {
          console.log(e.response.data)
          this.$store.commit("SET_MESSAGE", { title: "Error", text: e.response.data, display: true, style: "bg-warning" })
        }
      }
    },
  },
};
</script>
