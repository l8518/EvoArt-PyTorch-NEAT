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

  getPopulationSize () {
    return this._http.get(`popsize`)
  }

}
