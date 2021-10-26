async function imageValidator (event) {
    try {
        console.log(event.target.files[0])
    } catch {
        console.log('undefined event')
        return false
    }

    var img = new Image()

    img.onload = await function () {
        if (event.target.files[0].size > 1000000) {
            alert('The selected image file is too big. Please choose one that is smaller than 1MB.')
            return false
        }
        if (this.width > 1000 || this.height > 1000) {
            alert('The selected image is too big. Please choose one with maximum dimensions of 1000x1000')
            return false
        }
        return true
    }

    img.onerror = function () {
        alert('not a valid file: ' + event.target.files[0].type)
    }

    img.src = URL.createObjectURL(event.target.files[0])

    if (img.onload()) {
        return event.target.files[0]
    }
    return false
}

export default imageValidator

            // var img = new Image()

            // img.onload = await function () {
            //     if (e.target.files[0].size > 1000000) {
            //         alert('The selected image file is too big. Please choose one that is smaller than 1MB.')
            //         return false
            //     }
            //     if (this.width > 1000 || this.height > 1000) {
            //         console.log(this.width, ' x ', this.height)
            //         alert('The selected image is too big. Please choose one with maximum dimensions of 1000x1000.')
            //        return false
            //     }
            //     return true
            // }
            // img.onerror = function () {
            //     alert('not a valid file: ' + e.target.files[0].type)
            // }
            // img.src = URL.createObjectURL(e.target.files[0])

            // if (img.onload()) {
            //     console.log('correct image:', e.target.files[0].name)
            //     this.file = e.target.files[0]
            // }
