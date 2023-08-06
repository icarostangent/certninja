<template>
  <div class="scans">
    <div class="col">
      <div v-show="scans.items === []">
        <h5>No scan data</h5>
      </div>
      <div v-for="item in scans.items" :key="item.id" class="accordion" id="accordionCerts">
        <div class="accordion-item">
          <h1 class="accordion-header" :id="`heading-${item.id}`">
            <button class="accordion-button" type="button" data-bs-toggle="collapse"
              :data-bs-target="`#collapse-${item.id}`" aria-expanded="false" :aria-controls="`collapse-${item.id}`">
              <div class="fw-bold">{{ item.uuid }}</div>
            </button>
          </h1>
          <div :id="`collapse-${item.id}`" class="accordion-collapse collapse" :aria-labelledby="`heading-${item.id}`"
            data-bs-parent="#accordionCerts">
            <div class="accordion-body">
              <div class="ms-3 me-auto">
                <div v-if="JSON.parse(item.output)['error'] === undefined">
                  <br />
                  <h5>Cipher: {{ JSON.parse(item.output)['cipher'] }}</h5>
                  <h5>Subject:</h5>
                  <ul v-for="(field, index) in JSON.parse(item.output)['certificate'][
                    'subject'
                  ]" :key="index">
                    <li>{{ field[0][0] }}: {{ field[0][1] }}</li>
                  </ul>
                  <h5>Issuer:</h5>
                  <ul v-for="(field, index) in JSON.parse(item.output)['certificate'][
                    'issuer'
                  ]" :key="index">
                    <li>{{ field[0][0] }}: {{ field[0][1] }}</li>
                  </ul>
                  <h5>
                    Version: {{ JSON.parse(item.output)['certificate']["version"] }}
                  </h5>
                  <h5>
                    Serial No:
                    {{ JSON.parse(item.output)['certificate']["serialNumber"] }}
                  </h5>
                  <h5>
                    Not Before: {{ JSON.parse(item.output)['certificate']["notBefore"] }}
                  </h5>
                  <h5>
                    Not After: {{ JSON.parse(item.output)['certificate']["notAfter"] }}
                  </h5>
                  <h5>Alt Names:</h5>
                  <ul v-for="(field, index) in JSON.parse(item.output)['certificate'][
                    'subjectAltName'
                  ]" :key="index">
                    <li>{{ field[0] }}: {{ field[1] }}</li>
                  </ul>
                  <h5>
                    CA Issuer:
                    {{ JSON.parse(item.output)['certificate']["caIssuers"][0] }}
                  </h5>
                  <h5>CRL Distribution Points:</h5>
                  <ul v-for="(field, index) in JSON.parse(item.output)['certificate'][
                    'crlDistributionPoints'
                  ]" :key="index">
                    <li>{{ field }}</li>
                  </ul>
                </div>
                <div v-else class="ms-3 me-auto">
                  <br />
                  <h5>Error: {{ JSON.parse(item.output)["error"] }}</h5>
                  <p>Ex: {{ JSON.parse(item.output)["ex"] }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Pagination @page-changed="pageChanged" :totalPages="scans.totalPages" :currentPage="currentPage" />
    </div>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination.vue";

export default {
  name: "ScanList",
  props: {
    scans: Object,
  },
  components: {
    Pagination,
  },
  data() {
    return {
      currentPage: 1,
    }
  },
  methods: {
    pageChanged(page) {
      this.currentPage = page;
      this.$emit("page-changed", this.currentPage)
    },
  },
};
</script>

<style scoped>
</style>