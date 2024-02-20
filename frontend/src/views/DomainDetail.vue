<template>
  <div class="col-md-8 mx-auto domain">
    <i class="fas fa-check"></i>
    <i class="fas fa-asterisk"></i>
    <i class="fas fa-exclamation"></i>
    <i class="fas fa-times"></i>
    <i class="fas fa-power-off"></i>
    <i class="fas fa-hashtag"></i>
    <i class="fas fa-trash"></i>
    <i class="fas fa-plus"></i>

    <h1>{{ domain.name }}</h1>
    <div class="row">
      <div class="col-md-8 d-flex justify-content-end flex-fill">
        <div class="dropdown">
          <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1"
            data-bs-toggle="dropdown" aria-expanded="false">
            <i class="fa fa-cog"></i>
          </button>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            <li><a @click.prevent="scanNow" class="dropdown-item" href="#">Scan Now</a></li>
            <li><a @click.prevent="assignAgent" class="dropdown-item" href="#">Assign Agent</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a @click.prevent="deleteItem" class="dropdown-item" href="#">Delete</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-4">
        <div v-if="certificateStatus() === 'success'">
          <i class="fa fa-check fa-6x fa-fw"></i>
        </div>
        <div v-if="certificateStatus() === 'pending'">
          <i class="fa fa-spinner fa-pulse fa-6x fa-fw"></i>
        </div>
        <div v-if="certificateStatus() === 'error'">
          <i class="fa fa-exclamation fa-6x fa-fw"></i>
        </div>
      </div>
      <div class="col-md-4 flex-fill">
        <div class="domain">
          <p>{{ domain.ip_address }} {{ domain.port }}</p>
          <p>Created: {{ domain.created }}</p>
          <p>Activity: {{ domain.modified }}</p>
          <p>Agent: {{ domain.agents }}</p>
        </div>
      </div>
    </div>
    <ScanList :scans="scans" @page-changed="pageChanged" />
  </div>
</template>

<script>
import ScanList from "@/components/ScanList";
import { useToast } from 'vue-toastification'

export default {
  name: "DomainDetail",
  components: {
    ScanList,
  },
  computed: {
    domain() {
      return this.$store.state.domain;
    },
    scans() {
      return this.$store.state.scans;
    },
  },
  data() {
    return {
      currentPage: 1,
      domainId: this.$route.params.id,
    }
  },
  methods: {
    pageChanged(page) {
      this.currentPage = page;
      this.$store.dispatch("getScans", { domainId: this.domainId, page: this.currentPage });
    },
    certificateStatus() {
      if (!this.domain.last_scan) return "pending";
      if (JSON.parse(this.domain.last_scan)["error"]) return "error";
      return "success";
    },
    deleteItem() {
      if (confirm("are you sure?")) {
        try {
          this.$store.dispatch("deleteDomain", this.domain.id);
          useToast().success("domain successfully deleted");
          this.$router.push({ name: "domains" });
        } catch (error) {
          useToast().error("error deleting domain");
        }
      }
    },
  },
  mounted() {
    try {
      this.$store.dispatch("getDomain", { domainId: this.domainId });
    } catch (error) {
      console.log("error getting domain");
      this.$router.push({ name: "domains" });
    }
    try {
      this.$store.dispatch("getScans", { domainId: this.domainId, page: this.currentPage });
    } catch (error) {
      console.log("error getting scans");
    }
    try {
      this.$store.dispatch("getAgents", {})
    } catch (error) {
      console.log("error getting agents");
    }
  },
};
</script>

<style scope>
.scans {
  cursor: pointer;
}
</style>
