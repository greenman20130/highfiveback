import { FC } from 'react'
import AlarmingIndicators from './AlarmingIndicators/AlarmingIndicators'
import BurnoutLevel from './BurnoutLevel/BurnoutLevel'
import Calendar from './Calendar/Calendar'
import Notification from './Notification/Notification'
import styles from './Profile.module.css'
import Schedule from './Schedule/Schedule'
import Users from './Users/Users'

const Profile: FC = () => {
	return (
		<div className={styles.mainContainer}>
			<div className={styles.container}>
				<div className={styles.firstContainer}>
					<div className={styles.generalContainer}>
						<div className={styles.scheduleContainer}>
							<Schedule />
						</div>
						<div className={styles.usersContainer}>
							<Users />
						</div>
					</div>
					<div className={styles.notificationContainer}>
						<Notification />
					</div>
				</div>
				<div className={styles.secondContainer}>
					<div className={styles.image}></div>
					<div className={styles.burnoutLevel}>
						<BurnoutLevel />
					</div>
					<div className={styles.alarmingIndicators}>
						<AlarmingIndicators />
					</div>
					<div className={styles.redNotification}>
						У сотрудника стресс, давай напишем ему?
					</div>
					<div className={styles.calendarContainer}>
						<Calendar />
					</div>
				</div>
			</div>
		</div>
	)
}

export default Profile
