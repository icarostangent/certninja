<template>
    <!-- Content -->
    <div class="container">
        <div class="row mb-3">
            <h1 class="mb-3"><router-link class="plain" to="/domains/">Emails</router-link> / Create</h1>
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
import { useToast } from 'vue-toastification'

export default {
    name: 'EmailCreate',
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
            // const domainPattern = new RegExp(/^((http|https):\/\/)?([a-zA-Z0-9_][-_a-zA-Z0-9]{0,62}\.)+([a-zA-Z0-9]{1,10})$/igm)
            const ipPattern = new RegExp(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/)

            if (!domainPattern.test(this.domain)) {
                useToast().warning('Invalid domain')
                return
            }
            if (this.ip && !ipPattern.test(this.ip)) {
                useToast().warning('Invalid IP')
                return
            }
            if (this.port && !parseInt(this.port)) {
                useToast().warning('Invalid port')
                return
            }
            if (parseInt(this.port) <= 0 || parseInt(this.port) > 65535) {
                useToast().warning('Invalid port')
                return
            }
            this.$store.dispatch('createDomain', { 'name': this.domain, 'ip_address': this.ip, 'port': this.port })
                .then(() => {
                    useToast().success('Success')
                    this.$router.push({ 'name': 'domains' })
                })
                .catch((e) => {
                    useToast().error(e.response.data.detail)
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