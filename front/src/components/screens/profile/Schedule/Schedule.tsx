import cn from 'classnames'
import { FC, useState } from 'react'
import closeBtn from '../../../../assets/icons/cross.svg'
import { getCurrentDate } from '../../../../utils/getCurrentDate'
import { getDiffTime } from '../../../../utils/getDiffTime'
import styles from '../Profile.module.css'
import ModalScheduleMenu from './ModalScheduleMenu'

export interface ITask {
	id: number
	text: string
	time: string
	date: Date
	isChecked: boolean
}

const Schedule: FC = () => {
	const [style, setStyle] = useState('headerNotificationContainer')
	const [data, setData] = useState<ITask[]>([])
	const [notificationData, setNotificationData] = useState<ITask[]>([])
	const addTask = (data: ITask) => {
		setData((prevData) => [...prevData, data])
		if (data.isChecked) {
			setNotificationData([data])
			if (style !== 'headerNotificationContainer')
				setStyle('headerNotificationContainer')
		}
	}
	const removeNotification = () => {
		setStyle('removed')
	}

	const hourWord = (data: ITask[]) => {
		const result = getDiffTime(data)
		console.log(result)
		if (typeof result === 'number') {
			if (result === 1) return 'час'
			if ([5, 6, 7, 8].includes(result)) return 'часов'
			return 'часа'
		}
	}

	return (
		<>
			{getDiffTime(notificationData) && notificationData[0].isChecked && (
				<div
					className={cn({
						[styles.headerNotificationContainer]:
							style === 'headerNotificationContainer',
						[styles.removed]: style === 'removed',
					})}
				>
					<div className={styles.headerNotification}>
						<button
							className={styles.closeBtnNotification}
							onClick={removeNotification}
						>
							<img src={closeBtn} width={7} height={7} />
						</button>
						<span>
							{notificationData.length > 0
								? notificationData[0].isChecked
									? notificationData[0].text +
									  ' ' +
									  'через' +
									  ' ' +
									  getDiffTime(notificationData) +
									  ' ' +
									  hourWord(notificationData)
									: ''
								: ''}
						</span>
					</div>
				</div>
			)}

			<div className={styles.schedule}>
				<div className={styles.scheduleDateContainer}>
					<div className={styles.scheduleDate}>{getCurrentDate()}</div>
					<ModalScheduleMenu onChange={addTask} />
				</div>
				<div className={styles.scheduleList}>
					{data.length > 0 ? (
						data.map((item) => (
							<div key={item.id} className={styles.scheduleItem}>
								<div
									className={
										item.isChecked
											? styles.scheduleListBorderImportant
											: styles.scheduleListBorder
									}
								>
									<div className={styles.infoContainer}>
										<div className={styles.scheduleItemName}>{item.text}</div>
										<div className={styles.scheduleItemTime}>{item.time}</div>
									</div>
								</div>
							</div>
						))
					) : (
						<div className={styles.noTaskMessage}>На сегодня задач нет</div>
					)}
				</div>
			</div>
		</>
	)
}

export default Schedule
