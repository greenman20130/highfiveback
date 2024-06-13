import { FC } from 'react'
import DoughnutChart from './DoughnutChart'
import styles from './GeneralInfo.module.css'

const GeneralInfo: FC = () => {
	return (
		<>
			<div className={styles.mainContainer}>
				<div className={styles.container}>
					<div className={styles.gridContainerMain}>
						<div className={styles.box1}>
							<span className={styles.header}>
								Опросник на выгорание MBI, адаптирован Н.Е. Водопьяновой
							</span>
							<span className={styles.subHeader}>
								Это инструмент, предназначенный для диагностики синдрома
								эмоционального выгорания (СЭВ) у работающих людей. Опросник
								является ценным инструментом для оценки профессионального
								выгорания и разработки мер по его профилактике и коррекции.
							</span>
						</div>
						<div className={styles.box2}>
							<span className={styles.header}>Цель опросника:</span>
							<span className={styles.subHeader}>
								Определить уровень СЭВ и анализ ключевых компонентов:
								<ul className={styles.list}>
									<li>Эмоциональное истощение</li>
									<li>Деперсонализация</li>
									<li>Редукция профессиональных достижений</li>
								</ul>
							</span>
						</div>
						<div className={styles.box3}>
							<span className={styles.header}>Интерпретация результатов:</span>
							<span className={styles.subHeader}>
								Чем больше баллов по шкале, тем сильнее выражен компонент
								выгорания. Сумма баллов по всем шкалам определяет тяжесть общего
								состояния.
							</span>
						</div>
						<div className={styles.box4}>
							<span className={styles.header}>Истощение эмоциональное</span>
							<ul className={styles.list}>
								<li>Снижение настроения</li>
								<li>Быстрая утомляемость</li>
								<li>Раздражительность</li>
								<li>Равнодушие</li>
								<li>Потеря интереса к работе</li>
								<li>Чувство "пресыщения" работой</li>
							</ul>
						</div>
						<div className={styles.box5}>
							<span className={styles.header}>
								Деперсонализация (профессиональная)
							</span>
							<ul className={styles.list}>
								<li>Отстраненность</li>
								<li>Быстрая утомляемость</li>
								<li>Безразличие к работе</li>
								<li>Формальное выполнение обязанностей</li>
								<li>Отсутствие сопереживания</li>
								<li>Раздражительность, цинизм</li>
								<li>Высокомерие, сленг, ярлыки</li>
							</ul>
						</div>
						<div className={styles.box6}>
							<span className={styles.header}>
								Редукция профессиональных достижений
							</span>
							<ul className={styles.list}>
								<li>Негативная оценка себя и своих результатов</li>
								<li>Снижение мотивации</li>
								<li>Перекладывание обязанностей</li>
								<li>Изоляция, отстраненность</li>
								<li>Избегание работы</li>
							</ul>
						</div>
					</div>
					<div className={styles.gridContainerSide}>
						<div className={styles.box7}>
							<span className={styles.opacityText}>Дата проведения</span>
							<span className={styles.date}>10.01.2023 - 29.01.2023</span>
							<div className={styles.textContainer}>
								<div className={styles.section1}>
									<span className={styles.opacityText}>Участники</span>
									<span className={styles.date}>19/20</span>
								</div>
								<div className={styles.section2}>
									<span className={styles.opacityText}>Вопросы</span>
									<span className={styles.date}>22</span>
								</div>
							</div>
						</div>
						<div className={styles.box8}>
							<DoughnutChart />
						</div>
						<div className={styles.box9}>
							<span className={styles.header}>Важно</span>
							<br />
							<span>
								Опросник не является заменой индивидуальной консультации
								психолога
							</span>
							<br />
							<span>Выгорание — не приговор, с ним можно справиться!</span>
						</div>
					</div>
				</div>
			</div>
		</>
	)
}

export default GeneralInfo
