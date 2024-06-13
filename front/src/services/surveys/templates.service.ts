import axios from 'axios'
import { API_URL } from '../../config/api.config'
import { ITemplate } from '../surveys/../../components/screens/survey/types/ITemplate'

export const TemplateService = {
	async getById(id: string) {
		return axios.get<ITemplate>(API_URL + `/templates/` + id)
	},
}
