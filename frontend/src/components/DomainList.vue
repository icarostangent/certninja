<template>
  <div class="domains">
    <!-- <i class="fas fa-check"></i>
    <i class="fas fa-asterisk"></i>
    <i class="fas fa-exclamation"></i>
    <i class="fas fa-times"></i>
    <i class="fas fa-power-off"></i>
    <i class="fas fa-hashtag"></i>
    <i class="fas fa-trash"></i> -->

    <ul v-for="domain in domains.items" :key="domain.id" class="list-group">
      <li class="list-group-item pointer" :class="certificateStatus(domain.last_scan)"
        @click.prevent="onClickShowDetail(domain.id)">
        <div class="d-flex justify-content-between align-items-start">
          <div class="ms-2 me-auto">
            <div>
              <div class="fw-bold">{{ domain.name }}</div>
              <div v-if="domain.ip_address || domain.port">{{ domain.ip_address }}:{{ domain.port }}</div>
            </div>
            <div v-if="!domain.last_scan">no scan found</div>
            <div v-else>
              <div v-if="certificateStatus(domain.last_scan) === 'error'">
                Error: {{ JSON.parse(domain.last_scan)["error"] }}
              </div>
              <div v-else>
                Not After:
                {{
                  new Date(
                    JSON.parse(domain.last_scan)['certificate']['notAfter']
                  ).toUTCString()
                }}<br />
              </div>
            </div>
          </div>
          <div v-if="certificateStatus(domain.last_scan) === 'success'">
            <i class="fa fa-check fa-2x fa-fw"></i>
          </div>
          <div v-if="certificateStatus(domain.last_scan) === 'pending'">
            <i class="fa fa-spinner fa-pulse fa-2x fa-fw"></i>
          </div>
          <div v-if="certificateStatus(domain.last_scan) === 'error'">
            <i class="fa fa-exclamation fa-2x fa-fw"></i>
          </div>
        </div>
      </li>
    </ul>

    <Pagination @page-changed="pageChanged" :totalPages="domains.totalPages" :currentPage="currentPage" />
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";

export default {
  name: "DomainList",
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
    domains() {
      return this.$store.state.domains;
    },
  },
  mounted() {
    this.$store.dispatch("getDomains", { page: this.currentPage })
      .then(() => {
        this.interval = setInterval(() => {
          this.domains.items.forEach((item) => {
            if (!item.last_scan) {
              this.$store.dispatch("pollDomain", { domainId: item.id })
                .then((domain) => {
                  if (domain.last_scan !== "") {
                    this.domains.items = this.domains.items.map((item) => {
                      if (item.id === domain.id) {
                        return domain;
                      }
                      return item;
                    });
                  }
                });
            }
          });
        }, 2000);
      });
  },
  beforeUnmount() {
    this.interval = null;
  },
  methods: {
    // TODO: parse properly
    certificateStatus(scan) {
      if (!scan) return "pending";
      if (JSON.parse(scan)["error"]) return "error";
      return "success";
    },
    pageChanged(page) {
      this.currentPage = page;
      this.$store.dispatch("getDomains", { page: this.currentPage });
    },
    onClickShowDetail(domainId) {
      this.$router.push({ name: "domain", params: { id: domainId } });
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
