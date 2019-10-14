<template>
  <div>
    <img :src="`/render_individual/${popId}`" />
    <button class="btn btn-primary" v-on:click="onClick">I win</button>
  </div>
</template>

<script>
import Api from '../utils/api'

export default {
  name: 'Individual',
  props: {
    popId: {
      type: Number,
      default: 0
    }
  },
  data: function () {
    return {
      api: new Api('/')
    }
  },
  methods: {
    onClick () {
      this.api.selectPop(this.popId).then(() => {
        window.location.reload()
      })
      return this.popId
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
