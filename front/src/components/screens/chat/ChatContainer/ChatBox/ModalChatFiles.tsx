import { Modal } from '@mui/material'
import { FC, useState } from 'react'
import closeBtn from '../../../../../assets/icons/cross.svg'
import addIcon from '../../../../../assets/icons/plus.svg'
import { getDateOnly } from '../../../../../utils/getDateOnly'
import styles from '../../../profile/Schedule/ModalScheduleMenu.module.css'
import { IData } from '../../data/dialogs.interface'
import btnStyles from '../ChatContainer.module.css'

interface ModalChatFilesProps {
	data: IData
	onChange: (file: { file: string[] }) => void
}

const ModalChatFiles: FC<ModalChatFilesProps> = ({ data, onChange }) => {
	const currentDate = getDateOnly()
	const [open, setOpen] = useState(false)
	const handleOpen = () => setOpen(true)
	const handleClose = () => setOpen(false)
	const [id, setId] = useState(2)
	const [messageId, setMessageId] = useState(1)
	const [images, setImages] = useState<string[]>([])
	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		if (e.target.files) {
			const fileList = Array.from(e.target.files)
			fileList.forEach((file) => {
				const reader = new FileReader()
				reader.onloadend = () => {
					setImages((prevImages) => [...prevImages, reader.result as string])
				}
				reader.readAsDataURL(file)
			})
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
							file: images,
							time: new Date().toLocaleString().substring(12, 17),
							senderId: 4,
						},
					],
				})
				onChange({
					file: images,
				})
				setImages([])
				console.log(data.messagesData)
				handleClose()
			} else {
				setMessageId(messageId + 1)
				const searchTerm = currentDate
				const searchIndex = data.messagesData.findIndex(
					(item) => item.date === searchTerm
				)
				data.messagesData[searchIndex].messages.push({
					id: messageId,
					file: images,
					time: new Date().toLocaleString().substring(12, 17),
					senderId: 4,
				})
				onChange({
					file: images,
				})
				setImages([])
				handleClose()
			}
		}
	}
	return (
		<>
			<button onClick={handleOpen} className={btnStyles.addFileBtn}>
				<img src={addIcon} width={15} height={15} />
			</button>
			<Modal
				sx={{
					'& div.MuiModal-backdrop': {
						backgroundColor: 'rgba(255, 255, 255, 0.5)',
					},
				}}
				open={open}
				onClose={handleClose}
			>
				<div className={styles.modalContainer}>
					<div className={styles.modalHeaderContainer}>
						<div className={styles.modalHeading}>Добавить файл</div>
						<button className={styles.closeBtn} onClick={handleClose}>
							<img width={20} height={20} src={closeBtn} />
						</button>
					</div>
					<div id="dropZone" className={styles.modalContentFile}>
						<div className={styles.inputFileRow}>
							<label className={styles.inputFile}>
								<input type="file" onChange={handleChange} />
								<span>Перетащите файлы сюда или нажмите, что бы загрузить</span>
								<span>Максимальный размер файла 100MB</span>
							</label>
						</div>
					</div>
				</div>
			</Modal>
		</>
	)
}

export default ModalChatFiles
