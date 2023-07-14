<template>
    <div class="col-md-8 mx-auto checkout">
        <h1 class="display-4 fw-normal">Checkout</h1>
        <form v-show="this.showCardForm">
            <div ref="card"></div>
            <button @click.prevent="processPayment()" type="button" class="btn btn-primary btn-sm">Submit</button>
        </form>

        <div v-if="this.showSpinner">
            <i class="fa fa-spinner fa-pulse fa-10x fa-fw"></i>
        </div>
    </div>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
    name: 'Checkout',
    data() {
        return {
            accountType: this.$route.params.plan,
            card: null,
            stripe: null,
            elements: null,
            showCardForm: true,
            showSpinner: true,
            // customer: this.$store.state.account.post_excerpt,
        }
    },
    computed: {

    },
    methods: {
        clickContinue() {
            console.log('continue')
        },
        async processPayment() {
            const { error } = await this.stripe.confirmPayment({
                //`Elements` instance that was used to create the Payment Element
                elements: this.elements,
                // customer: this.customer,
                redirect: "if_required"
            });

            if (error) {
                // This point will only be reached if there is an immediate error when
                // confirming the payment. Show error to your customer (for example, payment
                // details incomplete)
                useToast().error(error.message);
                return
            }

            // Your customer will be redirected to your `return_url`. For some payment
            // methods like iDEAL, your customer will be redirected to an intermediate
            // site first to authorize the payment, then redirected to the `return_url`.

            // this.showCardForm = false
            const { paymentIntent } = await this.stripe.retrievePaymentIntent(this.$store.state.stripe.client_secret)
            // Inspect the PaymentIntent `status` to indicate the status of the payment
            // to your customer.
            //
            // Some payment methods will [immediately succeed or fail][0] upon
            // confirmation, while others will first enter a `processing` state.
            //
            // [0]: https://stripe.com/docs/payments/payment-methods#payment-notification
            switch (paymentIntent.status) {
                case 'succeeded':
                    useToast().success('Success! Payment received.');
                    this.$router.push('account')
                    break;

                case 'processing':
                    // message.innerText = "Payment processing. We'll update you when payment is received.";
                    break;

                case 'requires_payment_method':
                    // Redirect your user back to your payment page to attempt collecting
                    // payment again
                    useToast().error('Payment failed. Please try another payment method.');
                    this.showCardForm = true
                    // this.$route.push('checkout')
                    break;

                default:
                    useToast().error('Something went wrong.');
                    this.showAddressForm = true
                    // this.$route.push('checkout')
                    break;
            }

        },
    },
    mounted() {
        if (!this.addressExists) {
            this.showAddressDetail = true //false
            this.showAddressForm = true
        }

        const externalScript = document.createElement('script')
        externalScript.setAttribute('src', 'https://js.stripe.com/v3/')
        externalScript.setAttribute('type', 'module')
        document.head.appendChild(externalScript)

        externalScript.onload = () => {
            this.$store.dispatch('getPaymentIntent', { plan: this.$route.params.plan }).then(() => {
                this.stripe = Stripe(this.$store.state.stripe.publishable_key)
                this.elements = this.stripe.elements({
                    clientSecret: this.$store.state.stripe.client_secret,
                    appearance: { theme: 'stripe' },
                })
                let amount = 0
                if (this.$route.params.plan === 'basic') {
                    amount = 10
                }
                if (this.$route.params.plan === 'growth') {
                    amount = 10
                }
                if (this.$route.params.plan === 'ultimate') {
                    amount = 10
                }
                this.card = this.elements.create('payment', {
                    customer: this.$store.state.account.excerpt,
                    amount: 900,
                });
                this.card.mount(this.$refs.card);
            })
        }
    },
    beforeUnmount() {
        this.card = null;
        this.stripe = null;
        this.elements = null;
    },
}
</script>

<style scoped></style>