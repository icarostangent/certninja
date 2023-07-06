<template>
  <div class="col-md-8 mx-auto about">
    <RandomSnippet />
    <h1>This is an about page</h1>
  </div>
</template>

<script>
import RandomSnippet from '@/components/RandomSnippet.vue'

export default {
  name: "About",
  components: {
      RandomSnippet,
  },
};
</script>