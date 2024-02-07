<template>
  <link rel="stylesheet" :href="theme" />
  <Nav />
  <div class="padding-top">
    <router-view :key="$route.path" />
  </div>
</template>

<script>
import Nav from "@/components/Nav.vue";

export default {
  components: {
    Nav,
  },
  computed: {
    theme() {
      return this.$store.state.theme;
    },
  },
  mounted() {
    this.$store.dispatch("getTheme");
  },
};
</script>

<style>
.padding-top {
  padding-top: 70px;
}

.scroll {
  overflow: auto;
  height: 100%;
  padding: 0;
}
</style>
