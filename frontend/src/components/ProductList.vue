<template>
  <div class="products">

    <div class="card-group">
        <div v-for="product in products.items">
          <div class="card mb-4 rounded-3 shadow-sm">
            <div class="card-header py-3">
              <h4 class="my-0 fw-normal">{{ product.name }}</h4>
            </div>
            <div class="card-body">
              <h1 class="card-title pricing-card-title">${{ product.amount }}<small
                  class="text-muted fw-light">/mo</small></h1>
              <div v-html="product.description"></div>
              <button @click.prevent="submit(product.name)" type="button"
                class="w-100 btn btn-lg btn-outline-primary">Subscribe
                now on Stripe</button>
            </div>

          </div>
        </div>
    </div>

    <Pagination @page-changed="pageChanged" :totalPages="products.totalPages" :currentPage="currentPage" />
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";

export default {
  name: "ProductList",
  components: {
    Pagination,
  },
  data() {
    return {
      currentPage: 1,
      now: new Date(),
      interval: null,
    };
  },
  computed: {
    products() {
      return this.$store.state.products;
    },
  },
  mounted() {
    this.$store.dispatch("getProducts", { page: this.currentPage });
  },
  beforeUnmount() {
  },
  methods: {
    submit(product) {
      this.$router.push({ 'name': 'checkout', 'params': { 'plan': product.toLowerCase() } })
    },
    pageChanged(page) {
      this.currentPage = page;
      this.$store.dispatch("getProducts", { page: this.currentPage });
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
