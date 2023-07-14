<template>
  <div class="col-md-8 mx-auto subscribe">
    <header>
      <div class="pricing-header p-3 pb-md-4 mx-auto text-center">
        <h1 class="display-4 fw-normal">Subscribe</h1>
        <p class="fs-5 text-muted">Subscribe now to be a total badass</p>
      </div>
    </header>

    <main>
      <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
        <div class="col">
          <ProductList />
        </div>
      </div>

      <h2 class="display-6 text-center mb-4">Compare plans</h2>

      <div class="table-responsive">
        <table class="table text-center">
          <thead>
            <tr class="headRow">
              <th style="width: 24%;"></th>
              <th style="width: 19%;">Basic</th>
              <th style="width: 19%;">Growth</th>
              <th style="width: 19%;">Ultimate</th>
              <th style="width: 19%;">Enterprise</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row" class="text-start">Domains</th>
              <td>5</td>
              <td>25</td>
              <td>100</td>
              <td>Unlimited</td>
            </tr>
            <tr class="evenRow">
              <th scope="row" class="text-start">Scan History</th>
              <td>1 Month</td>
              <td>3 Months</td>
              <td>6 Months</td>
              <td>12+ Months</td>
            </tr>
            <tr>
              <th scope="row" class="text-start">Scan Frequency</th>
              <td>Weekly</td>
              <td>Up To Daily</td>
              <td>Up To Hourly</td>
              <td>Up To 10 min</td>
            </tr>
            <tr class="evenRow">
              <th scope="row" class="text-start">Expiration Notice within</th>
              <td>60 Days</td>
              <td>120 Days</td>
              <td>365 Days</td>
              <td>365 Days</td>
            </tr>
          </tbody>

          <tbody>
            <tr class="headRow">
              <th scope="row" class="text-start">Notification Types/Details:</th>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            <tr>
              <th scope="row" class="text-start">&nbsp;&nbsp;&nbsp;Expired</th>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
            </tr>
            <tr class="evenRow">
              <th scope="row" class="text-start">&nbsp;&nbsp;&nbsp;Expiring</th>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
            </tr>
            <tr>
              <th scope="row" class="text-start">&nbsp;&nbsp;&nbsp;Invalid</th>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
            </tr>
            <tr class="evenRow">
              <th scope="row" class="text-start">&nbsp;&nbsp;&nbsp;Weak Cipher Warning</th>
              <td></td>
              <td></td>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
            </tr>
            <tr>
              <th scope="row" class="text-start">Notificaiton Frequency Adjustment</th>
              <td></td>
              <td></td>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
            </tr>
            <tr class="evenRow">
              <th scope="row" class="text-start">Multiple Notificaiton Recipients</th>
              <td></td>
              <td></td>
              <td><i class="fas fa-check"></i></td>
              <td><i class="fas fa-check"></i></td>
            </tr>
            <tr>
              <th scope="row" class="text-start"></th>
              <td><button @click.prevent="submitBasic()" type="button"
                  class="w-100 btn btn-lg btn-outline-primary">Subscribe</button></td>
              <td><button @click.prevent="submitGrowth()" type="button"
                  class="w-100 btn btn-lg btn-outline-primary">Subscribe</button></td>
              <td><button @click.prevent="submitUltimate()" type="button"
                  class="w-100 btn btn-lg btn-outline-primary">Subscribe</button></td>
              <td><a href="/page/contact"><button type="button" class="w-100 btn btn-lg btn-outline-primary">Contact
                    Us</button></a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>
  </div>
</template>

<script>
import ProductList from "@/components/ProductList";

export default {
  name: 'Subscribe',
  components: {
    ProductList,
  },
  methods: {
    submitBasic() {
      //   this.$store.dispatch('subscribe', { price_id: 'price_1L60qbH5nGHVgNhzf762dtbt' }).then((res) => window.location.href = res.url)
      this.$router.push({ name: 'checkout', params: { plan: 'basic' } })
    },
    submitGrowth() {
      //   this.$store.dispatch('subscribe', { price_id: 'price_1L60r5H5nGHVgNhzrhNxesNi' }).then((res) => window.location.href = res.url)
      this.$router.push({ name: 'checkout', params: { plan: 'growth' } })
    },
    submitUltimate() {
      //   this.$store.dispatch('subscribe', { price_id: 'price_1L60rcH5nGHVgNhz0ApjoktB' }).then((res) => window.location.href = res.url)
      this.$router.push({ name: 'checkout', params: { plan: 'ultimate' } })
    },
  },
};
</script>
