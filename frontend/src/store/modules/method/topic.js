import { debounce, random } from 'lodash'
import TopicService from '../../../services/TopicService'

const baseTopic = { name: 'untitled topic', description: '', questions: [] }

export default {
    namespaced: true,
    state: {
        topics: [],
        topic: [],
        error: undefined,
        debouncers: {},
        errors: {},
        isSaved: {}
    },
    getters: {
        getById: state => id => state.topics.filter(object => object.id === id),
        getErrorById: state => id => state.errors[id],
        methodTopics: state => state.topics.filter(topic => !topic.parent_topic),
        subTopics: (state) => {
            const subTopics = state.topics.filter(topic => topic.parent_topic)
            const filtered = {}
            subTopics.forEach((subTopic) => {
                if (!filtered[subTopic.parent_topic]) {
                    filtered[subTopic.parent_topic] = []
                }
                filtered[subTopic.parent_topic] = [
                    ...filtered[subTopic.parent_topic],
                    subTopic
                ]
            })
            return filtered
        }
    },
    mutations: {
        setTopics (state, { data }) {
			state.topics = data
			state.debouncers = {}
			state.errors = {}
			state.isSaved = {}
		},
        setTopic (state, { data }) {
            state.topic = data || {}
        },
        addNewTopic (state, { parent } = {}) {
            const topic = { ...baseTopic, id: random(-1000000, -1) }
            topic.parent_topic = parent
            state.topics.push(topic)
            state.topic = topic
        },
        deleteTopic (state, { id }) {
            delete state.debouncers[id]
            delete state.errors[id]
            delete state.isSaved[id]
            state.topics = state.topics.filter(t => t.id !== id)
        },
        setError (state, { error, id }) {
            console.log(error?.response?.data)
            if (id) {
                state.errors = { ...state.errors, [id]: error?.response?.data || {} }
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

			state.topics = state.topics.map((item) => {
				if (item.id !== id) return item
				return Object.assign(item, data)
			})
		},
        setDebouncer (state, { id, commit }) {
			state.debouncers[id] = debounce(
				async ({ mId, topic }) => {
					const method = topic.id > 0 ? 'put' : 'post'
                    // topics.direct_indicators.forEach(indicator => { })
                    // if (topic.direct_indicator.length) {
                    //     question.direct_indicator = [question.direct_indicator[0].id] || []
                    // }
					const { response, error } = await TopicService[method](
						{ mId, id, data: topic }
					)
					if (error) {
						commit('setError', { error, id: topic.id })
						return
					}
					commit('setError', { errors: {}, id: topic.id })
					commit('setIsSaved', { id: topic.id, isSaved: true })
					commit('updateList', { id: topic.id, data: response.data })
				},
				1000
			)
		},
		resetTopics (state) {
			state.topics = []
		},
		setIsSaved (state, { id, isSaved = false }) {
			if (id) {
				state.isSaved = {
					...state.isSaved,
					[id]: isSaved
				}
			}
		}
    },
    actions: {
        async fetchTopics ({ commit }, payload) {
            const { response, error } = await TopicService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setTopics', response)
        },
        addNewTopic ({ commit }, payload) {
            commit('addNewTopic', payload)
        },
        async createTopic ({ commit, dispatch }, { mId, parent = null }) {
            const data = { ...baseTopic, parent_topic: parent }
            const { response, error } = await TopicService.post({ mId, data: data })
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchTopics', { mId: mId })
            await commit('setTopic', response)
        },
        async updateTopic ({ state, commit }, { mId, topic }) {
            if (!topic || !mId) { return }
            if (!state.debouncers[topic.id]) {
                commit('setDebouncer', { id: topic.id, commit })
            }
            commit('setIsSaved', { id: topic.id })
            await state.debouncers[topic.id]({ mId, topic })
        },
        async patchTopic ({ commit }, { mId, id, data }) {
            const { response, error } = await TopicService.patch({ mId: mId, id: id, data: data, headers: { 'Content-Type': 'application/json' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateList', { id: id, data: response.data })
            commit('setTopic', response)
        },
        async deleteTopic ({ commit }, payload) {
            if (payload.id > 0) {
                const { error } = await TopicService.delete(payload)
                if (error) {
                    commit('setError', { error })
                    return
                }
            }
            commit('deleteTopic', payload)
        },
        setTopic ({ state, commit }, { id } = {}) {
            const data = state.topics.find(topic => topic.id === id)
            if (data && data.id === state.topic.id) { return }
            commit('setTopic', { data })
        },
        resetError ({ commit }) {
            commit('setError', { error: undefined })
        },
        resetTopics ({ commit }) {
            commit('resetTopics')
        }
    }
}
