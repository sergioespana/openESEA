import SectionService from '../../../services/SectionService'
import { debounce, random } from 'lodash'

const baseSection = { title: 'new Section', questions: [] }

export default {
    namespaced: true,
    state: {
        sections: [],
        section: {},
        error: undefined,
		debouncers: {},
        errors: {},
		isSaved: {}
    },
	getters: {
		getById: state => id => state.sections.find(object => object.id === id),
        surveySections: (state) => {
			const filtered = {}
			state.sections.forEach((section) => { filtered[section.survey] = !filtered[section.survey] ? [section] : [...filtered[section.survey], section] })
			return filtered
		}
	},
    mutations: {
        setSections (state, { data }) {
			// for (const section of data) {
			// 	console.log(section) // section.questions.sort()
			// }
            state.sections = data
            state.debouncers = {}
			state.errors = {}
			state.isSaved = {}
			state.error = undefined
        },
        setSection (state, { data }) {
            state.section = data || {}
        },
        deleteSection (state, { id }) {
            delete state.debouncers[id]
			delete state.errors[id]
			delete state.isSaved[id]
			state.sections = state.sections.filter(s => s.id !== id)
            if (state.section.id === id) {
                state.section = {}
            }
        },
        updateList (state, { id, data }) {
			if (id !== data.id) {
			delete state.debouncers[id]
			delete state.errors[id]
			delete state.isSaved[id]
			}
			data.questions.sort()
			state.sections = state.sections.map((item) => {
				if (item.id !== id) return item
				return Object.assign(item, data)
			})
		},
		addNewSection (state, { survey }) {
			const section = { ...baseSection, id: random(-1000000, -1), survey }
			state.sections.push(section)
		},
		setIsSaved (state, { id, isSaved = false }) {
			if (id) {
				state.isSaved = {
					...state.isSaved,
					[id]: isSaved
				}
			}
		},
		setDebouncer (state, { id, commit }) {
			state.debouncers[id] = debounce(
				async ({ mId, sId, section }) => {
					const method = section.id > 0 ? 'put' : 'post'
					const { response, error } = await SectionService[method](
						{ mId, sId, id, data: section }
						)
					if (error) {
						commit('setError', { error, id: section.id })
						return
					}
					commit('setError', { error: {}, id: section.id })
					commit('setIsSaved', { id: section.id, isSaved: true })
					commit('updateList', { id: section.id, data: response.data })
				},
				500
			)
		},
        setError (state, { error, id }) {
            console.log(error?.response?.data)
            if (id) {
                state.errors = {
                    ...state.errors,
                    [id]: error?.response?.data || error
                }
                return
			}
			state.error = error
        },
        clearError (state) {
            state.error = []
        }
	},
    actions: {
        async fetchSections ({ commit }, payload) {
            const { response, error } = await SectionService.get(payload)
            commit('clearError')
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setSections', response)
        },
        async fetchSection ({ commit }, payload) {
            const { response, error } = await SectionService.get(payload)
            if (error) {
                commit('setError', { error })
            }
            commit('updateList', response)
            commit('setSection', response)
        },
        async createSection ({ commit, dispatch }, { mId, sId }) {
            const { response, error } = await SectionService.post({ mId, sId, data: baseSection })
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchSections', { mId: mId, sId: sId })
            commit('setSection', response)
        },
        async deleteSection ({ commit }, payload) {
            console.log('payload', payload)
            if (payload.id > 0) {
                const { error } = await SectionService.delete(payload)
                if (error) {
                    commit('setError', { error })
                    return
                }
            }
            commit('deleteSection', payload)
        },
       updateSection ({ state, commit }, { mId, sId, section }) {
			if (!section || !mId || !sId) return
			if (!state.debouncers[section.id]) {
				commit('setDebouncer', { id: section.id, commit })
			}
			commit('setIsSaved', { id: section.id })
			if (!section.title && state.isSaved[section.id]) return
			state.debouncers[section.id]({ mId, sId, section })
		},
		setSection ({ state, commit }, { id }) {
            if (id) {
                const data = state.sections.find(sections => sections.id === id)
                if (data && data.id === state.section.id) return
                commit('setSection', { data: data })
            } else {
                commit('setSection', {})
            }
		},
		resetError ({ commit }) {
			commit('setError', { error: undefined })
		},
		addNewSection ({ commit }, payload) {
			commit('addNewSection', payload)
		}
	}
}
// async updateSection ({ state, commit }, { mId, sId, data }) {
// const id = state.eseaAccount.id
// const data = state.eseaAccount
// const { response, error } = await SectionService.put({ mId, sId, id: data.id, data })
// if (error) {
//     commit('setError', { error })
//     return
// }
// commit('updateList', { id: response.data?.id, data: response.data })
// commit('setSection', response)
// },
