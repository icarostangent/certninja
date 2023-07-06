<template>
  <div class="float-end snippet">
    <h4><code>{{ snippet.code }}</code></h4>
  </div>
</template>

<script>
export default {
  name: "RandomSnippet",
  computed: {
    snippet() {
      return this.$store.state.snippet;
    },
  },
  mounted() {
    this.$store.dispatch("getSnippet").then(console.log(this.snippet));
  },
};
</script>
