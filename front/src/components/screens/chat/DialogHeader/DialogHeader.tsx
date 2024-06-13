import { ru } from 'date-fns/locale'
import { FC, useState } from 'react'
import DatePicker from 'react-datepicker'
import 'react-datepicker/dist/react-datepicker.css'
import addIcon from '../../../../assets/icons/plus.svg'
import searchIcon from '../../../../assets/icons/search.svg'
import styles from './DialogHeader.module.css'

const DialogHeader: FC = () => {
	const [startDate, setStartDate] = useState<Date | null>(null)
	return (
		<div className={styles.mainContainer}>
			<div className={styles.header}>
				<span className={styles.headerText}>Диалоги</span>
			</div>
			<div className={styles.searchContainer}>
				<div className={styles.searchBar}>
					<input
						className={styles.searchInput}
						type="text"
						placeholder="Поиск"
					></input>
					<button className={styles.searchBarButton}>
						<img src={searchIcon} width={19} height={19} />
					</button>
				</div>
				<div className={styles.searchDateContainer}>
					<DatePicker
						selected={startDate}
						onChange={(date: Date) => setStartDate(() => date)}
						className={styles.datePicker}
						dateFormat="d.MM.yyyy"
						locale={ru}
						placeholderText="Дата"
					/>
					<button className={styles.addBtn}>
						<img src={addIcon} width={19} height={19} />
					</button>
				</div>
				<div className={styles.searchEmployeeContainer}>
					<input
						className={styles.searchEmployeeInput}
						type="text"
						placeholder="Сотрудник"
					/>
					<button className={styles.addBtn}>
						<img src={addIcon} width={19} height={19} />
					</button>
				</div>
			</div>
			<div className={styles.chatContainer}></div>
		</div>
	)
}

export default DialogHeader
