<template>
  <a
    class="nav-link dropdown-toggle"
    href="#"
    role="button"
    id="dropdownMenuLink"
    data-bs-toggle="dropdown"
    data-bs-auto-close="outside"
    aria-expanded="false"
  >
    {{ this.title }}
  </a>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
    <template v-for="item in menuItems" :key="item.ID">
      <template v-if="item.child_items !== undefined">
        <li class="dropend">
          <Menu :title="item.title" :menuItems="item.child_items" />
        </li>
      </template>
      <template v-else-if="item.object === 'page' || item.object === 'post'">
        <li class="nav-item">
          <router-link :to="makePath(item)" class="dropdown-item">
            {{ item.title }}
          </router-link>
        </li>
      </template>
    </template>
  </ul>
</template>

<script>
import Menu from "@/components/Menu.vue";

export default {
  name: "Menu",
  props: {
    title: String,
    menuItems: Array,
  },
  components: {
    Menu,
  },
  methods: {
    makeId(item) {
      return `navbarDropdownDynamic-${item.ID}`;
    },
    makePath(item) {
      return `/${item.object}/${item.slug}`;
    },
  },
  mounted() {
    console.log(this.title);
  },
};
</script>

<style scoped>
</style>