<template>
  <div class="col-md-8 mx-auto blog">
    <RandomSnippet />
    <h1>Blog</h1>
    <div><PostList /></div>
  </div>
</template>

<script>
import PostList from '@/components/PostList.vue'
import RandomSnippet from '@/components/RandomSnippet.vue'

export default {
  name: "Blog",
  components: {
      PostList,
      RandomSnippet,
  },
  computed: {
    posts() {
      return this.$store.state.posts;
    },
  },
  mounted() {
  },
};
</script>
