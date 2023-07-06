<template>
  <div class="col-md-8 mx-auto page">
    <RandomSnippet />
    <div>
      <h1>{{ this.page.title.rendered }}</h1>
    </div>
    <div v-html="page.content.rendered"></div>
    <div class="disqus">
      <Disqus shortname='icaroslabs-com' />
    </div>
  </div>
</template>

<script>
import { Disqus } from 'vue-disqus'
import RandomSnippet from '@/components/RandomSnippet.vue'

export default {
  name: "Page",
  components: {
    Disqus,
      RandomSnippet,
  },
  computed: {
    page() {
      return this.$store.state.page[0];
    },
  },
  mounted() {
    console.log(this.page);
    this.$store.dispatch("getPage", { slug: this.$route.params.slug });
  },
};
</script>
