export const getRightDate = (date: string) => {
	const year = String(date).substring(0, 4)
	const month = String(date).substring(5, 7)
	const day = String(date).substring(8, 10)
	return `${day}.${month}.${year}`
}
