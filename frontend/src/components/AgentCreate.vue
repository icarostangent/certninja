<template>
    <div id="createAgentForm">
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
    name: 'AgentCreate',
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
            this.$store.dispatch('createDomain', { 'name': this.domain, 'ip_address': this.ip, 'port': this.port })
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
