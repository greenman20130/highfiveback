import { FC } from 'react'
import DoughnutBurnoutChart from '../Doughnut/DoughnutBurnoutChart'
import styles from '../Profile.module.css'

const BurnoutLevel: FC = () => {
	return (
		<>
			<div className={styles.burnoutLevelText}>
				<p>Мой уровень выгорания</p>
				<p style={{ marginTop: '60px', opacity: '0.4' }}>
					Пройти тест повторно можно здесь
				</p>
			</div>
			<div className={styles.burnoutLevelChart}>
				<DoughnutBurnoutChart />
			</div>
		</>
	)
}

export default BurnoutLevel
