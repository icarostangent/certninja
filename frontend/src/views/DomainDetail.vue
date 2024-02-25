<template>
  <div class="container">
    <div class="row mb-5">
      <div class="col">
        <h1 class="mb-3"><router-link class="plain" to="/domains/">Domains / </router-link>{{ domain.name }}</h1>

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

        <h3>Certificates</h3>
        <div class="table-responsive mb-3">
          <table class="table table-lg">
            <thead>
              <th>Common Name</th>
              <th>Issuer</th>
              <th>First Seen</th>
              <th>Valid From</th>
              <th>Valid To</th>
              <th></th>
            </thead>
            <tbody>
              <tr v-for="item in scans.items" :key="item.id" @click.prevent="showScan(item.id)" class="scan-item">
                <td>{{ item.common_name }}</td>
                <td>{{ item.issuer }}</td>
                <td>{{ new Date(item.created).toLocaleString() }}</td>
                <td>{{ new Date(item.not_before).toLocaleString() }}</td>
                <td>{{ new Date(item.not_after).toLocaleString() }}</td>
                <td><a class="btn btn-secondary rounded-pill">Show</a></td>
              </tr>
            </tbody>
          </table>
          <Pagination @page-changed="pageChangedScans" :totalPages="scans.totalPages" :currentPage="currentPageScans" />
        </div>
        <a @click.prevent="scanNow" class="btn btn-primary mb-5">Scan Now</a>

        <h3>Email Targets</h3>
        <div class="table-responsive mb-3">
          <table class="table table-md mb-3">
            <thead>
              <th>Email Address</th>
              <th class="text-end"></th>
            </thead>
            <tbody>
              <tr v-for="item in emails.items" :key="item.id" @click.prevent="showScan(item.id)" class="email-item">
              </tr>
            </tbody>
          </table>
          <Pagination @page-changed="pageChangedEmails" :totalPages="emails.totalPages"
            :currentPage="currentPageEmails" />
        </div>
        <router-link class="btn btn-primary mb-5" to="/emails/create/">Add Email</router-link>
      </div>
    </div>
    <div class="row text-center mb-5">
      <div class="col">
        <a @click.prevent="deleteItem" class="btn btn-danger mb-5">Delete</a>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from 'vue-toastification'
import Pagination from "@/components/Pagination";

export default {
  name: "DomainDetail",
  components: {
    Pagination,
  },
  computed: {
    domain() {
      return this.$store.state.domain;
    },
    scans() {
      return this.$store.state.scans;
    },
    emails() {
      return this.$store.state.emails;
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
    deleteItem() {
      if (confirm("are you sure?")) {
        try {
          this.$store.dispatch("deleteDomain", this.domain.id);
          useToast().success("domain successfully deleted");
          clearInterval(this.interval)
          this.$router.push({ name: "domains" });
        } catch (error) {
          useToast().error("error deleting domain");
        }
      }
    },
    scanNow() {
      this.$store.dispatch("scanNow", { domainId: this.domainId })
    },
    createEmail() {
      this.$store.dispatch("createEmail", { domainId: this.domainId })
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
.scan-item {
  cursor: pointer;
}

.plain {
  text-decoration: none;
  color: black;
}
</style>
