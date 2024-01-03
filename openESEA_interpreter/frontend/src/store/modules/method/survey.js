import SurveyService from '../../../services/SurveyService'
import { debounce, random } from 'lodash'

const baseSurvey = { name: '', description: '', welcome_text: '', closing_text: '', min_threshold: 100, response_type: 'single', questions: [] }

export default {
    namespaced: true,
    state: {
        surveys: [],
        survey: {},
        error: undefined,
		debouncers: {},
        errors: {},
		isSaved: {}
    },
	getters: {
		getById: state => id => state.surveys.find(object => object.id === id),
		getSurveys: state => state.surveys
	},
    mutations: {
        setSurveys (state, { data }) {
			for (const survey of data) {
				console.log(survey) // survey.questions.sort()
			}
            state.surveys = data
            state.debouncers = {}
			state.errors = {}
			state.isSaved = {}
			state.error = undefined
        },
        setSurvey (state, { data }) {
            state.survey = data || {}
        },
        deleteSurvey (state, { id }) {
            delete state.debouncers[id]
			delete state.errors[id]
			delete state.isSaved[id]
			state.surveys = state.surveys.filter(q => q.id !== id)
        },
        setError (state, { error, id }) {
            if (id) {
                state.errors = {
                    ...state.errors,
                    [id]: error?.response?.data || error
                }
                return
			}
			state.error = error
        },
        updateList (state, { id, data }) {
			if (id !== data.id) {
			delete state.debouncers[id]
			delete state.errors[id]
			delete state.isSaved[id]
			}
			// data.questions?.sort()
			state.surveys = state.surveys.map((item) => {
				if (item.id !== id) return item
				return Object.assign(item, data)
			})
            console.log('surveys', state.surveys)
		},
		addNewSurvey (state, { method }) {
			const survey = { ...baseSurvey, id: random(-1000000, -1), method: method }
			state.surveys.push(survey)
            state.survey = survey
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
				async ({ mId, survey }) => {
					console.log('LLL', survey)
					const method = survey.id > 0 ? 'put' : 'post'
					const { response, error } = await SurveyService[method](
						{ mId, id, data: survey }
						)
					if (error) {
						console.log('---', survey, error.response.data)
						commit('setError', { error, id: survey.id })
						return
					}
                    console.log('------>', response.data)
					commit('setError', { error: {}, id: survey.id })
					commit('setIsSaved', { id: survey.id, isSaved: true })
                    commit('setSurvey', response)
					commit('updateList', { id: survey.id, data: response.data })
				},
				500
				)
			}
	},
    actions: {
        async fetchSurveys ({ commit }, payload) {
            const { response, error } = await SurveyService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setSurveys', response)
        },
        async fetchSurvey ({ commit }, payload) {
            const { response, error } = await SurveyService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateList', { id: payload.id, data: response.data })
            commit('setSurvey', response)
        },
        async deleteSurvey ({ commit }, payload) {
            if (payload.id > 0) {
                const { error } = await SurveyService.delete(payload)
                if (error) {
                    commit('setError', { error })
                    return
                }
            }
            commit('deleteSurvey', payload)
        },
        async updateSurvey ({ state, commit }, { mId, survey }) {
			if (!survey || !mId) return
			if (!state.debouncers[survey.id]) {
				commit('setDebouncer', { id: survey.id, commit })
			}
            if (survey.id < 0) {
                commit('updateList', { id: survey.id, data: survey })
            }
			commit('setIsSaved', { id: survey.id })
			if (!survey.name && state.isSaved[survey.id]) { return }
			await state.debouncers[survey.id]({ mId, survey })
		},
		setSurvey ({ state, commit }, { id }) {
            if (id) {
                const data = state.surveys.find(surveys => surveys.id === id)
                if (data && data.id === state.survey.id) return
                commit('setSurvey', { data: data })
            } else {
                commit('setSurvey', {})
            }
		},
		resetError ({ commit }) {
			commit('setError', { error: undefined })
		},
		async addNewSurvey ({ commit }, payload) {
			await commit('addNewSurvey', payload)
		}
	}
}
