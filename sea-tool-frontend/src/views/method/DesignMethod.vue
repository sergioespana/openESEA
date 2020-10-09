<template>
	<v-row justify="center" class="fill-height">
		<v-col cols="11" lg="11" xl="11" class="fill-height">
			<div class="d-flex flex-column fill-height">
				<v-row :class="$style['content']" class="ma-0">
					<v-col :class="$style['list']" class="pa-0 ma-4">
						<method-form
							:method="method" class="mb-4"
							@input="updateMethod($event)"
						/>
						<div
							v-for="(topic, topicIndex) in items"
							:key="`topic-${topicIndex}`"
						>
							<topic-form
								ref="items"
								:topic="topic"
								:active="activeItem.objType === topic.objType
									&& activeItem.id === topic.id"
								class="mb-6"
								@input="saveActive('topic', $event)"
								@click.native="toggleActive(topic)"
							/>
							<template v-for="(topicChild, index) in topic.children">
								<component
									:is="`${topicChild.objType}-form`" ref="items"
									:key="`topicChild-${index}`"
									:topic="topicChild"
									:question="topicChild"
									:errors="errors[topicChild.objType]
										&& errors[topicChild.objType][topicChild.id]"
									:indirect-indicator="topicChild"
									:active="activeItem.objType === topicChild.objType
										&& activeItem.id === topicChild.id"
									class="mb-6"
									@input="saveActive(topicChild.objType, $event)"
									@click.native="toggleActive(topicChild)"
								/>
								<template v-for="(subTopicChild, index) in topicChild.children">
									<component
										:is="`${subTopicChild.objType}-form`"
										ref="items"
										:key="`subTopicChild-${index}`"
										:topic="subTopicChild"
										:question="subTopicChild"
										:indirect-indicator="subTopicChild"
										:active="activeItem.objType === subTopicChild.objType
											&& activeItem.id === subTopicChild.id"
										class="mb-6"
										@input="saveActive(subTopicChild.objType, $event)"
										@click.native="toggleActive(subTopicChild)"
									/>
								</template>
							</template>
							<v-divider :class="$style.divider" />
						</div>
						<v-btn color="primary" text @click="addTopic">
							<v-icon>mdi-plus</v-icon>
							<p class="ml-2 mb-0">
								Add new topic
							</p>
						</v-btn>
					</v-col>
					<v-col cols="auto" class="pa-4 pl-0">
						<v-card
							:class="$style.toolbar"
							:style="{ 'margin-top': toolbarTop }"
							width="64"
							class="d-flex flex-column align-center justify-center"
						>
							<v-btn text height="64" class="pa-0" @click="addQuestion">
								<div class="d-flex flex-column">
									<v-icon class="mt-1">
										mdi-plus
									</v-icon>
									<p class="caption text-lowercase font-regular mb-0 mt-1">
										Question
									</p>
								</div>
							</v-btn>
							<v-divider width="85%" />
							<v-btn text height="64" class="pa-0" @click="addSubTopic">
								<div class="d-flex flex-column">
									<v-icon class="mt-1">
										mdi-plus
									</v-icon>
									<p class="caption text-lowercase font-regular mb-0 mt-1">
										Subtopic
									</p>
								</div>
							</v-btn>
							<v-divider width="85%" />
							<v-btn
								text height="64" class="pa-0"
								@click="addIndirectIndicator"
							>
								<div class="d-flex flex-column">
									<v-icon class="mt-1">
										mdi-plus
									</v-icon>
									<p class="caption text-lowercase font-regular mb-0 mt-1">
										Calculation
									</p>
								</div>
							</v-btn>
							<v-divider width="85%" />
							<v-btn
								:disabled="topics.length <= 1"
								text height="64" class="pa-0"
								@click="deleteActive"
							>
								<div class="d-flex flex-column">
									<v-icon class="mt-1">
										mdi-delete-outline
									</v-icon>
									<p class="caption text-lowercase font-regular mb-0 mt-1">
										Delete
									</p>
								</div>
							</v-btn>
						</v-card>
					</v-col>
				</v-row>
			</div>
		</v-col>
	</v-row>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import MethodForm from '@/components/forms/MethodForm';
import TopicForm from '@/components/forms/TopicForm';
import QuestionForm from '@/components/forms/QuestionForm';
import CalculationForm from '@/components/forms/CalculationForm';
import AlertMessage from '@/components/general/AlertMessage';
import getMethodItems from '@/utils/getMethodItems';

