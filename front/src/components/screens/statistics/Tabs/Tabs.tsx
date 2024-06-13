import { FC, useState } from 'react'
import Analytics from '../Analytics/Analytics'
import GeneralInfo from '../GeneralInfo/GeneralInfo'
import Profiles from '../Profiles/Profiles'
import TabContent from './TabContent'
import TabNavItem from './TabNavItem'
import './Tabs.css'
import Dynamic from '../4/Dynamic'
// import Button from '../survey/buttons/button'

const Tabs: FC = () => {
	const [activeTab, setActiveTab] = useState('tab1')
	

	return (
		<div className='wrapper__tabs__reports'>
			<div className='wrapper__report__nav'>
				<ul className='nav'>
					<TabNavItem
						title='Общая информация'
						id='tab1'
						activeTab={activeTab}
						setActiveTab={setActiveTab}
					/>
					<TabNavItem
						title='Профили'
						id='tab2'
						activeTab={activeTab}
						setActiveTab={setActiveTab}
					/>
					<TabNavItem
						title='Аналитика'
						id='tab3'
						activeTab={activeTab}
						setActiveTab={setActiveTab}
					/>
					<TabNavItem
						title='Динамика'
						id='tab4'
						activeTab={activeTab}
						setActiveTab={setActiveTab}
					/>
				</ul>
			</div>
			<div className='main__tabs'>
				<div className='outlet'>
					<TabContent id='tab1' activeTab={activeTab}>
						<GeneralInfo />
					</TabContent>
					<TabContent id='tab2' activeTab={activeTab}>
						<Profiles />
					</TabContent>
					<TabContent id='tab3' activeTab={activeTab}>
						<Analytics />
					</TabContent>
					<TabContent id='tab4' activeTab={activeTab}>
						<Dynamic/>
					</TabContent>
				</div>
			</div>
		</div>
	)
}

export default Tabs
