const API_URL = process.env.VUE_APP_ROOT_API // process.env.baseURL || process.env.apiUrl ||
const NETWORK_ROLES = {
    NETWORK_ADMIN: 'network admin',
    GUEST: 'guest'
}
const STATUS = {
    IDLE: 'idle',
    IN_PROGRESS: 'in progress',
    LOADING: 'Loading',
    ERROR: 'Error',
    SUCCESS: 'Succes'
}
const QUESTION_TYPES = { // can be removed in the future
    TEXT: 'TEXT',
	NUMBER: 'NUMBER',
	RADIO: 'RADIO',
	CHECKBOX: 'CHECKBOX'
}
const DATA_TYPES = [
    { text: 'TEXT', value: 'text', possibleUI: ['field', 'line', 'textbox'] },
    { text: 'INTEGER', value: 'integer', possibleUI: ['field'] },
    { text: 'DOUBLE', value: 'double', possibleUI: ['field'] },
    { text: 'DATE', value: 'date', possibleUI: ['field'] },
    { text: 'BOOLEAN', value: 'boolean', possibleUI: ['radiobutton', 'dropdown'] },
    { text: 'SINGLE CHOICE', value: 'singlechoice', possibleUI: ['radiobutton', 'dropdown'] },
    { text: 'MULTIPLECHOICE', value: 'multiplechoice', possibleUI: ['checkbox'] }
    ]
const UI_COMPONENTS = [
    { text: 'FIELD', value: 'field', possibleDataTypes: ['text', 'integer', 'double', 'date'] },
    { text: 'LINE', value: 'line', possibleDataTypes: ['text'] },
    { text: 'TEXTBOX', value: 'textbox', possibleDataTypes: ['text'] },
    { text: 'CHECKBOX', value: 'checkbox', possibleDataTypes: ['multiplechoice'] },
    { text: 'RADIOBUTTON', value: 'radiobutton', possibleDataTypes: ['boolean', 'singlechoice'] },
    { text: 'DROPDOWN', value: 'dropdown', possibleDataTypes: ['boolean', 'msinglechoice'] }
    // { text: 'FIELD', value: 'field', possibleDataType: ['field', 'line', 'textbox'] },
    // FIELD: 'field',
    // LINE: 'line',
    // TEXTBOX: 'textbox',
    // DROPDOWN: 'dropdown',
    // RADIOBUTTON: 'radiobutton',
    // CHECKBOX: 'checkbox'
]
const RESPONSE_TYPE = {
    MULTIPLE: 'multiple',
    SINGLE: 'single'
}

export { NETWORK_ROLES, STATUS, API_URL, QUESTION_TYPES, DATA_TYPES, UI_COMPONENTS, RESPONSE_TYPE }
