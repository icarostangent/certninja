<template>
  <div class="col-md-8 mx-auto blog">
    <h1>Blog</h1>
    <div><PostList /></div>
  </div>
</template>

<script>
import PostList from '@/components/PostList.vue'

export default {
  name: "Blog",
  components: {
      PostList,
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
