import { random, debounce, isInteger } from 'lodash'
import QuestionService from '../../../services/QuestionService'

const baseQuestion = { name: '', description: '', isMandatory: true, uiComponent: null, direct_indicator: [] }

export default {
    namespaced: true,
    state: {
        questions: [],
        question: {},
        error: undefined,
		debouncers: {},
		errors: {},
		isSaved: {}
    },
	getters: {
		getById: state => id => state.questions.find(object => object.id === id),
		topicQuestions: (state) => {
			const filtered = {}
			state.questions.forEach((question) => { filtered[question.topic] = !filtered[question.topic] ? [question] : [...filtered[question.topic], question] })
            console.log('questions:', filtered)
			return filtered
		},
        sectionQuestions: (state) => {
            const filtered = {}
            state.questions.forEach((question) => { filtered[question.section] = !filtered[question.section] ? [question] : [...filtered[question.section], question] })
            return filtered
        },
		getValidQuestionKeyNumber: (state) => {
			const indicators = state.questions
				.map(indicator => parseInt(indicator.direct_indicators?.[0].key.match(/[^_]*$/), 10))
				.filter(indicator => isInteger(indicator))
			return indicators.length ? Math.max(...indicators) + 1 : 1
		}
	},
    mutations: {
        setQuestions (state, { data }) {
			state.questions = data
			state.debouncers = {}
			state.errors = {}
			state.isSaved = {}
		},
		setQuestion (state, { data }) {
			state.question = data || {}
		},
		deleteQuestion (state, { id }) {
			delete state.debouncers[id]
			delete state.errors[id]
			delete state.isSaved[id]
			state.questions = state.questions.filter(q => q.id !== id)
            if (state.question.id === id) {
                state.question = {}
            }
		},
		updateList (state, { id, data }) {
			if (id !== data.id) {
				delete state.debouncers[id]
				delete state.errors[id]
				delete state.isSaved[id]
			}

			state.questions = state.questions.map((item) => {
				if (item.id !== id) return item
				return Object.assign(item, data)
			})
		},
		addNewQuestion (state, { section }) {
			const question = { ...baseQuestion, id: random(-1000000, -1), section }
			state.questions.push(question)
			state.question = question
		},
		setDebouncer (state, { id, commit }) {
			state.debouncers[id] = debounce(
				async ({ mId, SuId, SeId, question }) => {
					const method = question.id > 0 ? 'put' : 'post'
                    if (question.direct_indicator.length) {
                        question.direct_indicator = [question.direct_indicator[0].id] || []
                    }
					const { response, error } = await QuestionService[method](
						{ mId, SuId, SeId, id, data: question }
					)
					if (error) {
						commit('setError', { error, id: question.id })
						return
					}
					commit('setError', { error: {}, id: question.id })
					commit('setIsSaved', { id: question.id, isSaved: true })
					commit('updateList', { id: question.id, data: response.data })
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
        async fetchQuestions ({ commit }, payload) {
            commit('clearError')
			const { response, error } = await QuestionService.get(payload)
			if (error) {
				commit('setError', { error })
				return
			}
            commit('setQuestions', response)
        },
        async deleteQuestion ({ commit }, payload) {
			if (payload.id > 0) {
				const { error } = await QuestionService.delete(payload)
				if (error) {
					commit('setError', { error })
					return
				}
			}
			commit('deleteQuestion', payload)
        },
        updateQuestion ({ state, commit }, { mId, SuId, SeId, question }) {
            console.log('____')
			if (!question || !mId) return
			if (!state.debouncers[question.id]) {
				commit('setDebouncer', { id: question.id, commit })
			}
			if (question.id < 0) {
				commit('updateList', { id: question.id, data: question })
			}
			commit('setIsSaved', { id: question.id })
			if (!question.name) { return }
			state.debouncers[question.id]({ mId, SuId, SeId, question })
		},
		setQuestion ({ state, commit }, { id } = {}) {
            if (id) {
                const data = state.questions.find(questions => questions.id === id)
                if (data && data.id === state.question.id) return
                commit('setQuestion', { data })
            } else {
                commit('setQuestion', {})
            }
		},
		resetError ({ commit }) {
			commit('setError', { error: undefined })
		},
		addNewQuestion ({ commit }, payload) {
			commit('addNewQuestion', payload)
		}
    }
}
