import axios from 'axios'

/**
 * The API Class
 */
export default class Api {
  _http
  constructor (url) {
    this._http = axios.create({
      baseURL: url,
      headers: { 'Content-Type': 'application/json' }
    })
  }

  getCurrentPopulation () {
    return this._http.get(`current_population`)
  }

  selectPop (popnum) {
    return this._http.post(`select_individual/${popnum}`) // TODO: Refactor this, not really good
  }

}
