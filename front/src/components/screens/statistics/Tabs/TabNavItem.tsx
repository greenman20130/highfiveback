import { Dispatch, FC } from 'react'

const TabNavItem: FC<{
	id: string
	title: string
	activeTab: string
	setActiveTab: Dispatch<React.SetStateAction<string>>
}> = ({ id, title, activeTab, setActiveTab }) => {
	const handleClick = () => {
		setActiveTab(id)
	}

	return (
		<li onClick={handleClick} className={activeTab === id ? 'active' : ''}>
			<div className='window__tab'>{title}</div>
		</li>
	)
}
export default TabNavItem
