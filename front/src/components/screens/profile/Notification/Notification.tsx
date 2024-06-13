import { FC } from 'react'
import styles from '../Profile.module.css'

const Notification: FC = () => {
	const currentDate = new Date()
	currentDate.setDate(currentDate.getDate() + 7)
	return (
		<>
			<div className={styles.header}>Напоминание</div>
			<div className={styles.text}>
				Опрос сотрудников заканчивается через неделю,{' '}
				{currentDate.toLocaleDateString()}
				<br />
				На данный момент 9 человек еще не прошли опрос
			</div>
		</>
	)
}

export default Notification
