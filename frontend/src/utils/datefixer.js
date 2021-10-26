import moment from 'moment'

// format example: MM/DD/YYYY/ hh:mm
function dateFixer (value, format) {
    if (value) {
        if (format) {
            return moment(String(value)).format(format)
        }
        return moment(String(value)).format('MM/DD/YYYYY')
    }
}

export default dateFixer
