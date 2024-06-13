import { FC } from 'react'
import { useLocation } from 'react-router-dom'
import { IData } from '../data/dialogs.interface'
import data from '../data/dialogs.json'
import ChatBox from './ChatBox/ChatBox'
import styles from './ChatContainer.module.css'
import ChatHeader from './ChatHeader/ChatHeader'
import ChatInfo from './ChatInfo/ChatInfo'

const ChatContainer: FC = () => {
	const location = useLocation()

	let chat: IData
	if (location.pathname === '/chat/1') {
		chat = data[0]
	} else if (location.pathname === '/chat/2') {
		chat = data[1]
	} else if (location.pathname === '/chat/3') {
		chat = data[2]
	} else {
		throw new Error('Invalid Chat')
	}

	return (
		<div className={styles.mainContainer}>
			<ChatHeader data={chat} />
			<div className={styles.chatContainer}>
				<ChatBox data={chat} />
				<ChatInfo data={chat} />
			</div>
		</div>
	)
}

export default ChatContainer
