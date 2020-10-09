const API_URL = `${process.env.VUE_APP_BASE_URL}/api`;
const MEDIA_URL = `${process.env.VUE_APP_BASE_URL}/media`;
const STATUS = {
	IDLE: 'idle',
	IN_PROGRESS: 'in progress',
	LOADING: 'Loading',
	ERROR: 'Error',
	SUCCESS: 'Success',
};
const QUESTION_TYPES = {
	TEXT: 'TEXT',
	NUMBER: 'NUMBER',
	RADIO: 'RADIO',
	CHECKBOX: 'CHECKBOX',
};

export { STATUS, API_URL, MEDIA_URL, QUESTION_TYPES };
