import cn from 'classnames'
import { NavLink, useLocation } from 'react-router-dom'
import styles from './Menu.module.css'

const MenuItem = ({ title, icon, style = '', link }) => {
	const location = useLocation()
	return (
		<li
			className={cn({
				[styles.activeTab]: location.pathname === link,
				[styles.inactivePage]: style.length > 0,
				[styles.chatContainerTab]: location.pathname.indexOf('chat') === 1,
			})}
		>
			<NavLink to={link}>
				<img src={icon} width={25} height={25} />
				<span>{title}</span>
			</NavLink>
		</li>
	)
}

export default MenuItem
