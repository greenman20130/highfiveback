export const getDateOnly = () => {
	const date = new Date().toLocaleString()
	const dateOnly = String(date).substring(0, 10)
	return dateOnly
}
