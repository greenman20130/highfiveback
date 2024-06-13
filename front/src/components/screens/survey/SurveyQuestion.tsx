import { FC } from 'react'
import GroupSurveyOption from './GroupSurveyOption'
import styles from './Survey.module.css'
import { IQuestion } from './types/ITemplate'

interface SurveyQuestionProps {
	data: IQuestion[]
	answers: (answer: string, questionId: number, questionText: string) => void
}

const SurveyQuestion: FC<SurveyQuestionProps> = ({ data, answers }) => {
	const collectAnswers = (
		answer: string,
		questionId: number,
		questionText: string
	) => {
		answers(answer, questionId, questionText)
	}
	return (
		<div className={styles.container}>
			{data.map((item) => (
				<div key={item.id}>
					<div className={styles.headingContainer}>
						<span className={styles.heading}>{item.text}</span>
					</div>
					<div>
						<GroupSurveyOption
							options={item.options}
							questionId={item.id}
							questionText={item.description}
							collectAnswers={collectAnswers}
						/>
					</div>
					{item.required === true ? (
						<div className={styles.footerText}>
							<span>*Этот вопрос обязательный</span>
						</div>
					) : null}
				</div>
			))}
		</div>
	)
}

export default SurveyQuestion
