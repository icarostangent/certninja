<template>
  <div class="emails">
    <div v-for="email in emails.items">
      <p>
        email: {{ email.email }}<br />
        verified: {{ email.verified }}<br />
        verification sent: {{ email.verification_sent }}<br />
        reset key sent: {{ email.reset_sent }}<br />
      </p>
    </div>
    <Pagination @page-changed="pageChanged" :totalPages="emails.totalPages" :currentPage="currentPage" />
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";

export default {
  name: "EmailList",
  components: {
    Pagination,
  },
  data() {
    return {
      currentPage: 1,
      now: new Date(),
      interval: null,
    };
  },
  computed: {
    emails() {
      return this.$store.state.emails;
    },
  },
  mounted() {
    this.$store.dispatch("getEmails", { page: this.currentPage })
  },
  methods: {
    pageChanged(page) {
      this.currentPage = page;
      this.$store.dispatch("getEmails", { page: this.currentPage });
    },
  },
};
</script>

<style scope>
.pointer {
  cursor: pointer;
}

.error {
  background-color: red;
}

.pending {
  background-color: yellow;
}

.success {
  background-color: green;
}
</style>
