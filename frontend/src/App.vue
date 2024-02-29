<template>
  <link rel="stylesheet" :href="theme" />
  <Nav />
  <Message />
  <div ref="top" class="padding-top">
    <router-view :key="$route.path" />
  </div>
  <Footer />
</template>

<script>
import Footer from "@/components/Footer.vue";
import Message from "@/components/Message.vue";
import Nav from "@/components/Nav.vue";

export default {
  components: {
    Footer,
    Message,
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
