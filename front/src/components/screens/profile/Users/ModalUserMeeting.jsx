import { Modal } from '@mui/material'
import { useState } from 'react'
import closeBtn from '../../../../assets/icons/cross.svg'
import btnStyles from '../Profile.module.css'
import './ModalUserMeeting.module.css'
import styles from './ModalUserMeeting.module.css'

const ModalUserMeeting = () => {
	const [open, setOpen] = useState(false)
	const handleOpen = () => setOpen(true)
	const handleClose = () => setOpen(false)
	return (
		<>
			<button className={btnStyles.userChat} onClick={handleOpen}>
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
									<input className={styles.inputTime} type='time' />
								</div>
								<div className={styles.datePicker}>
									<input name='date' className={styles.inputDate} type='date' />
								</div>
							</div>
							<div className={styles.modalTextAreaContainer}>
								<textarea
									name='text'
									className={styles.textArea}
									placeholder='Введите текст'
								/>
							</div>
							<div className={styles.modalFooter}>
								<button
									className={styles.btnCreate}
									type='button'
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

export default ModalUserMeeting
