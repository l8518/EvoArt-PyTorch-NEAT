<template>
  <div>
    <div class="container">
      <div class="row">
        <Individual class="border border-secondary col-3" v-on:selected="onSelected" :pop-id="popId" v-for="popId in currentPopulation" :key="popId" />
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
      currentPopulation: []
    }
  },
  created: function () {
    let qry = this.api.getCurrentPopulation()

    Promise.all([qry]).then((resArry) => {
      this.currentPopulation = resArry[0].data.population
      this.loaded = true
    })
  },
  methods: {
    onSelected () {
      let qry = this.api.getCurrentPopulation()
      this.currentPopulation = []
      Promise.all([qry]).then((resArry) => {
        this.currentPopulation = resArry[0].data.population
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
