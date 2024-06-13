import { useMutation, useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { FC, useState } from 'react'
import { TemplateService } from '../../../services/surveys/templates.service'
import { IQuestion, collectAnswers } from '../../../utils/collectAnswers'
import styles from './Survey.module.css'
import SurveyHeading from './SurveyHeading'
import SurveyQuestion from './SurveyQuestion'
import Result from './result/Result'

interface FinalResult {
	result: string
	points: {
		'Эмоциональное истощение': number
		'Редукция личных достижений': number
		Деперсонализация: number
	}
}

const SurveyContainer: FC = () => {
	const [answerArray, setAnswer] = useState<IQuestion[]>([])
	const [isResult, setIsResult] = useState(false)
	const [isOpen, setIsOpen] = useState(false)
	const [finalResult, setFinalResult] = useState<FinalResult>({
		result: '',
		points: {
			'Эмоциональное истощение': 0,
			'Редукция личных достижений': 0,
			Деперсонализация: 0,
		},
	})
	const { isLoading, data } = useQuery({
		queryKey: ['template'],
		queryFn: () =>
			TemplateService.getById('ffe20cfa-4cb8-4dc5-b757-e06a037f4882'),
	})

	const templateData = data?.data

	const getAnswer = (
		answer: string,
		questionId: number,
		questionText: string
	) => {
		const answers = collectAnswers(
			questionId,
			questionText,
			answer,
			answerArray
		)
		setAnswer(answers)
	}

	const mutation = useMutation({
		mutationFn: () => {
			return axios.post('https://api.opros.skroy.ru/answers', {
				pollId: 'd39f2956-59c7-4b0e-a4c4-01aabeb65668',
				templateId: 'ffe20cfa-4cb8-4dc5-b757-e06a037f4882',
				userId: 'e937332f-34f2-41f1-868a-1eaa8db789e0',
				answers: answerArray,
			})
		},
		onSuccess: (data) => {
			const response = axios.get(
				'https://hf.skroy.ru/statistics/' + data.data.id
			)
			response.then((response) => {
				const data = response.data
				setFinalResult(data)
				setIsResult(true)
				setIsOpen(true)
			})
		},
	})

	if (isLoading) {
		return <div>Loading...</div>
	} else {
		return (
			<div>
				<SurveyHeading />
				<div className={styles.surveyContainer}>
					{!isLoading && (
						<>
							{templateData &&
								templateData.questions.map((question) => (
									<SurveyQuestion
										key={question.id}
										data={[question]}
										answers={getAnswer}
									/>
								))}
							<div className={styles.btnContainer}>
								<button
									onClick={() => {
										if (answerArray.length !== templateData?.questions.length) {
											alert('Не на все вопросы дан ответ')
										} else {
											mutation.mutate()
										}
									}}
									className={styles.sendBtn}
								>
									Отправить
								</button>
							</div>
						</>
					)}
					{isResult === true && (
						<Result
							result={finalResult.result}
							points={finalResult.points}
							isOpen={isOpen}
						/>
					)}
				</div>
			</div>
		)
	}
}

export default SurveyContainer
