export const getRequestData = (data) => {
    const formData = new FormData()
    Object.defineProperties(data).forEach(([key, value]) => {
        formData.append(`${key}`, value)
    })
    return formData
}
