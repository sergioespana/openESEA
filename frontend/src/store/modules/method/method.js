import MethodService from '../../../services/MethodService'
import { AxiosInstance } from '../../../plugins/axios'
import _ from 'lodash'

const baseMethod = { name: 'Untitled method', description: '...' }

export default {
    namespaced: true,
    state: {
        methods: [],
        method: { },
        error: undefined,
        isSaved: undefined,
        debouncer: _.debounce(async ({ id, method, commit }) => {
            const { response, error } = await MethodService.put({ id: id, data: method })
            if (error) {
                commit('setError', { error })
            } else {
                console.log('debouncing', response)
                commit('setIsSaved', { isSaved: true })
                commit('clearError')
                commit('updateList', { id: method.id, data: response.data })
            }
        }, 1000)
    },
    mutations: {
        setMethods (state, { data }) {
            state.methods = data
            state.errors = []
            state.isSaved = true
        },
        setMethod (state, { data }) {
            state.method = { ...data } || baseMethod
            state.error = []
            state.isSaved = true
        },
        addMethodToList (state, { data }) {
            state.methods.push(data)
        },
        deleteMethod (state, { id }) {
            state.methods = state.methods.filter(m => m.id !== id)
        },
        updateList (state, { id, data }) {
            if (id !== data.id) {
                state.error = []
                state.isSaved = false
            }
            state.methods = state.methods.map((item) => {
                if (item.id !== id) { return item }
                return Object.assign(item, data)
            })
        },
        setIsSaved (state, { isSaved = false }) {
            state.isSaved = isSaved
        },
        setError (state, { error }) {
            console.log(error?.response?.data)
            state.error = error?.response?.data || []
        },
        clearError (state) {
            state.error = []
        }
    },
    actions: {
        async fetchMethods ({ commit }, payload) {
            commit('clearError')
            const { response, error } = await MethodService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setMethods', response)
        },
        async fetchMethod ({ commit }, payload) {
            const { response, error } = await MethodService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setMethod', response)
        },
        async uploadMethod (payload) {
            var formData = new FormData()
            formData.append('file', payload)
            console.log(payload)
            return new Promise((resolve, reject) => {
                AxiosInstance.post('/import-yaml/', formData, { headers: { 'Content-Type': 'multipart/form-data' } }) // { headers: { 'Content-Type': 'multipart/form-data' } }
            .then(response => {
                console.log(response)
                resolve()
                })
            .catch(err => { reject(err) })
            })
        },
        async createMethod ({ commit, dispatch }, { data }) {
            const { response, error } = await MethodService.post({ data: data || baseMethod })
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchMethods', {})
            await commit('setMethod', response)
        },
        async updateMethod ({ state, commit }, method) {
            if (method.id !== state.method.id) { return }
            commit('setIsSaved', {})
            state.debouncer({ id: method.id, method, commit })
        },
        async deleteMethod ({ commit }, payload) {
            const { error } = await MethodService.delete(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('deleteMethod', payload)
            commit('setMethod', {})
        },
        setMethod ({ state, commit }, { id }) {
            if (id) {
                const data = state.methods.find(m => m.id === id)
                commit('setMethod', { data })
            } else {
                commit('setMethod', {})
            }
        }
    }
}
