import { ITask } from '@/components/screens/profile/Schedule/Schedule'
import { Modal } from '@mui/material'
import { FC, useState } from 'react'
import closeBtn from '../../../../../assets/icons/cross.svg'
import addBtnIcon from '../../../../../assets/icons/plus.svg'
import styles from '../../../profile/Schedule/ModalScheduleMenu.module.css'
import btnStyles from '../ChatContainer.module.css'

const AddTaskModal: FC<ITask> = ({ onChange }) => {
	const [open, setOpen] = useState(false)
	const handleOpen = () => setOpen(true)
	const handleClose = () => setOpen(false)
	const [date, setDate] = useState('')
	const [text, setText] = useState('')
	const [id, setId] = useState(0)

	const handleSubmit = () => {
		const checkbox = document.getElementById(
			'checkbox'
		) as HTMLInputElement | null
		if (checkbox) {
			onChange({
				id: id,
				date: date,
				text: text,
				isChecked: checkbox.checked,
			})
			setDate('')
			setText('')
			setId(id + 1)
		}
	}
	return (
		<>
			<button onClick={handleOpen} className={btnStyles.meetingBtn}>
				<img width={10} height={10} src={addBtnIcon} />
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
						<div className={styles.modalHeading}>Добавить задачу</div>
						<button className={styles.closeBtn} onClick={handleClose}>
							<img width={20} height={20} src={closeBtn} />
						</button>
					</div>
					<div className={styles.modalContent}>
						<form>
							<div className={styles.modalInputDateContainer}>
								<div className={styles.datePicker}>
									<input
										name="date"
										className={styles.inputDateTask}
										type="date"
										onChange={(e) => setDate(e.target.value)}
									/>
								</div>
							</div>
							<div className={styles.modalTextAreaContainer}>
								<textarea
									name="text"
									className={styles.textArea}
									placeholder="Введите текст"
									onChange={(e) => setText(e.target.value)}
								/>
							</div>
							<div className={styles.modalFooterTask}>
								<label className={styles.checkboxLabel}>
									<input
										id="checkbox"
										type="checkbox"
										className={styles.checkbox}
									/>
									Важная
								</label>
								<button
									className={styles.btnCreateTask}
									type="button"
									onClick={() => {
										handleSubmit()
										handleClose()
									}}
								>
									Создать
								</button>
							</div>
						</form>
					</div>
				</div>
			</Modal>
		</>
	)
}

export default AddTaskModal
