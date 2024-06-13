export interface IData {
	id: number
	chatName: string
	photo: string
	isAnonymous: boolean
	levelOfBurnout: string
	lastMessage: string
	lastMessageDate: string
	unreadMessages: number
	workExperience?: string
	phoneNumber?: string
	email?: string
	messagesData: {
		id: number
		date: string
		messages: {
			id: number
			text?: string
			file?: string[]
			time: string
			senderId: number
		}[]
	}[]
	onChange: (file: { file: string[] }) => void
}

export interface IDataProp {
	data: IData
}
