import exitIcon from '../../../../assets/icons/exit.svg'
import Menu from './Menu'
import styles from './Menu.module.css'
import MenuItem from './MenuItem'
import photo from './Photo.png'

const MenuContainer = ({ role }) => {
	return (
		<>
			<Menu role={role} />
			<div className={styles.profileInfo}>
				<img width={50} height={50} src={photo} alt='Profile' />
				<div className={styles.textContainer}>
					<div className={styles.profileName}>Алена Сон</div>
					<div className={styles.profileWork}>HR</div>
				</div>
			</div>
			<div className={styles.exitButton}>
				<MenuItem title={'Выйти'} icon={exitIcon} />
			</div>
		</>
	)
}

export default MenuContainer
