import MenuContainer from './MenuContainer/MenuContainer'
import styles from './Navigation.module.css'

const Navigation = ({ role }) => {
	return (
		<div className={styles.navigation}>
			<div className={styles.logo}>High five</div>
			<MenuContainer role={role} />
		</div>
	)
}

export default Navigation
