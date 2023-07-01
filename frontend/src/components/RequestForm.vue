<template>
  <div class="w-full max-w-xs mx-auto">
    <form
      @submit.prevent="submit()"
      class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
    >
      <div class="mb-4">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="username"
        >
          Email
        </label>
        <input
          v-model="form.email"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="username"
          type="text"
          placeholder="Username"
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
        email: "",
      },
    };
  },
  methods: {
    submit() {
      let emailRegex =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      if (this.form.email === "") {
        useToast().warning("email required");
        return;
      }
      if (!this.form.email.toLowerCase().match(emailRegex)) {
        useToast().warning("please enter a valid email address");
        return;
      }
      try {
        this.$store.dispatch("request", this.form);
        this.$router.push("thanks");
      } catch (e) {
        // if ( e.response && e.response.status === 403 ) {
        //   useToast().warning('invalid credentials')
        //   return
        // }
        // useToast().warning('network unavailable')
      }
    },
  },
};
</script>
