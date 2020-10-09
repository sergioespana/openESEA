const getChildren = (topic, topicQuestions, topicIndirectIndicators) => {
	let children = [];
	if (topicQuestions[topic.id]) {
		children = topicQuestions[topic.id].map(question => ({
			...question,
			objType: 'question',
			showName: question.key,
			uniqueId: `question_${question.id}`,
		}));
	}
	if (topicIndirectIndicators[topic.id]) {
		children = [
			...children,
			...topicIndirectIndicators[topic.id].map(indirectIndicator => ({
				...indirectIndicator,
				objType: 'calculation',
				showName: indirectIndicator.name,
				uniqueId: `calculation_${indirectIndicator.id}`,
			})),
		];
	}

	return children;
};

export default (
	methodTopics, subTopics, topicQuestions, topicIndirectIndicators,
) => {
	if (!methodTopics.length) return [];
	return methodTopics.map((topic) => {
		let children = getChildren(
			topic,
			topicQuestions,
			topicIndirectIndicators,
		);

		if (subTopics[topic.id]) {
			const subTopicItems = subTopics[topic.id].map((subTopic) => {
				const subChildren = getChildren(
					subTopic,
					topicQuestions,
					topicIndirectIndicators,
				);

				return {
					...subTopic,
					objType: 'topic',
					showName: subTopic.name,
					uniqueId: `topic_${subTopic.id}`,
					children: subChildren,
				};
			});
			children = [...children, ...subTopicItems];
		}

		return {
			...topic,
			objType: 'topic',
			showName: topic.name,
			uniqueId: `topic_${topic.id}`,
			children,
		};
	});
};
