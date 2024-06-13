import { FC } from 'react'
import DoughnutGenderChart from './DoughnutGenderChart'
import HorizontalBarChart from './HorizontalBarChart'
import styles from './Profiles.module.css'

const Profiles: FC = () => {
	return (
		<>
			<div className={styles.mainContainer}>
				<div className={styles.firstContainer}>
					<div className={styles.textBox}>
						<span className={styles.opacityHeader}>
							Количество сотрудников, испытывающих выгорание по филиалам
						</span>
					</div>
					<div className={styles.citiesContainer}>
						<div className={styles.cityBox}>
							<span className={styles.number}>40</span>
							<span className={styles.text}>Самара</span>
						</div>
						<div className={styles.cityBox}>
							<span className={styles.number}>88</span>
							<span className={styles.text}>Москва</span>
						</div>
						<div className={styles.cityBox}>
							<span className={styles.number}>60</span>
							<span className={styles.text}>Казань</span>
						</div>
					</div>
					<div className={styles.textBox}>
						<span className={styles.opacityHeader}>
							Количество сотрудников, испытывающих выгорание по должности
						</span>
					</div>
					<div className={styles.staffContainer}>
						<div className={styles.staffBox}>
							<span className={styles.number}>2</span>
							<span className={styles.text}>Руководитель</span>
						</div>
						<div className={styles.staffBox}>
							<span className={styles.number}>5</span>
							<span className={styles.text}>Менеджер</span>
						</div>
						<div className={styles.staffBox}>
							<span className={styles.number}>34</span>
							<span className={styles.text}>Педагог</span>
						</div>
					</div>
					<div className={styles.textBox}>
						<span className={styles.opacityHeader}>Статистика по возрасту</span>
					</div>
					<div className={styles.ageStatsContainer}>
						<HorizontalBarChart />
					</div>
				</div>
				<div className={styles.secondContainer}>
					<div className={styles.textBox}>
						<span className={styles.opacityHeader}>Статистика по полу</span>
					</div>
					<div className={styles.genderStatsContainer}>
						<DoughnutGenderChart />
					</div>
					<div className={styles.textBox}>
						<span className={styles.opacityHeader}>
							Количество сотрудников, испытывающих конкретную фазу выгорания
						</span>
					</div>
					<div className={styles.phaseStatsContainer}>
						<div className={styles.phaseBox}>
							<span className={styles.number}>22</span>
							<span className={styles.text}>Эмоциональное истощение</span>
						</div>
						<div className={styles.phaseBox}>
							<span className={styles.number}>34</span>
							<span className={styles.text}>
								Редукция профессиональных достижений
							</span>
						</div>
						<div className={styles.phaseBox}>
							<span className={styles.number}>5</span>
							<span className={styles.text}>Деперсонализация</span>
						</div>
					</div>
				</div>
			</div>
		</>
	)
}

export default Profiles
