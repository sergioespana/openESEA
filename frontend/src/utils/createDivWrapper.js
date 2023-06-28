import { createApp, h } from 'vue'

function createDivWrapper (parent, type, data = {}, div_options = {}) {
    var ComponentApp = createApp({
        setup () {
            return () => h(type, data)
        }
    })
    var wrapper = document.createElement('div', div_options)
    ComponentApp.mount(wrapper)
    parent.appendChild(wrapper)
    return wrapper
}
// mountVueComponent
// function createDivWrapper (parent, component) {
//     const app = createApp({
//       setup () {
//         return () => h(component)
//       }
//     })
//     app.mount(parent)
//   }

export default createDivWrapper
