import { FC } from 'react'

const TabContent: FC<{
	id: string
	activeTab: string
	children: React.ReactNode
}> = ({ id, activeTab, children }) => {
	return activeTab === id ? <div className='TabContent'>{children}</div> : null
}

export default TabContent
