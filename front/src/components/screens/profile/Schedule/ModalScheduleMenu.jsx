import { Modal } from '@mui/material'
import { useState } from 'react'
import closeBtn from '../../../../assets/icons/cross.svg'
import addBtnIcon from '../../../../assets/icons/plus.svg'
import styles from './ModalScheduleMenu.module.css'

const ModalScheduleMenu = ({ onChange }) => {
	const [open, setOpen] = useState(false)
	const handleOpen = () => setOpen(true)
	const handleClose = () => setOpen(false)
	const [time, setTime] = useState('')
	const [date, setDate] = useState('')
	const [text, setText] = useState('')
	const [id, setId] = useState(0)

	const handleSubmit = () => {
		const checkbox = document.querySelector('[type="checkbox"]')
		onChange({
			id: id,
			time: time,
			date: date,
			text: text,
			isChecked: checkbox.checked,
		})
		setTime('')
		setDate('')
		setText('')
		setId(id + 1)
	}

	return (
		<>
			<button onClick={handleOpen} className={styles.addBtn}>
				<img className={styles.addBtnIcon} src={addBtnIcon} />
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
								<div className={styles.timePicker}>
									<input
										className={styles.inputTime}
										type='time'
										onChange={e => setTime(e.target.value)}
									/>
								</div>
								<div className={styles.datePicker}>
									<input
										name='date'
										className={styles.inputDate}
										type='date'
										onChange={e => setDate(e.target.value)}
									/>
								</div>
							</div>
							<div className={styles.modalTextAreaContainer}>
								<textarea
									name='text'
									className={styles.textArea}
									placeholder='Введите текст'
									onChange={e => setText(e.target.value)}
								/>
							</div>
							<div className={styles.modalFooter}>
								<label className={styles.checkboxLabel}>
									<input type='checkbox' className={styles.checkbox} />
									Важная
								</label>
								<button
									className={styles.btnCreate}
									type='button'
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

export default ModalScheduleMenu
