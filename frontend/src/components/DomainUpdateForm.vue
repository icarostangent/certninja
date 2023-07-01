<template>
  <div id="update-domain">
    <form class="input-group mb-3">
      <div class="form-control">
        <input
          class="form-control"
          type="text"
          v-model="this.form.domain"
          name="domain"
          placeholder="Domain..."
        />
        <input
          class="form-control"
          type="text"
          v-model="this.form.ip"
          name="ip"
          placeholder="(Optional) IP Address..."
        />
        <input
          @click.prevent="submitForm"
          value="submit"
          class="btn btn-block"
        />
        <input
          @click.prevent="cancelForm"
          value="cancel"
          class="btn btn-block"
        />
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: "DomainUpdateForm",
  data() {
    return {
      form: {
        domain: this.domain.post_title,
        ip: this.domain.post_excerpt,
      },
    };
  },
  props: {
    domain: Object,
  },
  methods: {
    submitForm() {
      const domainPattern = new RegExp(
        /^((http|https):\/\/)?([a-zA-Z0-9_][-_a-zA-Z0-9]{0,62}\.)+([a-zA-Z0-9]{1,10})$/gim
      );
      const ipPattern = new RegExp(
        /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
      );

      const ip = this.form.ip ? this.form.ip.split(":")[0] : '';
      const port = this.form.ip ? this.form.ip.split(":")[1] : '';

      console.log(ip)
      console.log(port)

      if (!domainPattern.test(this.form.domain)) {
        console.log("invalid domain");
        return;
      }

      if (ip && !ipPattern.test(ip)) {
        console.log("invalid ip");
        return;
      }

      if (port && port <= 0 || port > 65535) {
        consele.log("invalid port");
        return;
      }

      this.form.domainId = this.domain.ID;
      this.$store.dispatch("updateDomain", this.form);
      this.form.domain = "";
      this.form.ip = "";
    },
    cancelForm() {
      this.$emit("hide-form", true);
    },
  },
};
</script>
