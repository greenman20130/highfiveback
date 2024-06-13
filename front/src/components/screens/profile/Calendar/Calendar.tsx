import { endOfWeek, isWithinInterval, startOfWeek } from 'date-fns'
import { ru } from 'date-fns/locale'
import { FC } from 'react'
import { DayPicker, Row, RowProps } from 'react-day-picker'

import 'react-day-picker/dist/style.css'

function CurrentWeekRow(props: RowProps) {
	const isDateInCurrentWeek = (dateToCheck: Date) => {
		const today = new Date()
		const start = startOfWeek(today)
		const end = endOfWeek(today)
		return isWithinInterval(dateToCheck, { start, end })
	}
	const isNotCurrentWeek = props.dates.every(date => !isDateInCurrentWeek(date))
	if (isNotCurrentWeek) return <></>
	return <Row {...props} />
}

const Calendar: FC = () => {
	return (
		<DayPicker
			components={{ Row: CurrentWeekRow }}
			showOutsideDays
			locale={ru}
			mode='single'
			disableNavigation={true}
		/>
	)
}

export default Calendar
