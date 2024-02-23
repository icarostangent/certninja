<template>
    <div class="container">
        <div class="row mb-5">
            <div class="col">
                <h1 class="mb-3">Domains</h1>
                <router-link class="btn btn-primary mb-3" to="/domains/create/">Track Domain</router-link>
                <div class="col-md-6">
                    <label for="search" class="form-label">Search</label>
                    <input @input="searchDomains" v-model="search" type="text" class="form-control mb-3" id="search" />
                </div>
                <div class="table-responsive mb-3">
                    <table class="table">
                        <thead>
                            <th></th>
                            <th>Domain</th>
                            <th>IP Address</th>
                            <th>Port</th>
                            <th>Activity</th>
                            <th>Error</th>
                            <th></th>
                        </thead>
                        <tbody>
                            <tr v-for="item in domains.items" :key="item.id" @click.prevent="showDomain(item.id)"
                                class="domain-item">
                                <td v-if="item.scan_status !== 'complete'"><i class="fa fa-spinner fa-pulse fa-2x"></i></td>
                                <td v-else-if="item.last_scan_error"><i class="fas fa-exclamation fa-2x"></i></td>
                                <td v-else><i class="fas fa-check fa-2x"></i></td>
                                <td>{{ item.name }}</td>
                                <td>{{ item.ip_address }}</td>
                                <td>{{ item.port }}</td>
                                <td>{{ new Date(item.modified).toLocaleString() }}</td>
                                <td>{{ item.last_scan_error }}</td>
                                <td><a class="btn btn-secondary rounded-pill">Show</a></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <Pagination @page-changed="pageChanged" :totalPages="domains.totalPages" :currentPage="currentPage" />
            </div>
        </div>
    </div>
</template>

<script>
import Pagination from "@/components/Pagination";

export default {
    name: 'Domains',
    components: {
        Pagination,
    },
    data() {
        return {
            currentPage: 1,
            now: new Date(),
            interval: null,
            search: "",
        };
    },
    computed: {
        domains() {
            return this.$store.state.domains;
        },
    },
    mounted() {
        this.$store.dispatch("getDomains", { page: this.currentPage })
            .then(() => {
                this.interval = setInterval(() => {
                    this.domains.items.forEach((item) => {
                        if (item.scan_status !== 'complete') {
                            this.$store.dispatch("pollDomain", { domainId: item.id })
                                .then((domain) => {
                                    if (domain.scan_status === "complete") {
                                        this.domains.items = this.domains.items.map((item) => {
                                            if (item.id === domain.id) {
                                                return domain;
                                            }
                                            return item;
                                        });
                                    }
                                });
                        }
                    });
                }, 2000);
            });
    },
    beforeUnmount() {
        this.interval = null;
    },
    methods: {
        showDomain(id) {
            this.$router.push({ name: 'domain', params: { id: id } })
        },
        pageChanged(page) {
            this.currentPage = page;
            this.$store.dispatch("getDomains", { page: this.currentPage });
        },
        searchDomains() {
            this.$store.dispatch("searchDomains", { search: this.search });
        },

    },
}
</script>

<style scope>
.domain-item {
    cursor: pointer;
}
</style>