import AccountAuditService from '@/services/AccountAuditService'

export default {
    namespaced: true,
    state: {
        accountAudits: [],
        accountAudit: {},
        startedAudit: false,
        error: []
    },
    mutations: {
        setAccountAudits (state, { data }) {
            state.accountAudits = data
        },
        setAccountAudit (state, { data }) {
            state.accountAudit = data || {}
        },
        updateAccountAudit (state, { data, id }) {
            state.accountAudits = state.accountAudits.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        changeStartedAudit (state, data) {
            state.startedAudit = data
        },
        // deleteEseaAccount (state, { id }) {
        //     state.eseaAccounts = state.eseaAccounts.filter(e => e.id !== id)
        // },
        setError (state, { error }) {
            console.log('my error:', error?.response.data)
            state.error = error?.response.data || []
        }
    },
    actions: {
        async fetchAccountAudits ({ commit }, payload) {
            const { response, error } = await AccountAuditService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setAccountAudits', response)
        },
        async fetchAccountAudit ({ commit }, payload) {
            const { response, error } = await AccountAuditService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setAccountAudit', response)
        },
        // async createEseaAccount ({ commit, dispatch }, { oId, data }) {
        //     const { response, error } = await EseaAccountService.post({ oId, data: data })
        //     if (error) {
        //         commit('setError', { error })
        //         return
        //     }
        //     await dispatch('fetchEseaAccounts', { oId })
        //     await commit('setEseaAccount', response)
        // },
        async updateAccountAudit ({ commit }, { oId, eaId, data }) {
            const { response, error } = await AccountAuditService.put({ oId, eaId, id: data.id, data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            console.log('account audit:', response.data)
            commit('updateAccountAudit', response)
            commit('setAccountAudit', response)
        },
        // async deleteEseaAccount ({ commit, dispatch }, payload) {
        //     const { error } = await EseaAccountService.delete(payload)
        //     if (error) {
        //         commit('setError', { error })
        //         return
        //     }
        //     commit('deleteEseaAccount', payload)
        //     commit('setEseaAccount', {})
        // },
        setAccountAudit ({ state, commit }, { id }) {
            if (id) {
                const data = state.accountAudit.find(e => e.id === id)
                commit('setAccountAudit', { data: data })
            } else {
                commit('setAccountAudit', {})
            }
        },
        changeStartedAudit ({ commit }, data) {
            commit('changeStartedAudit', data)
        }
    }
}
