import { FC } from 'react'
import DoughnutAlarmingChart from '../Doughnut/DoughnutAlarmingChart'
import styles from '../Profile.module.css'

const AlarmingIndicators: FC = () => {
	return (
		<>
			<div className={styles.alarmingIndicatorsText}>
				<p>Тревожные показатели</p>
				<p style={{ marginTop: '70px', opacity: '0.4' }}>
					Backend разработчики
				</p>
			</div>
			<div className={styles.alarmingIndicatorsChart}>
				<DoughnutAlarmingChart />
			</div>
		</>
	)
}

export default AlarmingIndicators
