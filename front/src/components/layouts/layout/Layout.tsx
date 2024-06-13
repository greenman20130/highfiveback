import { FC } from 'react'
import { Outlet } from 'react-router-dom'
import Navigation from '../navigation/Navigation'
import styles from './Layout.module.css'

interface Props {
	role: boolean
}

const Layout: FC<Props> = ({ role = true }) => {
	return (
		<div className={styles.layout}>
			<Navigation role={role} />
			<div className={styles.center}>
				<Outlet />
			</div>
		</div>
	)
}

export default Layout
