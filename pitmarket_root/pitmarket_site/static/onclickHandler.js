for (let row of document.getElementsByClassName('listing-table')[0].getElementsByTagName('tbody')[0].getElementsByClassName('listing-row')) {
	row.onclick = (e) => {
		if (e.target.tagName == 'TD') {
			window.location.href = row.getAttribute('data-url');
		}
	}
}