import { FC } from 'react'
import Dialogs from './Dialogs/Dialogs'
import HeaderChat from './DialogHeader/DialogHeader'

const ChatPage: FC = () => {
	return (
		<>
			<HeaderChat />
			<Dialogs />
		</>
	)
}

export default ChatPage
