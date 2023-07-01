<template>
    <div id="createDomainForm">
        <form class="mb-3">
            <div class="form-control">
                <input class="form-control" type="text" v-model="domain" name="domain" placeholder="Domain" />
                <div class="input-group">
                    <input class="form-control" type="text" v-model="ip" name="ip"
                        placeholder="IP Address (Use to bypass DNS lookup)" />
                    <input class="form-control" type="text" v-model="port" name="ip" placeholder="Port (optional)" />
                </div>
                <button @click.prevent="onClickCreate" type="button" class="btn btn-primary btn-sm">Save</button>
            </div>
        </form>
    </div>
</template>

<script>
import { useToast } from 'vue-toastification'

export default {
    name: 'DomainCreate',
    data() {
        return {
            domain: '',
            ip: '',
            port: '',
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
            if (!this.ip && !this.port) {
                this.$store.dispatch('createDomain', { 'domain': this.domain })
                this.$store.state.domains.totalItems += 1
                this.domain = ''
                useToast().success('Success')
                return
            }
            if (this.ip && !this.port) {
                this.$store.dispatch('createDomain', { 'domain': this.domain, 'ip': this.ip })
                this.$store.state.domains.totalItems += 1
                this.domain = ''
                this.ip = ''
                useToast().success('Success')
                return
            }
            if (!this.ip && this.port) {
                this.$store.dispatch('createDomain', { 'domain': this.domain, 'ip': `:${this.port}` })
                this.$store.state.domains.totalItems += 1
                this.domain = ''
                this.port = ''
                useToast().success('Success')
                return
            }
            if (this.ip && this.port) {
                this.$store.dispatch('createDomain', { 'domain': this.domain, 'ip': `${this.ip}:${this.port}` })
                this.$store.state.domains.totalItems += 1
                this.domain = ''
                this.ip = ''
                this.port = ''
                useToast().success('Success')
                return
            }
        }
    },
}
</script>
