<template>
    <ul class="pagination">
        <li class="pagination-item">
            <button @click="onClickFirstPage" class="btn btn-primary btn-sm" :class="isInFirstPage? 'disabled':''" :disabled="isInFirstPage">First</button>
        </li>
        <li class="pagination-item">
            <a href="#" @click.prevent="onClickPreviousPage" :class="isInFirstPage? 'disabled':''" :disabled="isInFirstPage"><i class="fas fa-angle-double-left"></i></a>
        </li>
        <li :key="page.id" v-for="page in pages" class="pagination-item">
            <a href="#" @click.prevent="onClickPage(page.name)" :disabled="page.isDisabled" :class="{ active: isPageActive(page.name) }">{{ page.name }}</a>
        </li>
        <li class="pagination-item">
            <a href="#" @click.prevent="onClickNextPage" :class="isInLastPage? 'disabled':''" :disabled="isInLastPage"><i class="fas fa-angle-double-right"></i></a>
        </li>
        <li class="pagination-item">
            <button @click="onClickLastPage" class="btn btn-primary btn-sm" :class="isInLastPage? 'disabled':''" :disabled="isInLastPage">Last</button>
        </li>
    </ul>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    maxVisibleButtons: {
      type: Number,
      required: false,
      default: 3
    },
    totalPages: {
      type: Number,
      required: true
    },
    perPage: {
      type: Number,
      required: false, 
      default: 10
    },
    currentPage: {
      type: Number,
      required: true
    }
  },
  computed: {
    isInFirstPage () {
      return this.currentPage === 1
    },
    isInLastPage () {
      if (this.totalPages === 0) {
        return true
      }
      return this.currentPage === this.totalPages
    },
    startPage () {
      // When on the first page
      if (this.currentPage === 1) {
        return 1
      }
      // When on the last page
      if (this.totalPages < this.maxVisibleButtons) {
        return 1
      }
      if (this.currentPage === this.totalPages) {
        return this.totalPages - this.maxVisibleButtons + 1
      }
      // When in between
      return this.currentPage - 1
    },
    endPage () {
      if (this.totalPages === 0) {
        return 1
      }
      if (this.totalPages < this.maxVisibleButtons) {
        return this.totalPages
      }
      return Math.min(this.startPage + this.maxVisibleButtons - 1, this.totalPages)
    },
    pages () {
      const range = []
      for (let i = this.startPage; i <= this.endPage; i++) {
        range.push({
          name: i,
          isDisabled: i === this.currentPage
        })
      }
      return range
    }
  },
  methods: {
    onClickFirstPage () {
      if (this.isInFirstPage) {
        return false
      }
      this.$emit('page-changed', 1)
    },
    onClickPreviousPage () {
      if (this.isInFirstPage) {
        return false
      }
      this.$emit('page-changed', this.currentPage - 1)
    },
    onClickPage (page) {
      this.$emit('page-changed', page)
    },
    onClickNextPage () {
      if (this.isInLastPage) {
        return false
      }
      this.$emit('page-changed', this.currentPage + 1)
    },
    onClickLastPage () {
      if (this.isInLastPage) {
        return false
      }
      this.$emit('page-changed', this.totalPages)
    },
    isPageActive (page) {
      return this.currentPage === page
    }
  },
  mounted() {
  },
}
</script>
<style scoped>
  .pagination {
    list-style-type: none;
    float: right;
    margin: 10px 0;
    .pagination-item {
      display: inline-block;
      color: #ddd;
      a {
        text-decoration: none;
        margin: 5px;
        color: #2c3e50;
      }
      a.disabled {
        color: #ccc;
        cursor: no-drop;
      }
      .active {
        background-color: tomato;
        color: #ffffff !important;
        font-weight: bold;
        padding: 3px 8px;
      }
    }
  }
  button[disabled], html input[disabled] {
    cursor: default;
    color: lightgray;
  }
</style>
