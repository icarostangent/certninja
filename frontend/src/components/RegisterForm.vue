<template>
  <div class="w-full max-w-xs mx-auto">
    <form
      @submit.prevent="register()"
      class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
    >
      <div class="mb-4">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="username"
        >
          Username
        </label>
        <input
          v-model="form.username"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="username"
          type="text"
          placeholder="Username"
        />
      </div>

      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="email">
          Email
        </label>
        <input
          v-model="form.email"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="email"
          type="text"
          placeholder="Email"
        />
      </div>

      <div class="mb-6">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="password"
        >
          Password
        </label>
        <input
          v-model="form.password"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
          id="password"
          type="password"
          placeholder="•••••••••••"
        />
      </div>

      <div class="mb-6">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="password-confirm"
        >
          Password Confirmation
        </label>
        <input
          v-model="form.passwordConfirm"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
          id="password-confirm"
          type="password"
          placeholder="•••••••••••"
        />
      </div>

      <div class="flex items-center justify-between">
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Sign In
        </button>
      </div>
    </form>
    <p class="text-center text-gray-500 text-xs">
      &copy;2020 All rights reserved.
    </p>
  </div>
</template>
<script>
import { useToast } from "vue-toastification";

export default {
  data() {
    return {
      form: {
        username: "",
        email: "",
        password: "",
        passwordConfirm: "",
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
        useToast().warning("username must be at least 6 characters");
        return;
      }
      if (!this.form.email.toLowerCase().match(emailRegex)) {
        useToast().warning("please enter a valid email address");
        return;
      }
      if (!this.form.password.match(passwordRegex)) {
        useToast().warning(
          "password must be 8 characters, contain at least one capital and one lowercase letter, and have at least one special character"
        );
        return;
      }
      if (this.form.password !== this.form.passwordConfirm) {
        useToast().warning("passwords must match");
        return;
      }
      try {
        const res = await this.$store.dispatch("register", this.form);
        this.$router.push("thanks");
      } catch (e) {
        if (e.response && e.response.data.code === "missing-parameters") {
          useToast().warning("all fields are required");
          return;
        }
        if (e.response && e.response.data.code === "cant-create") {
          useToast().warning("username or email already registered");
          return;
        }
        useToast().error("network unavailable");
      }
    },
  },
};
</script>
