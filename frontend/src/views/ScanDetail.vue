<template>
  <h1>Common Name:</h1>
  {{ scan.common_name }}<br />
  <h3>Alt Names:</h3>
  <ul class="list-group">
    <li v-for="item in scan.alt_names.split(', ')" :key="item.id" class="list-group-item">{{ item }}</li>
  </ul>
  <h3>Issuer:</h3>
  {{ scan.issuer }}<br />
  <h3>Not After:</h3>
  {{ scan.not_after }}<br />
  <h3>Not Before:</h3>
  {{ scan.not_before }}<br />
  <h3>SerialNumber:</h3>
  {{ scan.serial_number }}<br />
  <h3>Signature Algorithm:</h3>
  {{ scan.signature_algorithm }}<br />
</template>
<script>
export default {
  name: "ScanDetail",
  computed: {
    scan() {
      return this.$store.state.scan
    },
  },
  data() {
    return {
      scanId: this.$route.params.scan_id,
    }
  },
  methods: {},
  mounted() {
    this.$store.dispatch('getScan', { domainId: this.domainId, scanId: this.scanId })
  },
}
</script>
<style></style>