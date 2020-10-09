export const firstValidIndex = (list, index) => {
	if (!list.length) {
		return -1;
	}
	const checkIndex = (currIndex) => {
		if (!list[currIndex]) {
			return checkIndex(currIndex - 1);
		}
		return currIndex;
	};
	return checkIndex(index);
};

export const getRequestData = (data) => {
	const formData = new FormData();
	Object.entries(data).forEach(([key, value]) => {
		if (key === 'image' && (!value || typeof value === 'string')) {
			return;
		}

		formData.append(`${key}`, value);
	});

	return formData;
};
