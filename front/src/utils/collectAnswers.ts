export interface IQuestion {
	questionId: number
	text: string
	answer: {
		id: string
		value: string
		image: string
	}[]
}

export const collectAnswers = (
	questionId: number,
	questionText: string,
	result: string,
	questionAnswer: IQuestion[]
) => {
	const lastIndex = questionAnswer.at(-1)
	if (questionId !== lastIndex?.questionId || undefined) {
		questionAnswer.push({
			questionId: questionId,
			text: questionText,
			answer: [
				{
					id: result.split('-')[0],
					value: result.split('-')[1],
					image: '',
				},
			],
		})
	}
	if (questionId === lastIndex?.questionId) {
		const searchTerm = questionId
		const searchIndex = questionAnswer.findIndex(
			(item) => item.questionId === searchTerm
		)
		questionAnswer[searchIndex].answer.splice(0, 3, {
			id: result.split('-')[0],
			value: result.split('-')[1],
			image: '',
		})
	}
	return questionAnswer
}
