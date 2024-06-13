import { FC } from 'react'
import { Link } from 'react-router-dom'
import noAvatar from '../../../../assets/images/noAvatar.svg'
import profileImage from '../../../../assets/images/Фото4.svg'
import data from '../data/dialogs.json'
import styles from './Dialogs.module.css'

const Dialogs: FC = () => {
	return (
		<div className={styles.mainContainer}>
			<div className={styles.chatList}>
				<div className={styles.sortHeader}>Все сообщения</div>
				{data.map((item) => (
					<Link key={item.id} to={String(item.id)}>
						<div className={styles.chatItem}>
							<div className={styles.profileImage}>
								<img
									src={
										item.photo === 'assets/images/noAvatar.svg'
											? noAvatar
											: profileImage
									}
									width={70}
									height={70}
								/>
							</div>
							<div className={styles.chatInfo}>
								<span className={styles.chatName}>{item.chatName}</span>
								<span className={styles.lastMessage}>{item.lastMessage}</span>
							</div>
							<div className={styles.chatFooter}>
								<div className={styles.chatTime}>
									{item.lastMessageDate.substring(11, 16)}
								</div>
								{item.unreadMessages > 0 && (
									<div className={styles.unreadMessage}>
										{item.unreadMessages}
									</div>
								)}
							</div>
						</div>
					</Link>
				))}
			</div>
		</div>
	)
}

export default Dialogs
