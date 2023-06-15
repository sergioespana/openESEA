function createElement (parent, elementName, elementOptions) {
    var element = document.createElement(elementName)
    for (var key in elementOptions) {
        element[key] = elementOptions[key]
    }
    parent.appendChild(element)
    return element
}

export default createElement
