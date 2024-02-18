<template>
  <h1 class="text-center mb-3">Welcome to CertNinja</h1>
  <h4 class="text-center mb-4">Badass</h4>
  <AnoymousScan />
  <div class="col mx-auto page">
    <div>
      <h1>{{ this.page.title.rendered }}</h1>
    </div>
    <div v-html="page.content.rendered"></div>
  </div>
</template>

<script>
import AnoymousScan from "@/components/AnonymousScan"

export default {
  name: "Home",
  components: {
    AnoymousScan,
  },
  computed: {
    page() {
      return this.$store.state.page[0];
    },
  },
  mounted() {
    console.log(this.page);
    this.$store.dispatch("getPage", { slug: 'home' });
  },
};
</script>
