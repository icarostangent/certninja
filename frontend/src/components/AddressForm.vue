<template>
    <form>
        <div class="input-group">
            <input class="form-control" type="text" v-model="this.addressForm.firstName" name="firstName"
                placeholder="First name" />
            <input class="form-control" type="text" v-model="this.addressForm.lastName" name="lastName"
                placeholder="Last name" />
        </div>
        <input class="form-control" type="text" v-model="this.addressForm.line1" name="line1"
            placeholder="Address line 1" />
        <input class="form-control" type="text" v-model="this.addressForm.line2" name="line2"
            placeholder="Address line 2" />
        <div class="input-group">
            <input class="form-control" type="text" v-model="this.addressForm.city" name="city" placeholder="City" />
            <input class="form-control" type="text" v-model="this.addressForm.state" name="state" placeholder="State" />
        </div>
        <div class="input-group">
            <input class="form-control" type="text" v-model="this.addressForm.postalCode" name="postalCode"
                placeholder="Postal code" />
            <input class="form-control" type="text" v-model="this.addressForm.country" name="couintry"
                placeholder="Country" />
        </div>
        <button @click.prevent="processAddress" type="button" class="btn btn-primary btn-sm">Submit</button>
    </form>
</template>

<script>
export default {
    name: 'AddressForm',
}
</script>

<style scoped>
</style>