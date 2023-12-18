const getChildren = (section, sectionQuestions) => {
    let children = []
    console.log(section, sectionQuestions)
    if (sectionQuestions[section.id]) {
        children = sectionQuestions[section.id].map(question => ({
            ...question,
            objType: 'question',
            showName: question.name,
            uniqueId: `question_${question.id}`
        }))
    }
    return children
}

export default (methodSections, sectionQuestions) => {
    if (!methodSections) return []
    return methodSections.map((section) => {
        const children = getChildren(section, sectionQuestions)

    return {
        ...section,
        objType: 'section',
        showName: section.name,
        uniqueId: `section_${section.id}`,
        children
    }
    })
}
