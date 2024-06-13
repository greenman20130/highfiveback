export function getCurrentDate() {
	const date = new Date()
	const month = date.getMonth()
	const monthNames = [
		'января',
		'февраля',
		'марта',
		'апреля',
		'мая',
		'июня',
		'июля',
		'августа',
		'сентября',
		'ноября',
		'декабря',
	]
	const days = ['ВС', 'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']

	return (
		days[date.getDay()] + ',' + ' ' + date.getDate() + ' ' + monthNames[month]
	)
}
