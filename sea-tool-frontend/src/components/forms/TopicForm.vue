<template>
	<v-card v-if="active" :style="cssProps" width="100%" outlined>
		<v-form ref="form" class="px-6 pt-2" @submit.prevent="save">
			<v-row dense>
				<v-col>
					<v-text-field
						ref="input"
						v-model="lazyTopic.name"
						:error-messages="nameErrors"
						:label="NameLabel"
						name="name"
						max="45"
						class="headline"
						height="45"
						@blur="updateName"
						@focus="$event.target.select()"
					/>
				</v-col>
			</v-row>
			<v-row v-if="!lazyTopic.parent_topic" dense>
				<v-col>
					<v-textarea
						v-model="lazyTopic.description"
						:error-messages="descriptionErrors"
						name="description"
						label="Topic description"
						rows="1"
						auto-grow
						@blur="updateDescription"
					/>
				</v-col>
			</v-row>
		</v-form>
	</v-card>
	<topic-card
		v-else
		:name="lazyTopic.name"
		:description="lazyTopic.description"
		:is-sub-topic="!isMainTopic"
	/>
</template>

<script>
import { isEqual } from 'lodash';
import HandleValidationErrors from '@/utils/HandleValidationErrors';
import { required, maxLength } from '@/utils/validators';
import TopicCard from '@/components/cards/TopicCard';

export default {
	components: {
		TopicCard,
	},
	props: {
		topic: {
			type: Object,
			required: true,
		},
		active: {
			type: Boolean,
			default: false,
		},
		errors: {
			type: Object,
			default: () => ({}),
		},
	},
	data() {
		return {
			lazyTopic: { ...this.topic },
		};
	},
	computed: {
		isMainTopic() {
			return !this.lazyTopic.parent_topic;
		},
		NameLabel() {
			return this.isMainTopic ? 'Topic name' : 'Sub topic name';
		},
		nameErrors() {
			return HandleValidationErrors(
				this.$v.lazyTopic.name,
				this.errors.name,
			);
		},
		descriptionErrors() {
			return HandleValidationErrors(
				this.$v.lazyTopic.description,
				this.errors.description,
			);
		},
		cssProps() {
			const props = {};
			if (this.active) {
				props['border-color'] = this.$vuetify.theme.currentTheme.primary;
			}
			return props;
		},
	},
	watch: {
		topic(val) {
			if (!isEqual(this.lazyTopic, val)) {
				this.lazyTopic = { ...val };
			}
		},
		lazyTopic: {
			deep: true,
			handler(val) {
				if (isEqual(this.topic, val)) return;
				this.$emit('input', val);
			},
		},
		active(val) {
			if (!val) {
				this.$v.$touch();
			} else {
				this.$nextTick(() => this.$refs.input && this.$refs.input.focus());
			}
		},
	},
	mounted() {
		if (!this.lazyTopic.name) {
			this.$refs.input.focus();
		}
	},
	created() {
		this.initialize();
	},
	methods: {
		initialize() {
			if (!this.lazyTopic.name) {
				const name = this.lazyTopic.parent_topic ? 'subtopic' : 'topic';
				this.lazyTopic.name = `Untitled ${name}`;
			}
		},
		updateName() {
			this.$v.lazyTopic.name.$touch();
		},
		updateDescription() {
			this.$v.lazyTopic.description.$touch();
		},
	},
	validations: {
		lazyTopic: {
			name: { required, maxLength: maxLength(120) },
			description: {},
		},
	},
};
</script>
