<template>
  <div class="col-md-8 mx-auto request">
    <div class="container mx-auto px-4">
      <div class="flex-mx-4">
        <div class="w-full">
          <h1>Enter email address</h1>
        </div>
      </div>
      <div class="flex-mx-4">
        <div class="w-full">
          <RequestForm />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RequestForm from '@/components/RequestForm'

export default {
    components: {
        RequestForm,
    } 
}
</script>