export default {
	components: {
		MethodForm,
		TopicForm,
		QuestionForm,
		CalculationForm,
		AlertMessage,
	},
	data() {
		return {
			updateToolbar: 0,
		};
	},
	computed: {
		...mapState('organization', ['organization']),
		...mapState('method', ['method', 'error']),
		...mapState('topic', {
			topics: 'topics',
			activeTopic: 'topic',
			topicErrors: 'errors',
		}),
		...mapGetters('topic', ['methodTopics', 'subTopics']),
		...mapState('question', {
			activeQuestion: 'question',
			questionErrors: 'errors',
		}),
		...mapGetters('question', ['topicQuestions']),
		...mapState('indirectIndicator', {
			activeIndirectIndicator: 'indirectIndicator',
			indirectIndicatorErrors: 'errors',
		}),
		...mapGetters('indirectIndicator', ['topicIndirectIndicators']),
		activeItem() {
			let objType = 'topic';
			let { id } = this.activeTopic;

			if (this.activeQuestion.id) {
				objType = 'question';
				id = this.activeQuestion.id;
			}
			if (this.activeIndirectIndicator.id) {
				objType = 'calculation';
				id = this.activeIndirectIndicator.id;
			}
			return { objType, id };
		},
		toolbarTop() {
			let toolbarY = 0;
			let item;

			if (this.updateToolbar && this.activeItem && this.$refs.items) {
				item = this.$refs.items.find(i => i.active);
			}

			if (item) {
				toolbarY = item.$el.offsetTop;
			}
			return `${toolbarY}px`;
		},
		items() {
			return getMethodItems(
				this.methodTopics,
				this.subTopics,
				this.topicQuestions,
				this.topicIndirectIndicators,
			);
		},
		errors() {
			return {
				question: this.questionErrors,
				topic: this.topicErrors,
				calculation: this.indirectIndicatorErrors,
			};
		},
	},
	beforeRouteUpdate(to, from, next) {
		this.$route.params.id = to.params.id;
		this.initialize();
		next();
	},
	watch: {
		activeItem() {
			this.updateToolbar = 0;
			this.$nextTick(() => { this.updateToolbar = 1; });
		},
	},
	created() {
		this.initialize();
	},
	methods: {
		...mapActions('method', [
			'fetchMethod',
			'updateMethod',
			'saveMethod',
		]),
		...mapActions('topic', [
			'fetchTopics',
			'updateTopic',
			'addNewTopic',
			'deleteTopic',
			'setTopic',
		]),
		...mapActions('question', [
			'fetchQuestions',
			'setQuestion',
			'addNewQuestion',
			'deleteQuestion',
			'updateQuestion',
		]),
		...mapActions('indirectIndicator', [
			'fetchIndirectIndicators',
			'addNewIndirectIndicator',
			'updateIndirectIndicator',
			'setIndirectIndicator',
			'deleteIndirectIndicator',
		]),
		async initialize() {
			const methodId = parseInt(this.$route.params.id, 10);
			if (this.method.id !== methodId) {
				const { error } = await this.fetchMethod({
					id: methodId,
					oId: this.organization.id,
				});
				if (error) {
					this.$router.push({ name: 'methods' });
				}
			}
			await this.fetchTopics({
				oId: this.organization.id,
				mId: this.method.id,
			});
			await this.fetchQuestions({
				oId: this.organization.id,
				mId: this.method.id,
			});
			await this.fetchIndirectIndicators({
				oId: this.organization.id,
				mId: this.method.id,
			});
			this.toggleActive({ objType: 'topic' });
		},
		addTopic() {
			this.addNewTopic();
			this.setQuestion();
			this.setIndirectIndicator();
		},
		addSubTopic() {
			this.addNewTopic({
				parent: this.activeTopic.parent_topic || this.activeTopic.id,
			});
			this.setQuestion();
			this.setIndirectIndicator();
		},
		addQuestion() {
			this.addNewQuestion({ topic: this.activeTopic.id });
			this.setIndirectIndicator();
		},
		addIndirectIndicator() {
			this.addNewIndirectIndicator({ topic: this.activeTopic.id });
			this.setQuestion();
		},
		toggleActive(item) {
			const { objType } = item;
			const topic = { id: item.topic || item.id };
			this.setTopic(topic);
			if (objType === 'topic') {
				this.setQuestion();
				this.setIndirectIndicator();
			} else if (objType === 'question' && item.id !== this.activeQuestion.id) {
				this.setQuestion(item);
				this.setIndirectIndicator();
			} else if (
				objType === 'calculation'
				&& item.id !== this.activeIndirectIndicator.id
			) {
				this.setIndirectIndicator(item);
				this.setQuestion();
			}
		},
		saveActive(type, object) {
			if (type === 'topic') {
				this.updateTopic({
					oId: this.organization.id,
					mId: this.method.id,
					topic: object,
				});
			}
			if (type === 'question') {
				this.updateQuestion({
					oId: this.organization.id,
					mId: this.method.id,
					question: object,
				});
			}
			if (type === 'calculation') {
				this.updateIndirectIndicator({
					oId: this.organization.id,
					mId: this.method.id,
					indirectIndicator: object,
				});
			}
		},
		deleteActive() {
			const { objType, id } = this.activeItem;
			if (objType === 'topic') {
				this.deleteTopic({
					oId: this.organization.id,
					mId: this.method.id,
					id,
				});
			}
			if (objType === 'question') {
				this.deleteQuestion({
					oId: this.organization.id,
					mId: this.method.id,
					id,
				});
			}
			if (objType === 'calculation') {
				this.deleteIndirectIndicator({
					oId: this.organization.id,
					mId: this.method.id,
					id,
				});
			}
		},
	},
};
</script>

<style lang="scss" module>
.card {
  border-radius: 8px !important; // important used to overwrite vuetify
  border-width: 2px !important; // important used to overwrite vuetify
	border-style: solid;
}

.content {
	overflow-y: auto;
}

.list {
	position: relative;
}

.toolbar {
	transition: all 0.5s ease 0s;
}

.divider {
	margin: 64px 0;
}
</style>
