<template>
  <div class="row">
    <div class="domain-details-top col-md-8 d-flex justify-content-end flex-fill">
      <div class="dropdown">
        <button
          class="btn btn-secondary dropdown-toggle"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <i class="fa fa-cog"></i>
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
          <li>
            <a @click.prevent="deleteItem" class="dropdown-item" href="#"
              >Delete</a
            >
          </li>
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
        <h3>{{ domain.post_title }}</h3>
        <p>{{ domain.post_excerpt }}</p>
        <p>Created: {{ domain.post_date }}</p>
        <p>Activity: {{ domain.post_modified }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
  name: "DomainItem",
  props: {
    domain: Object,
  },
  components: {},
  methods: {
    certificateStatus() {
      console.log(typeof this.domain.post_content, this.domain.post_content);
      if (!this.domain.post_content) return "pending";
      if (JSON.parse(this.domain.post_content)["error"]) return "error";
      return "success";
    },
    deleteItem() {
      if (confirm("are you sure?")) {
        try {
          this.$store.dispatch("deleteDomain", this.domain.ID);
          useToast().success("domain successfully deleted");
          this.$router.push({ name: "domains" });
        } catch (error) {
          useToast().error("error deleting domain");
        }
      }
    },
  },
};
</script>

<style scope>
.scans {
  cursor: pointer;
}
</style>
