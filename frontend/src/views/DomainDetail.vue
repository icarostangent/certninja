<template>
  <div class="container">
    <div class="row mb-5">
      <div class="col">
        <h1 class="mb-3">{{ domain.name }}</h1>

        <div class="row mb-5">
          <div class="col-md">
            <div class="mb-3">
              <i v-if="domain.scan_status !== 'complete'" class="fa fa-spinner fa-pulse fa-5x"></i>
              <i v-else-if="domain.last_scan_error" class="fas fa-exclamation fa-5x"></i>
              <i v-else class="fas fa-check fa-5x"></i><br />
            </div>
            <span class="mt-3">Status: {{ domain.last_scan_error }}</span>
          </div>

          <div class="col-md">
            <span>Domain: {{ domain.name }} </span><br />
            <span>IP: {{ domain.ip }}</span><br />
            <span>Port: {{ domain.port }} </span><br />
            <span>Activity: {{ new Date(domain.modified).toLocaleString() }}</span>
          </div>
        </div>

        <div class="row mb-5">
          <div class="col-md">
            <h3>Certificates</h3>
            <div class="table-responsive mb-3">
              <table class="table">
                <thead>
                  <th>Common Name</th>
                  <th>Issuer</th>
                  <th>First Seen</th>
                  <th>Valid From</th>
                  <th>Valid To</th>
                  <th></th>
                </thead>
                <tbody>
                  <tr v-for="item in scans.items" :key="item.id" @click.prevent="showScan(item.id)" class="click">
                    <td>{{ item.common_name }}</td>
                    <td>{{ item.issuer }}</td>
                    <td>{{ new Date(item.created).toLocaleString() }}</td>
                    <td>{{ new Date(item.not_before).toLocaleString() }}</td>
                    <td>{{ new Date(item.not_after).toLocaleString() }}</td>
                    <td><a class="btn btn-secondary rounded-pill">Show</a></td>
                  </tr>
                </tbody>
              </table>
              <Pagination @page-changed="pageChangedScans" :totalPages="scans.totalPages"
                :currentPage="currentPageScans" />
            </div>
            <a @click.prevent="scanNow" class="btn btn-primary">Scan Now</a>
          </div>
        </div>

        <div class="row mb-5">
          <div class="col-md">
            <h3>Email Targets</h3>
            <div class="table-responsive mb-3">
              <table class="table mb-3">
                <thead>
                  <th>Email Address</th>
                  <th></th>
                </thead>
                <tbody>
                  <tr v-for="item in emails.items" :key="item.id" @click.prevent="showEmail(item.id)" class="click">
                    <td>{{ item.email }}
                    </td>
                    <td><a class="btn btn-secondary rounded-pill">Show</a></td>
                  </tr>
                </tbody>
              </table>
              <Pagination @page-changed="pageChangedEmails" :totalPages="emails.totalPages"
                :currentPage="currentPageEmails" />
            </div>
            <a @click.prevent="createEmail" class="btn btn-primary">Create Email</a>
          </div>
        </div>
      </div>
    </div>
    <div class="row text-center mb-5">
      <div class="col">
        <a @click.prevent="deleteItem" class="btn btn-danger">Delete</a>
      </div>
    </div>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination"

export default {
  name: "DomainDetail",
  components: {
    Pagination,
  },
  computed: {
    domain() {
      return this.$store.state.domain
    },
    scans() {
      return this.$store.state.scans
    },
    emails() {
      return this.$store.state.emails
    },
  },
  data() {
    return {
      currentPageScans: 1,
      currentPageEmails: 1,
      interval: null,
      domainId: this.$route.params.id,
    }
  },
  methods: {
    showScan(scan_id) {
      this.$router.push({ name: 'scan', params: { domain_id: this.domainId, scan_id: scan_id } })
    },
    pollDomain() {
      this.interval = setInterval(() => {
        if (this.domain.scan_status !== 'complete') {
          this.$store.dispatch("pollDomain", { domainId: this.domainId })
            .then((domain) => {
              if (domain.scan_status === "complete") {
                this.$store.commit('SET_DOMAIN', domain)
                this.currentPageScans = 1
                this.$store.dispatch("getScans", { domainId: this.domainId, page: this.currentPageScans })
              }
            })
        }
      }, 2000)
    },
    pageChangedScans(page) {
      this.currentPageScans = page;
      this.$store.dispatch("getScans", { domainId: this.domainId, page: this.currentPageScans });
    },
    pageChangedEmails(page) {
      this.currentPageEmails = page;
      this.$store.dispatch("getEtails", { domainId: this.domainId, page: this.currentPageEmails });
    },
    deleteItem() {
      if (confirm("are you sure?")) {
        try {
          this.$store.dispatch("deleteDomain", this.domain.id);
          this.$store.commit("SET_MESSAGE", { title: "Success", text: "Domain deleted successfully", display: true, style: "bg-success" })
          clearInterval(this.interval)
          this.$router.push({ name: "domains" });
        } catch (error) {
          this.$store.commit("SET_MESSAGE", { title: "Error", text: "Failed to delete domain", display: true, style: "bg-warning" })
        }
      }
    },
    scanNow() {
      this.$store.dispatch("scanNow", { domainId: this.domainId })
    },
    createEmail() {
      this.$router.push({ name: 'email-create', params: { domainId: this.domainId } })
    },
  },
  mounted() {
    this.$store.dispatch("getDomain", { domainId: this.domainId })
    this.$store.dispatch("getScans", { domainId: this.domainId, page: this.currentPageScans })
    this.$store.dispatch("getEmails", { domainId: this.domainId, page: this.currentPageEmails })
    this.pollDomain()
  },
  beforeUnmount() {
    clearInterval(this.interval)
  },
}
</script>

<style scope>
.click {
  cursor: pointer;
}

.plain {
  text-decoration: none;
  color: black;
}
</style>
                                                  