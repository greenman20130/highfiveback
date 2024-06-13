import { ITask } from '@/components/screens/profile/Schedule/Schedule'
import { FC, useState } from 'react'
import addBtn from '../../../../../assets/icons/plus.svg'
import { IData } from '../../data/dialogs.interface'
import styles from '../ChatContainer.module.css'
import AddTaskModal from './AddTaskModal'

const ChatInfo: FC<{ data: IData }> = ({ data }) => {
	const [select, setSelect] = useState<number[]>([])
	const [tasks, setTasks] = useState<ITask[]>([])
	const addTask = (task: ITask) => {
		setTasks((prevTasks) => [...prevTasks, task])
		console.log(task)
	}

	const checker = (id: number) => {
		if (select.includes(id)) {
			setSelect(select.filter((item) => item !== id))
		} else {
			setSelect((prevSelect) => [...prevSelect, id])
		}
	}

	const getCorrectDate = (date: Date) => {
		const month = String(date).substring(5, 7)
		const day = String(date).substring(8, 10)
		return `${day}.${month}`
	}

	return (
		<div className={styles.dialogInfoContainer}>
			<div className={styles.userInfoContainer}>
				<span className={styles.heading}>О собеседнике</span>
				{data.isAnonymous ? (
					<div className={styles.textContainer}>
						<span className={styles.text}>
							Собеседник решил оставить ФИ анонимным
						</span>
						<span className={styles.text}>
							Уровень выгорания: {data.levelOfBurnout}
						</span>
						<span className={styles.text}>
							Стаж работы: {data.workExperience}
						</span>
					</div>
				) : (
					<div className={styles.textContainer}>
						<span className={styles.text}>{data.chatName}</span>
						<span className={styles.text}>
							Уровень выгорания: {data.levelOfBurnout}
						</span>
						<span className={styles.text}>
							Стаж работы: {data.workExperience}
						</span>
						<span className={styles.text}>Телефон: {data.phoneNumber}</span>
						<span className={styles.text}>E-mail: {data.email}</span>
					</div>
				)}
			</div>
			<div className={styles.filesContainer}>
				<span className={styles.heading}>Файлы</span>
			</div>
			<div className={styles.tasksContainer}>
				<div className={styles.tasksWrapper}>
					<span className={styles.heading}>Задачи</span>
					<AddTaskModal onChange={addTask} />
				</div>
				{tasks.length > 0
					? tasks.map((task) => (
							<div
								className={
									task.isChecked ? styles.taskWrapperRed : styles.taskWrapper
								}
								key={task.id}
							>
								<div style={{ display: 'flex' }}>
									<input
										className={styles.checkbox}
										type="checkbox"
										onClick={() => {
											checker(task.id)
										}}
									/>
									<span
										className={
											select.includes(task.id)
												? styles.dateTextChecked
												: styles.dateText
										}
									>
										{getCorrectDate(task.date)}
									</span>
								</div>
								<span
									className={
										select.includes(task.id) ? styles.textChecked : styles.text
									}
								>
									{task.text}
								</span>
							</div>
					  ))
					: null}
			</div>
			<div className={styles.commentsContainer}>
				<div className={styles.commentsWrapper}>
					<span className={styles.heading}>Комментарии</span>
					<button className={styles.addTaskBtn}>
						<img width={10} height={10} src={addBtn} />
					</button>
				</div>
			</div>
		</div>
	)
}

export default ChatInfo
