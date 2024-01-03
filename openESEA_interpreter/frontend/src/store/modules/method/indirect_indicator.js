import { debounce, isInteger, random } from 'lodash' // random, debounce,
import IndirectIndicatorService from '../../../services/IndirectIndicatorService'

const baseIndirectIndicator = { name: '', formula: '' }

export default {
    namespaced: true,
    state: {
        indirectIndicators: [],
        indirectIndicator: {},
        error: undefined,
        debouncers: {},
        errors: {},
        isSaved: {}
    },
    getters: {
        getById: state => id => state.indirectIndicatorsfilter(object => object.id === id),
        topicIndirectIndicators: (state) => {
            const filtered = {}
            state.indirectIndicators.forEach((indirectIndicator) => {
                filtered[indirectIndicator.topic] = !filtered[indirectIndicator.topic] ? [indirectIndicator] : [...filtered[indirectIndicator.topic], indirectIndicator]
            })
            console.log('filtered:', filtered)
            return filtered
        },
        // What does this getter do exactly?
        getValidIndirectIndicatorNumber: (state) => {
            const indicators = state.indirectIndicators.map(indicator => parseInt(indicator.name.match(/[^_]*$/), 10)).filter(indicator => isInteger(indicator))
            return indicators.length ? Math.max(...indicators) + 1 : 1
        }
    },
    mutations: {
        setIndirectIndicators (state, { data }) {
            if (data.length) {
                data.forEach(indicator => { indicator.objType = 'indirect-indicator' })
            }
            state.indirectIndicators = data || {}
            state.debouncers = {}
            state.errors = {}
            state.isSaved = {}
        },
        setIndirectIndicator (state, { data }) {
            state.indirectIndicator = data || {}
        },
        deleteIndirectIndicator (state, { id }) {
            delete state.debouncers[id]
            delete state.errors[id]
            delete state.isSaved[id]
            state.indirectIndicators = state.indirectIndicators.filter(i => i.id !== id)
        },
        updateList (state, { id, data }) {
            if (id !== data.id) {
                delete state.debouncers[id]
                delete state.errors[id]
                delete state.isSaved[id]
            }
            state.indirectIndicators = state.indirectIndicators.map((item) => {
                if (item.id !== id) { return item }
                return Object.assign(item, data)
            })
        },
        addNewIndirectIndicator (state) {
            const indirectIndicator = { ...baseIndirectIndicator, id: random(-1000000, -1) }
            state.indirectIndicators.push(indirectIndicator)
            state.indirectIndicator = indirectIndicator
        },
        setDebouncer (state, { id, commit }) {
            state.debouncers[id] = debounce(
                async ({ mId, indirectIndicator }) => {
                    const method = indirectIndicator.id > 0 ? 'put' : 'post'
                    const { response, error } = await IndirectIndicatorService[method]({ mId, id, data: indirectIndicator })
                if (error) {
                    commit('setError', { error, id: indirectIndicator.id })
                    return
                }
                console.log('saving indirect indicator...', indirectIndicator.id)
                console.log('response.data:', response.data)
                commit('setError', { error: {}, id: indirectIndicator.id })
                commit('setIsSaved', { id: indirectIndicator.id, isSaved: true })
				commit('updateList', { id: indirectIndicator.id, data: response.data })
                commit('setIndirectIndicator', response)
            }, 1000
            )
        },
        setIsSaved (state, { id, isSaved = false }) {
            if (id) {
                state.isSaved = { ...state.isSaved, [id]: isSaved }
            }
        },
        setError (state, { error, id }) {
            console.log(id, '--', error?.response?.data)
            if (id && error?.response?.data) {
                state.errors = { ...state.errors, [id]: error?.response?.data }
                return
            }
            state.error = error
        },
        clearError (state) {
            state.error = []
        }
    },
    actions: {
        async fetchIndirectIndicators ({ commit }, payload) {
            const { response, error } = await IndirectIndicatorService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setIndirectIndicators', response)
        },
        updateIndirectIndicator ({ state, commit }, { mId, indirectIndicator }) {
            indirectIndicator.formula = indirectIndicator.formula.replace('\n', '')
            if (indirectIndicator.topic === null) {
                delete indirectIndicator.topic
            }
            commit('clearError')
            delete state.errors[indirectIndicator.id]
            if (!indirectIndicator || !mId) { return }
            if (!state.debouncers[indirectIndicator.id]) {
                commit('setDebouncer', { id: indirectIndicator.id, commit })
            }
            if (indirectIndicator.id < 0) {
                commit('updateList', { id: indirectIndicator.id, data: indirectIndicator })
            }
            commit('setIsSaved', { id: indirectIndicator.id })
            if (!indirectIndicator.name) { return }
            state.debouncers[indirectIndicator.id]({ mId, indirectIndicator })
        },
        async patchIndirectIndicator ({ commit }, { mId, id, data }) {
            console.log('LLL', data)
            const { response, error } = await IndirectIndicatorService.patch({ mId: mId, id: id, data: data, headers: { 'Content-Type': 'application/json' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateList', { id: id, data: response.data })
            commit('setIndirectIndicator', response)
        },
        async deleteIndirectIndicator ({ commit }, payload) {
            if (payload.id > 0) {
                const { error } = await IndirectIndicatorService.delete(payload)
                if (error) {
                    commit('setError', { error })
                    return
                }
            }
            commit('deleteIndirectIndicator', payload)
        },
        setIndirectIndicator ({ state, commit }, { id } = {}) {
            const data = state.indirectIndicators.find(indirectIndicator => indirectIndicator.id === id)
            if (data && data.id === state.indirectIndicator.id) return
            commit('setIndirectIndicator', { data })
        },
        resetError ({ commit }) {
            commit('setError', { error: undefined })
        },
        addNewIndirectIndicator ({ commit }, payload) {
            commit('addNewIndirectIndicator', payload)
        }
    }
}
