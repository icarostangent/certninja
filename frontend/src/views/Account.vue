<template>
  <div class="col-md-8 mx-auto account">
    <h1>Account</h1>
    <p>
      login: {{ username }}<br />
      billing email: {{ email }}
    </p>
    <div class="d-flex justify-content-between">
      <div col>
        <h3>Subscription</h3>
        <p>
          client reference id: {{ clientReferenceId }}<br />
          customer id: {{ customerId }}<br />
          subscription type: {{ subscriptionType }}<br />
          subscription active: {{ subscriptionActive }}<br />
          period start: {{ periodStart }}<br />
          period end: {{ periodEnd }}<br />
          previous subscription type: {{ previousSubscriptionType }}<br />
          cancel at: {{ cancelAt }}<br />
          cancel at period end: {{ cancelAtPeriodEnd }}<br />
        </p>
        <p v-show="subscriptionType !== 'starter' && customerId">
          <button @click.prevent="onClickGetPortal" type="button"
            class="btn btn-primary btn-sm">Update Subscription</button>
        </p>
      </div>
      <div col>
        <h3>Email</h3>
        <div v-for="email in emails.items">
          <p>
            email: {{ email.email }}<br />
            verified: {{ email.verified }}<br />
            verification sent: {{ email.verification_sent }}<br />
            reset key sent: {{ email.reset_sent }}<br />
          </p>
        </div>
        <Pagination @page-changed="emailPageChanged" :totalPages="emails.totalPages" :currentPage="currentEmailPage" />
      </div>
      <div col>
        <h3>Agents</h3>
        <div v-for="agent in agents.items">
          <p>
            name: {{ agent.name }}<br />
            api key: {{ agent.api_key }}<br />
            last seen: {{ agent.last_seen }}<br />
          </p>
        </div>
        <Pagination @page-changed="agentPageChanged" :totalPages="emails.totalPages" :currentPage="currentAgentPage" />
      </div>
    </div>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";

export default {
  name: 'Account',
  components: {
    Pagination,
  },
  computed: {
    username() {
      return this.$store.state.auth.user.username
    },
    email() {
      return this.$store.state.auth.user.email
    },
    clientReferenceId() {
      return this.$store.state.auth.user.subscription.client_reference_id
    },
    subscriptionType() {
      return this.$store.state.auth.user.subscription.subscription_type
    },
    subscriptionActive() {
      return this.$store.state.auth.user.subscription.subscription_active
    },
    periodStart() {
      return this.$store.state.auth.user.subscription.period_start
    },
    periodEnd() {
      return this.$store.state.auth.user.subscription.period_end
    },
    previousSubscriptionType() {
      return this.$store.state.auth.user.subscription.previous_subscription_type
    },
    cancelAt() {
      return this.$store.state.auth.user.subscription.cancel_at
    },
    cancelAtPeriodEnd() {
      return this.$store.state.auth.user.subscription.cancel_at_period_end
    },
    customerId() {
      return this.$store.state.auth.user.subscription.customer_id
    },
    portalHref() {
      return this.$store.state.portal
    },
    emails() {
      return this.$store.state.emails
    },
    agents() {
      return this.$store.state.agents
    },
  },
  data() {
    return {
      currentEmailPage: 1,
      currentAgentPage: 1,
      getCustomerPortal: false,
    }
  },
  methods: {
    emailPageChanged(page) {
      this.currentEmailPage = page;
      this.$store.dispatch('getEmails', { page: this.currentEmailPage });
    },
    agentPageChanged(page) {
      this.currentAgentPage = page;
      this.$store.dispatch('getAgents', { page: this.currentAgentPage });
    },
    onClickGetPortal(e) {
      this.getCustomerPortal = true
      this.$store.dispatch('getCustomerPortal').then(() => {
        window.location.href = this.$store.state.portal
      })
    },
  },
  mounted() {
    this.$store.dispatch('getUser')
    this.$store.dispatch('getEmails', { 'page': 1 })
    this.$store.dispatch('getAgents', { 'page': 1 })
  },
}
</script>