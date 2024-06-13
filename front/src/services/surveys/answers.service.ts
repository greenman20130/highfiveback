import axios from 'axios'
import { API_URL } from '../../config/api.config'
import { IQuestion } from '../../utils/collectAnswers'

export const AnswersService = {
	async sendAnswer(answer: IQuestion[]) {
		return axios.post<string>(API_URL + `/answers`, {
			pollId: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
			templateId: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
			userId: '3fa85f64-5717-4562-b3fc-2c963f66afa6',
			assessorId: 'string',
			externalId: 'string',
			is_passed: true,
			answers: answer,
		})
	},
}
