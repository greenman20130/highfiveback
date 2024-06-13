import { FC, useState } from 'react'
import sendIcon from '../../../../../assets/icons/arrow_right.svg'
import noAvatar from '../../../../../assets/images/noAvatar.svg'
import profileImage from '../../../../../assets/images/Фото4.svg'
import myProfileImage from '../../../../../assets/images/Фото5.svg'
import { getDateOnly } from '../../../../../utils/getDateOnly'
import { IData } from '../../data/dialogs.interface'
import styles from '../ChatContainer.module.css'
import ModalChatFiles from './ModalChatFiles'

const ChatBox: FC<{ data: IData }> = ({ data }) => {
	const currentDate = getDateOnly()
	const [id, setId] = useState(2)
	const [messageId, setMessageId] = useState(1)
	const [message, setMessage] = useState('')
	const [images, setImages] = useState<string[]>([])
	const sendMessage = async (event: React.FormEvent<HTMLFormElement>) => {
		event.preventDefault()
		if (message.trim() === '') {
			alert('Введите сообщение')
			return
		}
		const lastIndex = data.messagesData.at(-1)
		if (currentDate !== lastIndex?.date) {
			setId(id + 1)
			setMessageId(messageId + 1)
			data.messagesData.push({
				id: id,
				date: currentDate,
				messages: [
					{
						id: messageId,
						text: message,
						time: new Date().toLocaleString().substring(12, 17),
						senderId: 4,
					},
				],
			})
			setMessage('')
		} else {
			setMessageId(messageId + 1)
			const searchTerm = currentDate
			const searchIndex = data.messagesData.findIndex(
				(item) => item.date === searchTerm
			)
			data.messagesData[searchIndex].messages.push({
				id: messageId,
				text: message,
				time: new Date().toLocaleString().substring(12, 17),
				senderId: 4,
			})
			setMessage('')
		}
	}

	const updateState = (file: { file: string[] }) => {
		setImages((prevImages) => [...prevImages, ...file.file])
	}

	return (
		<div className={styles.dialogWindow}>
			<div className={styles.messagesContainer}>
				{data.messagesData.map((item) => (
					<div key={item.id}>
						<div className={styles.dateContainer}>
							<div className={styles.date}>{item.date}</div>
						</div>
						{item.messages.map((message) => (
							<div key={message.id} className={styles.messageContainer}>
								<div
									className={
										message.senderId === data.id
											? styles.messageWrapperLeft
											: styles.messageWrapperRight
									}
								>
									{message.senderId === data.id ? (
										<>
											<div className={styles.profileImage}>
												<img
													width={54}
													height={54}
													src={
														data.photo === 'assets/images/noAvatar.svg'
															? noAvatar
															: profileImage
													}
												/>
											</div>
											<div className={styles.message}>
												<div className={styles.messageText}>
													<span>{message.text}</span>
													<span className={styles.time}>{message.time}</span>
												</div>
											</div>
										</>
									) : (
										<>
											<div className={styles.myMessage}>
												<div className={styles.messageText}>
													<span className={styles.time}>{message.time}</span>
													{message.text && <span>{message.text}</span>}
													{message.file &&
														message.file.map((fileItem) => (
															<img
																style={{ width: '500px' }}
																src={fileItem}
																alt="a"
															/>
														))}
												</div>
											</div>
											<div className={styles.profileImage}>
												<img width={54} height={54} src={myProfileImage} />
											</div>
										</>
									)}
								</div>
							</div>
						))}
					</div>
				))}
			</div>
			<div className={styles.inputContainer}>
				<ModalChatFiles onChange={updateState} data={data} />
				<form
					className={styles.formContainer}
					onSubmit={(event) => sendMessage(event)}
				>
					<input
						className={styles.inputMessage}
						type="text"
						value={message}
						placeholder="Сообщение..."
						onChange={(e) => setMessage(e.target.value)}
					/>
					<button className={styles.sendBtn} type="submit">
						<img
							src={sendIcon}
							style={{ marginLeft: '-1px', marginTop: '3px' }}
							width={20}
							height={20}
						/>
					</button>
				</form>
			</div>
		</div>
	)
}

export default ChatBox
