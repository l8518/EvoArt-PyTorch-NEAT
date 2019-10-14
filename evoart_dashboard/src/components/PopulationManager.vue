<template>
  <div>
    <div class="container">
      <div class="row">
        <Individual class="border border-secondary col-4" :pop-id="i" v-for="i in popSize" :key="i" />
      </div>
    </div>
  </div>
</template>

<script>
import Individual from './Individual'
import Api from '../utils/api'

export default {
  name: 'PopulationManager',
  components: {
    Individual
  },
  data: function () {
    return {
      api: new Api('/'),
      loaded: false,
      popSize: 0
    }
  },
  created: function () {
    let qry = this.api.getPopulationSize()

    Promise.all([qry]).then((resArry) => {
      this.popSize = resArry[0].data.pop_size
      this.loaded = true
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
