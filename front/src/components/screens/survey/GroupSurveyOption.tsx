import { FC } from 'react'
import RadioGroup from './RadioGroup'
import styles from './Survey.module.css'
import { IOption } from './types/ITemplate'

interface GroupSurveyOptionProps {
	options: IOption[]
	questionId: number
	questionText: string
	collectAnswers: (
		answer: string,
		questionId: number,
		questionText: string
	) => void
}

export interface IQuestion {
	questionId: number
	text: string
	answer: {
		id: string
		value: string
		image: string
	}[]
}

const GroupSurveyOption: FC<GroupSurveyOptionProps> = ({
	options,
	questionId,
	questionText,
	collectAnswers,
}) => {
	const radioAnswer = (answer: string) => {
		collectAnswers(answer, questionId, questionText)
	}
	return (
		<div className={styles.optionsContainer}>
			<RadioGroup radioAnswer={radioAnswer} options={options} />
		</div>
	)
}
export default GroupSurveyOption
