export interface ITemplate {
	userId?: number
	companyId?: number
	templateName: string
	templateDescription: string
	imageUrl?: string
	questions: IQuestion[]
}

export interface IQuestion {
	id: number
	text: string
	description: string
	type: string
	required: boolean
	options: IOption[]
}

export interface IOption {
	id: string
	value: string
	image?: string
}
