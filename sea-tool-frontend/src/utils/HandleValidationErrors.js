const validationErrors = Object.entries({
	required: 'This field is required.',
	email: 'This email address is invalid.',
	strongPassword: 'atleast one number and special character are required.',
	sameAsPassword: 'The passwords do not match.',
	maxLength: 'This field is too long',
});

export default (validationObject, serverValidationErrors = []) => {
	const errors = [];
	if (validationObject.$dirty) {
		validationErrors.forEach(([errorName, errorText]) => {
			if (errorName in validationObject && !validationObject[errorName]) {
				errors.push(errorText);
			}
		});
	}
	if (serverValidationErrors && serverValidationErrors.length) {
		serverValidationErrors.forEach(
			validationError => errors.push(validationError),
		);
	}
	return errors;
};
