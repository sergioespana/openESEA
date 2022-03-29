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
        // update list instead of pushing complete object
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
            // set information of direct indicator. Temporary id is created (negative number), which is used untill direct indicator is pushed to backend and gets permanend id.
            const directIndicator = { ...baseDirectIndicator, id: random(-1000000, -1) }//, topic, question }
            console.log('topic' + topic, 'question' + question)
            // new direct indicator is pushed to local storage
            state.directIndicators.push(directIndicator)
            // new direct indicator is set as active direct indicator
            state.directIndicator = directIndicator
        },
        setDebouncer (state, { id, commit }) {
            state.debouncers[id] = debounce(
                async ({ mId, directIndicator }) => {
                    // check if indicator exists in database (positive id) or not (negative, temporary id). Uses put or post dependent on this. Put/post can be found in BaseApiService.
                    const method = directIndicator.id > 0 ? 'put' : 'post'
                    // call to backend. DirectIndicatorService. Payload in curly braces.
                    const { response, error } = await DirectIndicatorService[method]({ mId, id, data: directIndicator })
                    // check if error, if yes, save error and return.
                    if (error) {
                        commit('setError', { error, id: directIndicator.id })
                        return
                    }
                    // make changes to state by calling other mutations
                    // empty error list
                    commit('setError', { error: {}, id: directIndicator.id })
					// set saved to true, indicating that indicator has been saved to database
                    commit('setIsSaved', { id: directIndicator.id, isSaved: true })
                    // update local storage list (eg with new non-temporary id)
					commit('updateList', { id: directIndicator.id, data: response.data })
                    // update local storage current object
                    commit('setDirectIndicator', response)
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
            // clear previous errors
            commit('clearError')
            delete state.errors[directIndicator.id]

            // check if payload is complete
            if (!directIndicator || !mId || !directIndicator.name || !directIndicator.key) { return }

            // reset unsaved status: indicate that indicator has not yet been saved to database
            commit('setIsSaved', { id: directIndicator.id })

            // check if call has already been recently made for this indicator. Debouncer object avoid database call overload.
            if (!state.debouncers[directIndicator.id]) {
                // where the magic happens: call to database
                commit('setDebouncer', { id: directIndicator.id, commit })
            }
            // check if id is negative (ie if id is temporary from local storage), and call updatelist to update localstorage
            if (directIndicator.id < 0) {
                commit('updateList', { id: directIndicator.id, data: directIndicator })
            }
            // add debouncer for this indicator to local storage (?)
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
            // call mutation addNewDirectIndicator
            commit('addNewDirectIndicator', payload)
        }
    }
}
