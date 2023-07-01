<template>
  <div v-if="listItem">
      world
    <div v-if="status === 'success'">
      <i class="fa fa-check fa-2x fa-fw"></i>
    </div>
    <div v-if="status === 'pending'">
      <i class="fa fa-spinner fa-pulse fa-2x fa-fw"></i>
    </div>
    <div v-if="status === 'error'">
      <i class="fa fa-exclamation fa-2x fa-fw"></i>
    </div>
  </div>
  <div v-else>
      hello
    <div v-if="status === 'success'">
      <i class="fa fa-check fa-4x fa-fw"></i>
    </div>
    <div v-if="status === 'pending'">
      <i class="fa fa-spinner fa-pulse fa-4x fa-fw"></i>
    </div>
    <div v-if="status === 'error'">
      <i class="fa fa-exclamation fa-4x fa-fw"></i>
    </div>
  </div>
</template>

<script>
export default {
  name: "StatusBadge",
  props: {
    status: {
        type: String,
        required: true
    },
    listItem: {
        type: Boolean,
        default: false,
    },
  },
};
</script>

<style scoped>
</style>