import { FC } from 'react'
import searchIcon from '../../../../../assets/icons/search.svg'
import { IData } from '../../data/dialogs.interface'
import styles from '../ChatContainer.module.css'
import DialogModal from './DialogModal'

const ChatHeader: FC<{ data: IData }> = ({ data }) => {
	return (
		<div className={styles.headerContainer}>
			<span className={styles.headerText}>{data.chatName}</span>
			<div className={styles.interactionContainer}>
				<DialogModal />
				<button className={styles.searchBtn}>
					<img src={searchIcon} width={19} height={19} />
				</button>
			</div>
		</div>
	)
}

export default ChatHeader
