import { Modal } from '@mui/material'
import { FC, useState } from 'react'
import closeBtn from '../../../../assets/icons/cross.svg'
import styles from './Result.module.css'

interface IResult {
	result: string
	isOpen: boolean
	points: {
		'Эмоциональное истощение': number
		'Редукция личных достижений': number
		Деперсонализация: number
	}
}

const totalPoints = (
	firstPoint: number,
	secondPoint: number,
	thirdPoint: number
) => {
	return firstPoint + secondPoint + thirdPoint
}

const Result: FC<IResult> = ({ result, points, isOpen }) => {
	const [modalOpen, setModalOpen] = useState(isOpen)
	const handleClose = () => {
		setModalOpen(false)
		location.reload()
	}
	return (
		<Modal
			sx={{
				'& div.MuiModal-backdrop': {
					backgroundColor: 'rgba(255, 255, 255, 0.5)',
				},
			}}
			open={modalOpen}
			onClose={handleClose}
		>
			<div className={styles.modalContainer}>
				<div className={styles.modalHeaderContainer}>
					<div className={styles.modalHeading}>Рекомендации опроса</div>
					<button className={styles.closeBtn} onClick={handleClose}>
						<img width={20} height={20} src={closeBtn} />
					</button>
				</div>
				<div className={styles.modalContent}>
					<div className={styles.headerContent}>
						<div className={styles.levelOfBurnout}>
							Уровень выгорания:{' '}
							<span style={{ color: '#D15541' }}>{result}</span>
						</div>
						<div className={styles.result}>
							Результат:{' '}
							<span style={{ color: '#D15541' }}>
								{totalPoints(
									points['Эмоциональное истощение'],
									points['Редукция личных достижений'],
									points.Деперсонализация
								)}{' '}
							</span>
							из 15 баллов
						</div>
						<div className={styles.confidentiality}>
							Конфиденциальность: Анонимно
						</div>
					</div>
					<div className={styles.statisticsContent}>
						<div className={styles.attritionLevel}>
							<div className={styles.header}>
								1. Ваш уровень эмоционального истощения{' '}
								{points['Эмоциональное истощение']} баллов из 5
							</div>
							<div className={styles.span}>
								Проявляется в снижении эмоционального тонуса, повышенной
								психической истощаемости и аффективной лабильности, равнодушием,
								неспособностью испытывать сильные эмоции, как положительные, так
								и отрицательные, утраты интереса и позитивных чувств к
								окружающим, ощущении «пресыщенности» работой,
								неудовлетворенностью жизнью в целом.
							</div>
						</div>
						<div className={styles.reduction}>
							<div className={styles.header}>
								2. Ваш уровень редукции личных достижений{' '}
								{points['Редукция личных достижений']} баллов из 5
							</div>
							<div className={styles.span}>
								Проявляется в негативном оценивании себя, результатов своего
								труда и возможностей для профессионального развития. Высокое
								значение этого показателя отражает тенденцию к негативной оценке
								своей компетентности и продуктивности и, как следствие, снижение
								профессиональной мотивации, нарастание негативизма в отношении
								служебных обязанностей, в лимитировании своей вовлеченности в
								профессию за счет перекладывания обязанностей и ответственности
								на других людей, к изоляции от окружающих, отстраненность и
								неучастие, избегание работы сначала психологически, а затем
								физически.
							</div>
						</div>
						<div className={styles.depersonalization}>
							<div className={styles.header}>
								3. Ваш уровень деперсонализации {points.Деперсонализация} баллов
								из 5
							</div>
							<div className={styles.span}>
								Проявляется в эмоциональном отстранении и безразличии,
								формальном выполнении профессиональных обязанностей без
								личностной включенности и сопереживания, а в отдельных случаях –
								в раздражительности, негативизме и циничном отношении к коллегам
								и пациентам. На поведенческом уровне «деперсонализация»
								проявляется в высокомерном поведении, использовании
								профессионального сленга, юмора, ярлыков.
							</div>
						</div>
					</div>

					{result === 'Низкая степень' && (
						<div className={styles.recommendations}>
							Рекомендации:
							<div className={styles.header}>
								Все отлично, поддерживайте этот баланс!
							</div>
							<div className={styles.span}>
								Работа, личная жизнь, отдых — все должно быть в равновесии.
								Спите достаточное количество часов, правильно питайтесь,
								занимайтесь спортом. Не останавливайтесь на достигнутом, ставьте
								перед собой новые цели и развивайтесь в профессиональном и
								личностном плане. Обязательно поддерживайте хорошие отношения с
								коллегами и близкими.
							</div>
						</div>
					)}
					{result === 'Средняя степень' && (
						<div className={styles.recommendations}>
							<div className={styles.header}>
								Пора взять паузу и позаботиться о себе. Вот несколько советов,
								которые помогут вам восстановиться:
							</div>
							<ul>
								<li style={{ marginBottom: '3px' }}>
									Вспомните о своих достижениях
								</li>
								<span>
									Составьте список всех своих профессиональных достижений,
									начиная с самых первых. Периодически просматривайте этот
									список, чтобы напомнить себе о своих успехах и зарядиться
									мотивацией
								</span>
								<li style={{ marginTop: '10px' }}>
									Собирайте отзывы и благодарности
								</li>
							</ul>
						</div>
					)}
					{result === 'Высокая степень' && (
						<div className={styles.recommendations}>
							<div className={styles.header}>
								Пора взять паузу и позаботиться о себе. Вот несколько советов,
								которые помогут вам восстановиться:
							</div>
							<div className={styles.span}>
								Не игнорируйте эти сигналы. Продолжительное выгорание может
								привести к серьёзным последствиям для вашего здоровья и карьеры.
								Возьмите отпуск, выходные или просто несколько дней отдыха,
								чтобы восстановить силы. Положительное влияние окажет смена
								обстановки: поездка, новое хобби, встреча с друзьями — все это
								поможет вам отвлечься от работы и зарядиться энергией. Так же
								рекомендуем поговорить с близкими, психологом или коллегами о
								своих переживаниях.
							</div>
						</div>
					)}
					{result === 'Крайне высокая степень' && (
						<div className={styles.recommendations}>
							<div className={styles.header}>
								Пора взять паузу и позаботиться о себе. Вот несколько советов,
								которые помогут вам восстановиться:
							</div>
							<div className={styles.span}>
								Не игнорируйте эти сигналы. Продолжительное выгорание может
								привести к серьёзным последствиям для вашего здоровья и карьеры.
								Возьмите отпуск, выходные или просто несколько дней отдыха,
								чтобы восстановить силы. Положительное влияние окажет смена
								обстановки: поездка, новое хобби, встреча с друзьями — все это
								поможет вам отвлечься от работы и зарядиться энергией. Так же
								рекомендуем поговорить с близкими, психологом или коллегами о
								своих переживаниях.
							</div>
						</div>
					)}
				</div>
			</div>
		</Modal>
	)
}

export default Result
