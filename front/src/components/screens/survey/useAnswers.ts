import { AnswersService } from '@/services/surveys/answers.service'
import { useQuery } from '@tanstack/react-query'
import { IQuestion } from './GroupSurveyOption'

export const useAnswers = (answerArray: IQuestion[]) => {
	const { isLoading, data } = useQuery({
		queryKey: ['answer'],
		queryFn: () => AnswersService.sendAnswer(answerArray),
	})
	return {isLoading, data}
}
