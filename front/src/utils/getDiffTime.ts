import { ITask } from '@/components/screens/profile/Schedule/Schedule'

export const getDiffTime = (data: ITask[]) => {
	const currentDate = new Date()
	if (data.length > 0) {
		const date = data[0].date
		const time = data[0].time
		const year = String(date).substring(0, 4)
		const month = String(date).substring(5, 7)
		const correctMonth = Number(month)
		const day = String(date).substring(8, 10)
		const hour = String(time).substring(0, 2)
		const minutes = String(time).substring(3, 5)
		const endDate = new Date(
			Number(year),
			correctMonth - 1,
			Number(day),
			Number(hour),
			Number(minutes)
		)
		const diff = currentDate.getTime() - endDate.getTime()
		const diffHours = diff / (1000 * 60 * 60)
		const diffRound = Math.round(diffHours)
		const absHours = Math.abs(diffRound)
		if (absHours <= 8) return true && absHours
	}
}
