<template>
	<v-navigation-drawer :style="navigation" clipped app permanent width="320px">
		<p class="title font-weight-bold mx-4 my-5">
			Indicator library
		</p>

		<v-treeview
			:items="items"
			:active.sync="activeItem"
			:open.sync="itemsOpen"
			activatable
			item-key="uniqueId"
			expand-icon="mdi-chevron-down"
		>
			<template v-slot:label="{ item }">
				<p class="mb-0">
					<v-icon v-if="item.uniqueId.includes('calculation')">
						mdi-calculator
					</v-icon>
					{{ item.showName || item.name }}
				</p>
			</template>
			<template v-slot:append="{ item }">
				<v-icon
					v-if="item.objType === 'question' && activeIndirectIndicator.id"
					:style="{ ['z-index']: 1000000 }"
					@click.stop="addToCalculation(item)"
				>
					mdi-arrow-right
				</v-icon>
			</template>
		</v-treeview>
	</v-navigation-drawer>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';
import getMethodItems from '@/utils/getMethodItems';

export default {
	data() {
		return {
			itemsOpen: [],
		};
	},
	computed: {
		...mapState('organization', ['organization']),
		...mapState('method', ['method']),
		...mapState('topic', { activeTopic: 'topic' }),
		...mapState('question', { activeQuestion: 'question' }),
		...mapState('indirectIndicator', {
			activeIndirectIndicator: 'indirectIndicator',
		}),
		...mapGetters('topic', ['methodTopics', 'subTopics']),
		...mapGetters('question', { topicQuestions: 'topicQuestions' }),
		...mapGetters('indirectIndicator', ['topicIndirectIndicators']),
		items() {
			return getMethodItems(
				this.methodTopics,
				this.subTopics,
				this.topicQuestions,
				this.topicIndirectIndicators,
			);
		},
		activeItem: {
			get() {
				if (this.activeQuestion.id) {
					return [`question_${this.activeQuestion.id}`];
				}
				if (this.activeIndirectIndicator.id) {
					return [`calculation_${this.activeIndirectIndicator.id}`];
				}
				return [`topic_${this.activeTopic.id}`];
			},
			set(val) {
				if (val.length) {
					this.setActiveItem(val[0]);
				}
			},
		},
		navigation() {
			return {
				'border-color': this.$vuetify.theme.parsedTheme.secondary.lighten5,
			};
		},
	},
	watch: {
		activeItem() {
			if (this.activeQuestion.id) {
				this.itemsOpen.push(`topic_${this.activeQuestion.topic}`);
			}
			if (this.activeIndirectIndicator.id) {
				this.itemsOpen.push(`topic_${this.activeIndirectIndicator.topic}`);
			}
			if (this.activeTopic.parent_topic) {
				this.itemsOpen.push(`topic_${this.activeTopic.parent_topic}`);
			}
		},
	},
	methods: {
		...mapActions('topic', ['setTopic']),
		...mapActions('question', ['setQuestion']),
		...mapActions('indirectIndicator', [
			'setIndirectIndicator',
			'updateIndirectIndicator',
		]),
		setActiveItem(active) {
			const [type, id] = active.split('_');
			const parsedId = parseInt(id, 10);
			if (type === 'topic') {
				this.setTopic({ id: parsedId });
				this.setQuestion();
				this.setIndirectIndicator();
			} else if (type === 'question') {
				this.setQuestion({ id: parsedId });
				this.setIndirectIndicator();
			} else if (type === 'calculation') {
				this.setIndirectIndicator({ id: parsedId });
				this.setQuestion();
			}
		},
		addToCalculation(item) {
			this.updateIndirectIndicator({
				oId: this.organization.id,
				mId: this.method.id,
				indirectIndicator: {
					...this.activeIndirectIndicator,
					formula: `${this.activeIndirectIndicator.formula} [${item.key}]`,
				},
			});
		},
	},
};
</script>
