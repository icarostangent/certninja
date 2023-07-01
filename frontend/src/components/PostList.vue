<template>
  <div class="posts">
    <!-- <i class="fas fa-check"></i>
    <i class="fas fa-asterisk"></i>
    <i class="fas fa-exclamation"></i>
    <i class="fas fa-times"></i>
    <i class="fas fa-power-off"></i>
    <i class="fas fa-hashtag"></i>
    <i class="fas fa-trash"></i> -->

    <ul v-for="post in posts.items" :key="post.id" class="list-group">
      <li class="list-group-item pointer"
        @click.prevent="onClickShowDetail(post.id)">
        <div class="d-flex justify-content-between align-items-start">
          <div class="ms-2 me-auto">
            <div>
              <div class="fw-bold">{{ post.title.rendered }}</div>
              {{ post.post_excerpt }}
            </div>
          </div>
        </div>
      </li>
    </ul>

    <Pagination @page-changed="pageChanged" :totalPages="posts.totalPages" :currentPage="currentPage" />
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";

export default {
  name: "PostList",
  components: {
    Pagination,
  },
  data() {
    return {
      currentPage: 1,
    };
  },
  computed: {
    posts() {
      return this.$store.state.posts;
    },
  },
  mounted() {
    this.$store.dispatch("getPosts", { page: this.currentPage });
  },
  beforeUnmount() {
  },
  methods: {
    pageChanged(page) {
      this.currentPage = page;
      this.$store.dispatch("getPosts", { page: this.currentPage });
    },
    onClickShowDetail(id) {
      this.$router.push({ name: "post", params: { id: id } });
    },
  },
};
</script>

<style scope>
.pointer {
  cursor: pointer;
}

.error {
  background-color: red;
}

.pending {
  background-color: yellow;
}

.success {
  background-color: green;
}
</style>
