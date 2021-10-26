const getChildren = (topic, topicDirectIndicators, topicIndirectIndicators) => {
    let children = []
    if (topicDirectIndicators[topic.id]) {
        children = topicDirectIndicators[topic.id].map(directIndicator => ({
            ...directIndicator,
            objType: 'direct-indicator',
            showName: directIndicator.name,
            uniqueId: `indicator${directIndicator.id}`
        }))
    }
    if (topicIndirectIndicators[topic.id]) {
        children = [
            ...children,
            ...topicIndirectIndicators[topic.id].map(indirectIndicator => ({
                ...indirectIndicator,
                objType: 'indirect-indicator',
                showName: indirectIndicator.name,
                uniqueId: `calculation_${indirectIndicator.id}`
            }))
        ]
    }
    return children
}

export default (
    methodTopics, subTopics, topicDirectIndicators, topicIndirectIndicators
) => {
    if (!methodTopics.length) return []
    return methodTopics.map((topic) => {
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
    })
}
