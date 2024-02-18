<template>
    <div class="p-5 mb-5 bg-body-tertiary">
        <form class="row g-3 mb-5">
            <div class="col-12">
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
        </form>
        <button @click.prevent="onClickCreate" class="btn btn-primary btn-lg" role="button">Scan Now</button>
    </div>

</template>

<script>
import { useToast } from 'vue-toastification'

export default {
    name: 'AnonymousScan',
    data() {
        return {
            domain: '',
            ip: null,
            port: null,
        }
    },
    methods: {
        onClickCreate() {
            const domainPattern = new RegExp(/^((http|https):\/\/)?([a-zA-Z0-9_][-_a-zA-Z0-9]{0,62}\.)+([a-zA-Z0-9]{1,10})$/igm)
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
            this.$store.dispatch('createAnonymousScan', { 'name': this.domain, 'ip_address': this.ip, 'port': this.port })
                .then(() => {
                    this.$store.state.domains.totalItems += 1
                    this.domain = ''
                    this.ip = null
                    this.port = null
                    useToast().success('Success')
                })
                .catch((e) => {
                    useToast().error(e.response.data.detail)
                })

        }
    },
}
</script>
