import { random, debounce, isInteger } from 'lodash'
import DirectIndicatorService from '../../../services/DirectIndicatorService'

const baseDirectIndicator = { key: '', name: '', description: '', isMandatory: true, datatype: '', options: [] }

export default {
    namespaced: true,
    state: {
        directIndicators: [],
        directIndicator: {},
        error: undefined,
        debouncers: {},
        errors: {},
        isSaved: {}
    },
    getters: {
        getById: state => id => state.directIndicators.find(object => object.id === id),
        topicDirectIndicators: (state) => {
            const filtered = {}
            state.directIndicators.forEach((directIndicator) => { filtered[directIndicator.topic] = !filtered[directIndicator.topic] ? [directIndicator] : [...filtered[directIndicator.topic], directIndicator] })
            return filtered
        },
        getValidDirectIndicatorNumber: (state) => {
            const indicators = state.directIndicators.map(indicator => parseInt(indicator.name.match(/[^_]*$/), 10)).filter(indicator => isInteger(indicator))
            return indicators.length ? Math.max(...indicators) + 1 : 1
        }
    },
    mutations: {
        setDirectIndicators (state, { data }) {
            if (data.length) {
                data.forEach(indicator => { indicator.objType = 'direct-indicator' })
            }
            state.directIndicators = data || {}
            state.debouncers = {}
            state.errors = {}
            state.isSaved = {}
        },
        setDirectIndicator (state, { data }) {
            state.directIndicator = data || {}
        },
        deleteDirectIndicator (state, { id }) {
            delete state.debouncers[id]
            delete state.errors[id]
            delete state.isSaved[id]
            state.directIndicators = state.directIndicators.filter(i => i.id !== id)
            if (state.directIndicator.id === 'id') {
                state.directIndicator = {}
            }
        },
        updateList (state, { id, data }) {
            if (id !== data.id) {
                delete state.debouncers[id]
                delete state.errors[id]
                delete state.isSaved[id]
            }
            state.directIndicators = state.directIndicators.map((item) => {
                if (item.id !== id) { return item }
                return Object.assign(item, data)
            })
        },
        addNewDirectIndicator (state, { topic, question }) {
            const directIndicator = { ...baseDirectIndicator, id: random(-1000000, -1), topic, question }
            state.directIndicators.push(directIndicator)
            state.directIndicator = directIndicator
        },
        setDebouncer (state, { id, commit }) {
            state.debouncers[id] = debounce(
                async ({ mId, directIndicator }) => {
                    const method = directIndicator.id > 0 ? 'put' : 'post'
                    const { response, error } = await DirectIndicatorService[method]({ mId, id, data: directIndicator })
                    if (error) {
                        commit('setError', { error, id: directIndicator.id })
                        return
                    }
                    commit('setError', { error: {}, id: directIndicator.id })
					commit('setIsSaved', { id: directIndicator.id, isSaved: true })
					commit('updateList', { id: directIndicator.id, data: response.data })
                },
                1000
            )
        },
        setIsSaved (state, { id, isSaved = false }) {
            if (id) {
                state.isSaved = {
                    ...state.isSaved,
                    [id]: isSaved
                }
            }
        },
        setError (state, { error, id }) {
            console.log(error?.response?.data)
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
        async fetchDirectIndicators ({ commit }, payload) {
            commit('clearError')
            const { response, error } = await DirectIndicatorService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setDirectIndicators', response)
        },
        async patchDirectIndicator ({ commit }, { mId, id, data }) {
            const { response, error } = await DirectIndicatorService.patch({ mId: mId, id: id, data: data, headers: { 'Content-Type': 'application/json' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateList', { id: id, data: response.data })
            commit('setDirectIndicator', response)
        },
        updateDirectIndicator ({ state, commit }, { mId, directIndicator }) {
            if (directIndicator.topic === null) {
                delete directIndicator.topic
            }
            commit('clearError')
            delete state.errors[directIndicator.id]

            if (!directIndicator || !mId) { return }
            if (!state.debouncers[directIndicator.id]) {
                commit('setDebouncer', { id: directIndicator.id, commit })
            }
            if (directIndicator.id < 0) {
                commit('updateList', { id: directIndicator.id, data: directIndicator })
            }
            commit('setIsSaved', { id: directIndicator.id })
            if (!directIndicator.name || !directIndicator.key) { return }
            state.debouncers[directIndicator.id]({ mId, directIndicator })
        },
        async deleteDirectIndicator ({ commit }, payload) {
            if (payload.id > 0) {
                const { error } = await DirectIndicatorService.delete(payload)
                if (error) {
                    commit('setError', { error })
                    return
                }
            }
            commit('deleteDirectIndicator', payload)
        },
        setDirectIndicator ({ state, commit }, { id } = {}) {
            if (id) {
            const data = state.directIndicators.find(indicator => indicator.id === id)
            if (data && data.id === state.directIndicator.id) { return data }
            commit('setDirectIndicator', { data })
            } else {
                commit('setDirectIndicator', {})
            }
        },
        resetError ({ commit }) {
            commit('setError', { error: undefined })
        },
        addNewDirectIndicator ({ commit }, payload) {
            commit('addNewDirectIndicator', payload)
        }
    }
}
