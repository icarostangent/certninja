<template>
  <div class="col-md-8 mx-auto post">
    <div><h1>{{ post.title.rendered }}</h1></div>
    <div v-html="post.content.rendered"></div>
  </div>
</template>

<script>
export default {
  name: "Post",
  computed: {
    post() {
      return this.$store.state.post;
    },
  },
  mounted() {
    this.$store.dispatch("getPost", { id: this.$route.params.id });
  },
};
</script>
