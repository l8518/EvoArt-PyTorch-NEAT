import { shallowMount } from '@vue/test-utils'
import PopulationManager from '@/components/PopulationManager.vue'

describe('PopulationManager.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = 'new message'
    const wrapper = shallowMount(PopulationManager, {
      propsData: { msg }
    })
    expect(wrapper.text()).toMatch(msg)
  })
})
