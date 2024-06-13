import recommendationLogo from '../../../../assets/icons/check.svg'
import chatLogo from '../../../../assets/icons/group.svg'
import helpLogo from '../../../../assets/icons/help.svg'
import historyLogo from '../../../../assets/icons/history.svg'
import homeLogo from '../../../../assets/icons/home.svg'
import companyLogo from '../../../../assets/icons/people.svg'
import statisticsLogo from '../../../../assets/icons/pie-chart.svg'
import surveyLogo from '../../../../assets/icons/report.svg'
import settingsLogo from '../../../../assets/icons/settings.svg'
import templatesLogo from '../../../../assets/icons/template.svg'
import styles from './Menu.module.css'
import MenuItem from './MenuItem'

const Menu = ({ role }) => {
	return (
		<div className={styles.menu}>
			<ul className={styles.ul}>
				<MenuItem title={'Профиль'} icon={homeLogo} link={'/profile'} />
				{role === true && (
					<MenuItem
						style={styles.inactivePage}
						title={'Компания'}
						icon={companyLogo}
						link={'/*'}
					/>
				)}
				<MenuItem title={'Опросы'} icon={surveyLogo} link={'/survey'} />
				{role === true && (
					<MenuItem
						style={styles.inactivePage}
						title={'Шаблоны'}
						icon={templatesLogo}
						link={'/*'}
					/>
				)}
				<MenuItem
					style={styles.inactivePage}
					title={'Рекомендации'}
					icon={recommendationLogo}
					link={'/*'}
				/>
				<MenuItem title={'Чат'} icon={chatLogo} link={'/chat'} />
				{role === true && (
					<MenuItem
						title={'Отчеты'}
						icon={statisticsLogo}
						link={'/statistics'}
					/>
				)}
				{role === true && (
					<MenuItem
						style={styles.inactivePage}
						title={'История'}
						icon={historyLogo}
						link={'/*'}
					/>
				)}
				<MenuItem
					style={styles.inactivePage}
					title={'Настройки'}
					icon={settingsLogo}
					link={'/*'}
				/>
				<MenuItem
					style={styles.inactivePage}
					title={'Помощь'}
					icon={helpLogo}
					link={'/*'}
				/>
			</ul>
		</div>
	)
}

export default Menu
