<template>
    <!-- Content -->
    <div class="container">
        <div class="row mb-3">
            <h1 class="mb-3"><router-link class="plain" to="/domains/">Domains</router-link> / Create</h1>
            <div class="col-md-12">
                <div class="form-outline">
                    <label for="validationDomain" class="form-label">Domain Name</label>
                    <input v-model="domain" type="text" class="form-control" id="validationDomain" required />
                    <div class="invalid-feedback">Invalid Domain</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-outline">
                    <label for="validationIPAddress" class="form-label">IP Address (Optional)</label>
                    <input v-model="ip" type="text" class="form-control" id="validationIPAddress" required />
                    <div class="invalid-feedback">Invalid IP Address</div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="form-outline">
                    <label for="validationPort" class="form-label">Port (Optional)</label>
                    <input v-model="port" type="text" class="form-control" id="validationPort" required />
                    <div class="invalid-feedback">Invalid Port</div>
                </div>
            </div>
        </div>
        <a @click.prevent="onClickCreate" class="btn btn-primary mb-5" href="">Track Domain</a>
    </div>
</template>

<script>
export default {
    name: 'DomainCreate',
    data() {
        return {
            domain: '',
            ip: null,
            port: 443,
        }
    },
    methods: {
        onClickCreate() {
            const domainPattern = new RegExp('^(?=.{1,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\\.)+[a-zA-Z]{2,}$)')
            const ipPattern = new RegExp(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/)

            if (!domainPattern.test(this.domain)) {
                this.$store.commit("SET_MESSAGE", { title: "Error", text: "Invalid Domain Name", display: true, style: "bg-warning" })
                return
            }
            if (this.ip && !ipPattern.test(this.ip)) {
                this.$store.commit("SET_MESSAGE", { title: "Error", text: "Invalid IP Address", display: true, style: "bg-warning" })
                return
            }
            if (this.port && !parseInt(this.port)) {
                this.$store.commit("SET_MESSAGE", { title: "Error", text: "Invalid Port", display: true, style: "bg-warning" })
                return
            }
            if (parseInt(this.port) <= 0 || parseInt(this.port) > 65535) {
                this.$store.commit("SET_MESSAGE", { title: "Error", text: "Invalid Port", display: true, style: "bg-warning" })
                return
            }
            this.$store.dispatch('createDomain', { 'name': this.domain, 'ip_address': this.ip, 'port': this.port })
                .then(() => {
                    this.$store.commit("SET_MESSAGE", { title: "Success", text: "Domain created successfully", display: true, style: "bg-success" })
                    this.$router.push({ 'name': 'domains' })
                })
                .catch((e) => {
                    if (e.response.data.detail === "Domain limit exceeded for subscription.") {
                        this.$store.commit("SET_MESSAGE", { title: "Error", text: `Domain limit exceeded.`, display: true, style: "bg-warning", path: "/account" })
                    } else {
                        this.$store.commit("SET_MESSAGE", { title: "Error", text: e.response.data, display: true, style: "bg-danger" })
                    }
                })

        }
    },
}
</script>

<style>
.plain {
    text-decoration: none;
    color: black;
}
</style>