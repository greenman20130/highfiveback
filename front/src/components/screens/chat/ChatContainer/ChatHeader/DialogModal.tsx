import { Modal } from '@mui/material'
import { FC, useState } from 'react'
import closeBtn from '../../../../../assets/icons/cross.svg'
import styles from '../../../profile/Users/ModalUserMeeting.module.css'
import btnStyles from '../ChatContainer.module.css'

const DialogModal: FC = () => {
	const [open, setOpen] = useState(false)
	const handleOpen = () => setOpen(true)
	const handleClose = () => setOpen(false)
	return (
		<>
			<button className={btnStyles.meetingBtn} onClick={handleOpen}>
				Встреча
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
						<div className={styles.modalHeading}>Предложить встречу</div>
						<button className={styles.closeBtn} onClick={handleClose}>
							<img width={20} height={20} src={closeBtn} />
						</button>
					</div>
					<div className={styles.modalContent}>
						<form>
							<div className={styles.modalInputDateContainer}>
								<div className={styles.timePicker}>
									<input className={styles.inputTime} type="time" />
								</div>
								<div className={styles.datePicker}>
									<input name="date" className={styles.inputDate} type="date" />
								</div>
							</div>
							<div className={styles.modalTextAreaContainer}>
								<textarea
									name="text"
									className={styles.textArea}
									placeholder="Введите текст"
								/>
							</div>
							<div className={styles.modalFooter}>
								<button
									className={styles.btnCreate}
									type="button"
									onClick={() => {
										handleClose()
									}}
								>
									Отправить
								</button>
							</div>
						</form>
					</div>
				</div>
			</Modal>
		</>
	)
}

export default DialogModal
