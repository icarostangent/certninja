<template>
  <div class="col-md-8 mx-auto domain">
    <h1>Domain Details</h1>
    <DomainItem :domain="domain" />
    <ScanList :scans="scans" @page-changed="pageChanged" />
  </div>
</template>

<script>
import DomainItem from "@/components/DomainItem";
import ScanList from "@/components/ScanList";

export default {
  name: "DomainDetail",
  components: {
    DomainItem,
    ScanList,
  },
  computed: {
    domain() {
      return this.$store.state.domain;
    },
    scans() {
      return this.$store.state.scans;
    },
  },
  data() {
    return {
      currentPage: 1,
      domainId: this.$route.params.id,
    }
  },
  methods: {
    pageChanged(page) {
      this.currentPage = page;
      this.$store.dispatch("getScans", { domainId: this.domainId, page: this.currentPage });
    },
  },
  mounted() {
    try {
      this.$store.dispatch("getDomain", { domainId: this.domainId });
    } catch (error) {
      console.log("error getting domain");
      this.$router.push({ name: "domains" });
    }
    try {
      this.$store.dispatch("getScans", { domainId: this.domainId, page: this.currentPage });
    } catch (error) {
      console.log("error getting scans");
    }
    try {
      this.$store.dispatch("getAgents", {})
    } catch (error) {
      console.log("error getting agents");
    }
  },
};
</script>
