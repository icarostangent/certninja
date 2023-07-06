<template>
  <div class="col-md-8 mx-auto post">
    <div>
      <h1>{{ post.title.rendered }}</h1>
    </div>
    <div v-html="post.content.rendered"></div>
    <div class="disqus">
      <Disqus shortname='icaroslabs-com' />
    </div>
  </div>
</template>

<script>
import { Disqus } from 'vue-disqus'

export default {
  name: "Post",
  components: {
    Disqus
  },
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
