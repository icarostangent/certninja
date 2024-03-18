<template>
  <div class="col-md-8 mx-auto thanks">
    <h1>This is a thanks page</h1>
    <p>Please check your email</p>
  </div>
</template>

<script>
export default {
  name: "Thanks",
  mounted() {
    this.$store.commit("SET_MESSAGE", { title: "Success", text: "Email is not plugged in. Proceed to login.", display: true, style: "bg-success" })
  },
}
</script>