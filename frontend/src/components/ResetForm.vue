<template>
  <div class="w-full max-w-xs mx-auto">
    <form
      @submit.prevent="reset()"
      class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
    >
      <div class="mb-4">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="password"
        >
          Password
        </label>
        <input
          v-model="form.password"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="password"
          type="password"
          placeholder="Username"
        />
      </div>
      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="confirm">
          Confirm
        </label>
        <input
          v-model="form.passwordConfirm"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
          id="confirm"
          type="password"
          placeholder="•••••••••••"
        />
      </div>
      <div class="flex items-center justify-between">
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Submit
        </button>
      </div>
    </form>
  </div>
</template>
<script>
import { useToast } from "vue-toastification";

export default {
  data() {
    return {
      form: {
        password: "",
        passwordConfirm: "",
        key: this.$route.query.key,
        id: this.$route.query.id,
      },
    };
  },
  methods: {
    reset() {
      let passwordRegex =
        /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%&*()]).{8,}/;
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
        console.log(this.form);
        this.$store.dispatch("reset", this.form);
        this.$router.push("login");
      } catch (e) {
        if (e.response && e.response.data.code === "missing-parameters") {
          useToast().warning("all fields are required");
          return;
        }
        useToast().error("network unavailable");
      }
    },
  },
};
</script>
