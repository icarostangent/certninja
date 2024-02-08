<template>
  <div class="agents">
    <div v-for="agent in agents.items">
      <p>
        name: {{ agent.name }}<br />
        api key: {{ agent.api_key }}<br />
        last seen: {{ agent.last_seen }}
      </p>
    </div>
    <Pagination @page-changed="pageChanged" :totalPages="agents.totalPages" :currentPage="currentPage" />
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";

export default {
  name: "AgentList",
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
    agents() {
      return this.$store.state.agents;
    },
  },
  mounted() {
      this.$store.dispatch("getAgents", { page: this.currentPage });
  },
  methods: {
    pageChanged(page) {
      this.currentPage = page;
    },
  },
};
</script>
