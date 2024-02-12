<template>
    <div class="col-md-8 mx-auto domains">
        <h1>Domains</h1>
        <div class="col-md-8 d-flex justify-content-end flex-fill">
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1"
                    data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fa fa-cog"></i>
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                    <li><a @click.prevent="trackDomain" class="dropdown-item" href="#">Track Domain</a></li>
                </ul>
            </div>
        </div>
        <BannerUpgrade v-if="!showDomainCreate" />
        <DomainCreate v-if="showDomainCreate" />
        <DomainList />
    </div>
</template>

<script>
import BannerUpgrade from '@/components/BannerUpgrade.vue'
import DomainCreate from '@/components/DomainCreate.vue'
import DomainList from '@/components/DomainList.vue'

export default {
    name: 'Domains',
    components: {
        BannerUpgrade,
        DomainCreate,
        DomainList,
    },
    data() {
        return {}
    },
    computed: {
        showDomainCreate() {
            if (this.$store.state.account.user_role === 'starter') {
                return (this.$store.state.domains.totalItems < 1);
                // return true;
            }
            else if (this.$store.state.account.user_role === 'basic') {
                return (this.$store.state.domains.totalItems < 5);
                // return true;
            }
            else if (this.$store.state.account.user_role === 'growth') {
                return (this.$store.state.domains.totalItems < 25);
                // return true;
            }
            else if (this.$store.state.account.user_role === 'ultimate') {
                return (this.$store.state.domains.totalItems < 100);
                // return true;
            }
            return true;
        },
    },
}
</script>
