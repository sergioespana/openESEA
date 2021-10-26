const getChildren = (topic, topicDirectIndicators, topicIndirectIndicators) => {
    let children = []
    if (topicDirectIndicators[topic.id]) {
        children = topicDirectIndicators[topic.id].map(directIndicator => ({
            ...directIndicator,
            objType: 'indicator',
            showName: directIndicator.name,
            uniqueId: `indicator_${directIndicator.id}`
        }))
    }
    if (topicIndirectIndicators[topic.id]) {
        children = [
            ...children,
            ...topicIndirectIndicators[topic.id].map(indirectIndicator => ({
                ...indirectIndicator,
                objType: 'calculation',
                showName: indirectIndicator.name,
                uniqueId: `calculation_${indirectIndicator.id}`
            }))
        ]
    }
    return children
}

export default (currentTopic, subTopics, topicDirectIndicators, topicIndirectIndicators) => {
    const topic = currentTopic
    if (!topic) return {}

    let children = getChildren(
        topic,
        topicDirectIndicators,
        topicIndirectIndicators
    )
    if (subTopics[topic.id]) {
        const subTopicItems = subTopics[topic.id].map(subTopic => {
            const subChildren = getChildren(
                subTopic,
                topicDirectIndicators,
                topicIndirectIndicators
            )
            return {
                ...subTopic,
                objType: 'topic',
                showName: subTopic.name,
                uniqueId: `topic_${subTopic.id}`,
                children: subChildren
            }
        })
        children = [...children, ...subTopicItems]
    }

    return {
        ...topic,
        objType: 'topic',
        showName: topic.name,
        uniqueId: `topic_${topic.id}`,
        children
    }
}
